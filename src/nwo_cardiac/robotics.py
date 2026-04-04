"""
Robotics Integration Module
Human-aware robot behavior using cardiac biometrics
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class HumanState:
    """Detected human state for robot decision-making."""
    identity: Optional[str]
    heart_rate: float
    stress_level: float  # 0-1
    fatigue_level: float  # 0-1
    attention_level: float  # 0-1
    liveness_confirmed: bool
    distance_meters: float


class HumanAwareRobot:
    """
    Robot with human-aware behavior using cardiac sensing.
    
    Enables:
    - Stress-responsive robot behavior
    - Identity-aware collaboration
    - Safety monitoring
    - Natural human-robot interaction
    """
    
    def __init__(
        self,
        robot_id: str,
        csi_enabled: bool = True,
        wearable_pairing_optional: bool = True,
        safety_zones: Optional[List[str]] = None
    ):
        """
        Initialize human-aware robot.
        
        Args:
            robot_id: Robot identifier
            csi_enabled: Use WiFi CSI for presence detection
            wearable_pairing_optional: Allow operation without wearable
            safety_zones: Defined safety zones
        """
        self.robot_id = robot_id
        self.csi_enabled = csi_enabled
        self.wearable_pairing_optional = wearable_pairing_optional
        self.safety_zones = safety_zones or []
        self._current_human_state = None
        self._certified_operators = set()
        
    def assess_human_state(
        self,
        detection_zone: str = "work_area",
        csi_sensor=None,
        wearable_connector=None
    ) -> HumanState:
        """
        Assess current state of human in robot's workspace.
        
        Args:
            detection_zone: Zone to monitor
            csi_sensor: CSI sensor for contactless sensing
            wearable_connector: Optional wearable for detailed vitals
            
        Returns:
            HumanState with stress, fatigue, attention levels
        """
        from .fusion import CardiacFusion
        
        # Default state
        state = HumanState(
            identity=None,
            heart_rate=70,
            stress_level=0.3,
            fatigue_level=0.2,
            attention_level=0.8,
            liveness_confirmed=False,
            distance_meters=2.0
        )
        
        # Detect presence with CSI
        if csi_sensor:
            is_present, distance = csi_sensor.detect_presence()
            if not is_present:
                return state
                
            state.distance_meters = distance
            state.liveness_confirmed = csi_sensor.get_liveness_score() > 0.8
            
            # Get basic HR from CSI
            hr, hrv, _ = csi_sensor.extract_cardiac_signal()
            state.heart_rate = hr
            
            # Estimate stress from HRV (lower HRV = higher stress)
            if hrv < 30:
                state.stress_level = 0.8
            elif hrv < 45:
                state.stress_level = 0.5
            else:
                state.stress_level = 0.2
                
        # Enhance with wearable data
        if wearable_connector:
            fusion = CardiacFusion(csi_sensor, wearable_connector)
            
            # Try to identify worker
            # In production, would check against enrolled operators
            state.identity = "detected_worker"
            
            # Get detailed vitals
            wearable_hr = wearable_connector.get_heart_rate()
            state.heart_rate = wearable_hr
            
            # Estimate fatigue from heart rate patterns
            # Sustained elevated HR = fatigue
            if wearable_hr > 100:
                state.fatigue_level = 0.7
            elif wearable_hr > 85:
                state.fatigue_level = 0.4
            else:
                state.fatigue_level = 0.2
                
        self._current_human_state = state
        return state
        
    def identify_worker(self, csi_sensor=None, wearable_connector=None) -> Optional[str]:
        """
        Identify the human worker in robot's workspace.
        
        Args:
            csi_sensor: CSI sensor
            wearable_connector: Wearable for identity
            
        Returns:
            Worker ID if identified, None otherwise
        """
        if not wearable_connector:
            return None
            
        from .fusion import CardiacFusion
        
        fusion = CardiacFusion(csi_sensor, wearable_connector)
        
        # Check against certified operators
        for operator_id in self._certified_operators:
            result = fusion.verify_identity(operator_id)
            if result.identity_verified:
                return operator_id
                
        return None
        
    def adapt_behavior(self, human_state: HumanState) -> Dict:
        """
        Adapt robot behavior based on human state.
        
        Args:
            human_state: Current human state
            
        Returns:
            Behavior adaptation commands
        """
        adaptations = {
            "speed_reduction": 0.0,
            "pause_operation": False,
            "request_supervisor": False,
            "enable_voice_prompts": False,
            "safety_distance_increase": 0.0
        }
        
        # High stress - slow down and add safety margin
        if human_state.stress_level > 0.7:
            adaptations["speed_reduction"] = 0.5
            adaptations["safety_distance_increase"] = 0.5
            adaptations["enable_voice_prompts"] = True
            
        # High fatigue - pause and alert
        if human_state.fatigue_level > 0.6:
            adaptations["pause_operation"] = True
            adaptations["request_supervisor"] = True
            
        # Low attention - add warnings
        if human_state.attention_level < 0.4:
            adaptations["enable_voice_prompts"] = True
            adaptations["safety_distance_increase"] = 0.3
            
        # Apply adaptations
        if adaptations["pause_operation"]:
            self.pause_operation()
            
        if adaptations["request_supervisor"]:
            self.request_supervisor()
            
        return adaptations
        
    def pause_operation(self):
        """Pause robot operation for safety."""
        logger.info(f"Robot {self.robot_id} pausing operation")
        # Integration with robot control API
        
    def request_supervisor(self):
        """Request human supervisor intervention."""
        logger.info(f"Robot {self.robot_id} requesting supervisor")
        # Send alert to supervisor system
        
    def enable_advanced_mode(self):
        """Enable advanced operation mode for certified operator."""
        logger.info(f"Robot {self.robot_id} enabling advanced mode")
        
    def restrict_to_safe_mode(self):
        """Restrict to safe mode for uncertified operator."""
        logger.info(f"Robot {self.robot_id} restricting to safe mode")
        
    def register_certified_operator(self, operator_id: str):
        """
        Register a certified operator for this robot.
        
        Args:
            operator_id: Operator identifier
        """
        self._certified_operators.add(operator_id)
        logger.info(f"Operator {operator_id} certified for robot {self.robot_id}")
        
    def get_collaboration_recommendation(self) -> str:
        """
        Get recommendation for human-robot collaboration mode.
        
        Returns:
            Recommended mode: "autonomous", "collaborative", "supervised", "paused"
        """
        if not self._current_human_state:
            return "autonomous"
            
        state = self._current_human_state
        
        if state.fatigue_level > 0.7 or state.stress_level > 0.8:
            return "paused"
        elif state.fatigue_level > 0.5 or state.stress_level > 0.6:
            return "supervised"
        elif state.attention_level < 0.5:
            return "supervised"
        else:
            return "collaborative"
