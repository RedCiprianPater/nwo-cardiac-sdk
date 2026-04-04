"""
Access Control Module
Standalone biometric access control using cardiac signatures
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AccessDecision:
    """Access control decision result."""
    granted: bool
    user_id: Optional[str]
    confidence: float
    method: str
    timestamp: str
    audit_id: str
    reason: str


class SecureEntry:
    """
    Standalone access control system using cardiac biometrics.
    
    Use cases:
    - High-security facility entry
    - Data center access
    - Laboratory clean rooms
    - Executive office suites
    """
    
    def __init__(
        self,
        entry_id: str,
        csi_enabled: bool = True,
        wearable_required: bool = True,
        anti_spoofing_level: str = "maximum",
        csi_range_max: float = 2.0
    ):
        """
        Initialize secure entry point.
        
        Args:
            entry_id: Unique identifier for this entry point
            csi_enabled: Use WiFi CSI for presence/liveness
            wearable_required: Require BLE wearable for identity
            anti_spoofing_level: "basic", "enhanced", or "maximum"
            csi_range_max: Maximum detection range in meters
        """
        self.entry_id = entry_id
        self.csi_enabled = csi_enabled
        self.wearable_required = wearable_required
        self.anti_spoofing_level = anti_spoofing_level
        self.csi_range_max = csi_range_max
        self._access_log = []
        self._authorized_users = set()
        
    def enroll_user(
        self,
        user_id: str,
        wearable_connector,
        csi_sensor=None
    ) -> Dict:
        """
        Enroll a user for access to this entry point.
        
        Args:
            user_id: User identifier
            wearable_connector: Connected wearable device
            csi_sensor: Optional CSI sensor for calibration
            
        Returns:
            Enrollment result
        """
        from .fusion import CardiacFusion
        
        fusion = CardiacFusion(
            csi_sensor=csi_sensor,
            wearable=wearable_connector
        )
        
        profile = fusion.enroll_identity(user_id)
        self._authorized_users.add(user_id)
        
        logger.info(f"User {user_id} enrolled for entry {self.entry_id}")
        return profile
        
    def process_entry_request(
        self,
        user_id: Optional[str] = None,
        csi_sensor=None,
        wearable_connector=None
    ) -> AccessDecision:
        """
        Process an entry request.
        
        If user_id is provided, verify that specific user.
        If None, attempt to identify from enrolled users.
        
        Args:
            user_id: Expected user (None for identification mode)
            csi_sensor: CSI sensor instance
            wearable_connector: Wearable connector instance
            
        Returns:
            Access decision
        """
        timestamp = datetime.utcnow().isoformat()
        audit_id = f"{self.entry_id}_{timestamp}_{hash(str(timestamp)) % 10000}"
        
        # Check if CSI detects presence
        if self.csi_enabled and csi_sensor:
            is_present, distance = csi_sensor.detect_presence(
                range_max=self.csi_range_max
            )
            
            if not is_present:
                decision = AccessDecision(
                    granted=False,
                    user_id=user_id,
                    confidence=0.0,
                    method="csi_presence",
                    timestamp=timestamp,
                    audit_id=audit_id,
                    reason="No presence detected"
                )
                self._log_access(decision)
                return decision
                
        # If no wearable required, just check liveness
        if not self.wearable_required and csi_sensor:
            liveness = csi_sensor.get_liveness_score()
            
            if liveness > 0.8:
                decision = AccessDecision(
                    granted=True,
                    user_id=user_id,
                    confidence=liveness,
                    method="csi_liveness_only",
                    timestamp=timestamp,
                    audit_id=audit_id,
                    reason="Liveness confirmed, no identity required"
                )
                self._log_access(decision)
                return decision
                
        # Full biometric verification required
        if wearable_connector is None:
            return AccessDecision(
                granted=False,
                user_id=user_id,
                confidence=0.0,
                method="biometric",
                timestamp=timestamp,
                audit_id=audit_id,
                reason="Wearable required but not provided"
            )
            
        from .fusion import CardiacFusion
        
        fusion = CardiacFusion(
            csi_sensor=csi_sensor,
            wearable=wearable_connector
        )
        
        # If user_id specified, verify that user
        if user_id:
            if user_id not in self._authorized_users:
                return AccessDecision(
                    granted=False,
                    user_id=user_id,
                    confidence=0.0,
                    method="authorization",
                    timestamp=timestamp,
                    audit_id=audit_id,
                    reason="User not authorized for this entry"
                )
                
            result = fusion.verify_identity(user_id)
            
            decision = AccessDecision(
                granted=result.identity_verified,
                user_id=user_id,
                confidence=result.confidence,
                method="cardiac_biometric",
                timestamp=timestamp,
                audit_id=audit_id,
                reason="Identity verified" if result.identity_verified else result.anomaly_type
            )
            
        else:
            # Identification mode - try to match against all enrolled users
            best_match = None
            best_confidence = 0.0
            
            for enrolled_id in self._authorized_users:
                result = fusion.verify_identity(enrolled_id)
                if result.confidence > best_confidence:
                    best_confidence = result.confidence
                    best_match = enrolled_id
                    
            if best_confidence > 0.9:
                decision = AccessDecision(
                    granted=True,
                    user_id=best_match,
                    confidence=best_confidence,
                    method="cardiac_identification",
                    timestamp=timestamp,
                    audit_id=audit_id,
                    reason=f"Identified as {best_match}"
                )
            else:
                decision = AccessDecision(
                    granted=False,
                    user_id=None,
                    confidence=best_confidence,
                    method="cardiac_identification",
                    timestamp=timestamp,
                    audit_id=audit_id,
                    reason="No matching identity found"
                )
                
        self._log_access(decision)
        return decision
        
    def _log_access(self, decision: AccessDecision):
        """Log access attempt for audit."""
        self._access_log.append({
            "audit_id": decision.audit_id,
            "user_id": decision.user_id,
            "granted": decision.granted,
            "confidence": decision.confidence,
            "timestamp": decision.timestamp,
            "reason": decision.reason
        })
        
    def get_access_logs(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve access logs.
        
        Args:
            start_time: Filter logs after this time
            end_time: Filter logs before this time
            user_id: Filter by specific user
            
        Returns:
            List of access log entries
        """
        logs = self._access_log
        
        if user_id:
            logs = [log for log in logs if log["user_id"] == user_id]
            
        return logs
        
    def revoke_access(self, user_id: str) -> bool:
        """
        Revoke a user's access.
        
        Args:
            user_id: User to revoke
            
        Returns:
            True if user was removed
        """
        if user_id in self._authorized_users:
            self._authorized_users.remove(user_id)
            logger.info(f"Access revoked for user {user_id} at entry {self.entry_id}")
            return True
        return False
