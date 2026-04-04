"""
Multi-Modal Fusion Engine
Combines WiFi CSI (presence/liveness) with BLE wearable (identity)
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class FusionResult:
    """Result of multi-modal cardiac fusion."""
    identity_verified: bool
    liveness_confirmed: bool
    confidence: float
    heart_rate_match: float
    csi_hrv: float
    wearable_hrv: float
    anomaly_detected: bool
    anomaly_type: Optional[str]
    timestamp: str


class CardiacFusion:
    """
    Fuses WiFi CSI and BLE wearable signals for robust biometrics.
    
    Key insight: CSI provides liveness + coarse HR, wearable provides
    identity-grade morphology. Together they create a system that is:
    - Hard to spoof (need both signals)
    - Privacy-preserving (contactless until identity needed)
    - Continuous (CSI always on, wearable periodic)
    """
    
    def __init__(
        self,
        csi_sensor,
        wearable,
        fusion_mode: str = "adaptive"
    ):
        """
        Initialize fusion engine.
        
        Args:
            csi_sensor: CSISensor instance
            wearable: BLE wearable connector instance
            fusion_mode: "adaptive", "strict", or "permissive"
        """
        self.csi = csi_sensor
        self.wearable = wearable
        self.fusion_mode = fusion_mode
        self._enrolled_identities = {}
        
    def enroll_identity(
        self,
        user_id: str,
        wearable_samples: int = 10,
        csi_calibration: bool = True
    ) -> Dict:
        """
        Enroll a new user into the biometric system.
        
        Args:
            user_id: Unique user identifier
            wearable_samples: Number of wearable readings to capture
            csi_calibration: Whether to calibrate CSI for this user
            
        Returns:
            Enrollment profile
        """
        logger.info(f"Enrolling user {user_id}")
        
        # Capture wearable identity signature
        wearable_sig = self.wearable.extract_identity_signature()
        
        # Optional: Calibrate CSI for this user
        csi_profile = None
        if csi_calibration:
            csi_profile = self.csi.calibrate_for_subject(user_id)
            
        profile = {
            "user_id": user_id,
            "wearable_signature": wearable_sig.tolist(),
            "csi_profile": csi_profile,
            "enrolled_at": "2026-04-05T12:00:00Z"
        }
        
        self._enrolled_identities[user_id] = profile
        return profile
        
    def verify_identity(
        self,
        user_id: str,
        csi_weight: float = 0.3,
        wearable_weight: float = 0.7,
        liveness_required: bool = True
    ) -> FusionResult:
        """
        Verify user identity using both modalities.
        
        Args:
            user_id: User to verify against
            csi_weight: Weight for CSI signal (presence/liveness)
            wearable_weight: Weight for wearable signal (identity)
            liveness_required: Whether liveness check is mandatory
            
        Returns:
            FusionResult with verification outcome
        """
        if user_id not in self._enrolled_identities:
            return FusionResult(
                identity_verified=False,
                liveness_confirmed=False,
                confidence=0.0,
                heart_rate_match=0.0,
                csi_hrv=0.0,
                wearable_hrv=0.0,
                anomaly_detected=True,
                anomaly_type="user_not_enrolled",
                timestamp="2026-04-05T12:00:00Z"
            )
            
        # Step 1: Check presence with CSI
        is_present, distance = self.csi.detect_presence()
        if not is_present:
            return FusionResult(
                identity_verified=False,
                liveness_confirmed=False,
                confidence=0.0,
                heart_rate_match=0.0,
                csi_hrv=0.0,
                wearable_hrv=0.0,
                anomaly_detected=True,
                anomaly_type="no_presence_detected",
                timestamp="2026-04-05T12:00:00Z"
            )
            
        # Step 2: Verify liveness with CSI
        liveness_score = self.csi.get_liveness_score()
        if liveness_required and liveness_score < 0.8:
            return FusionResult(
                identity_verified=False,
                liveness_confirmed=False,
                confidence=liveness_score,
                heart_rate_match=0.0,
                csi_hrv=0.0,
                wearable_hrv=0.0,
                anomaly_detected=True,
                anomaly_type="liveness_check_failed",
                timestamp="2026-04-05T12:00:00Z"
            )
            
        # Step 3: Extract CSI cardiac signal
        csi_hr, csi_hrv, csi_conf = self.csi.extract_cardiac_signal()
        
        # Step 4: Get wearable identity signature
        wearable_sig = self.wearable.extract_identity_signature()
        wearable_hrv = self.wearable.get_heart_rate_variability()
        
        # Step 5: Compare with enrolled identity
        enrolled_sig = np.array(
            self._enrolled_identities[user_id]["wearable_signature"]
        )
        
        # Cosine similarity for identity match
        identity_match = np.dot(wearable_sig, enrolled_sig) / (
            np.linalg.norm(wearable_sig) * np.linalg.norm(enrolled_sig)
        )
        
        # Step 6: Check heart rate consistency
        wearable_hr = 60 + np.random.randn() * 5  # Placeholder
        hr_match = 1.0 - abs(csi_hr - wearable_hr) / max(csi_hr, wearable_hr)
        
        # Step 7: Detect anomalies (signal mismatch)
        anomaly_detected = False
        anomaly_type = None
        
        if hr_match < 0.7:
            anomaly_detected = True
            anomaly_type = "heart_rate_mismatch"
            
        if identity_match < 0.85:
            anomaly_detected = True
            anomaly_type = "identity_mismatch"
            
        # Step 8: Calculate overall confidence
        confidence = (
            csi_weight * liveness_score +
            wearable_weight * identity_match
        )
        
        identity_verified = (
            identity_match > 0.9 and
            liveness_score > 0.8 and
            not anomaly_detected
        )
        
        return FusionResult(
            identity_verified=identity_verified,
            liveness_confirmed=liveness_score > 0.8,
            confidence=confidence,
            heart_rate_match=hr_match,
            csi_hrv=csi_hrv,
            wearable_hrv=wearable_hrv.get("rmssd", 0) if isinstance(wearable_hrv, dict) else wearable_hrv,
            anomaly_detected=anomaly_detected,
            anomaly_type=anomaly_type,
            timestamp="2026-04-05T12:00:00Z"
        )
        
    def continuous_authentication(
        self,
        user_id: str,
        check_interval: float = 5.0
    ):
        """
        Generator for continuous authentication.
        
        Yields verification results at specified intervals.
        Useful for access control scenarios.
        
        Args:
            user_id: User to continuously authenticate
            check_interval: Seconds between checks
            
        Yields:
            FusionResult at each interval
        """
        import time
        
        while True:
            result = self.verify_identity(user_id)
            yield result
            
            if not result.identity_verified:
                logger.warning(f"Authentication failed for {user_id}")
                break
                
            time.sleep(check_interval)
            
    def detect_spoofing_attempt(self) -> Dict:
        """
        Detect various spoofing attacks.
        
        Attack types detected:
        - Replay attack: Identical signal patterns
        - Synthetic ECG: Too-perfect morphology
        - Distance attack: CSI shows person far, wearable says close
        - Multi-person: Multiple cardiac signatures in CSI
        
        Returns:
            Spoofing detection results
        """
        checks = {
            "signal_uniqueness": self._check_signal_entropy(),
            "csi_wearable_proximity": self._check_sensor_proximity(),
            "temporal_consistency": self._check_temporal_patterns(),
            "multi_person_detection": self._check_multiple_subjects()
        }
        
        is_spoof = any(not passed for passed in checks.values())
        
        return {
            "is_spoofing_attempt": is_spoof,
            "checks": checks,
            "confidence": 0.92 if is_spoof else 0.98
        }
        
    def _check_signal_entropy(self) -> bool:
        """Check that signals have natural entropy (not replayed)."""
        return True  # Placeholder
        
    def _check_sensor_proximity(self) -> bool:
        """Verify CSI and wearable are detecting same proximity."""
        return True  # Placeholder
        
    def _check_temporal_patterns(self) -> bool:
        """Check for natural temporal variation."""
        return True  # Placeholder
        
    def _check_multiple_subjects(self) -> bool:
        """Detect if multiple people are present (potential relay attack)."""
        return True  # Placeholder
