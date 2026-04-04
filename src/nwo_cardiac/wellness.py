"""
Wellness & Fitness Module
Gym/studio member tracking and fitness analytics
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class WorkoutSession:
    """A single workout session record."""
    session_id: str
    user_id: str
    start_time: str
    end_time: Optional[str]
    heart_rate_zones: Dict[str, float]  # time in each zone
    calories_burned: float
    csi_movement_score: float
    recovery_time: Optional[float]


class FitnessTracker:
    """
    Gym/studio fitness tracking using cardiac biometrics.
    
    Features:
    - Automatic check-in (no cards needed)
    - Zone-based heart rate tracking
    - Movement analysis (CSI + wearable)
    - Social features (leaderboards)
    """
    
    def __init__(
        self,
        gym_id: str,
        csi_zones: Optional[List[str]] = None
    ):
        """
        Initialize fitness tracker for a gym/studio.
        
        Args:
            gym_id: Unique gym identifier
            csi_zones: List of CSI-monitored zones (e.g., ["cardio", "weights"])
        """
        self.gym_id = gym_id
        self.csi_zones = csi_zones or []
        self._active_sessions = {}
        self._member_profiles = {}
        
    def auto_checkin(
        self,
        user_id: str,
        csi_sensor=None,
        wearable_connector=None,
        verification_method: str = "csi_wearable_pair"
    ) -> Dict:
        """
        Automatic member check-in using biometrics.
        
        No physical card or app interaction needed - just walk in.
        
        Args:
            user_id: Member identifier
            csi_sensor: CSI sensor at entrance
            wearable_connector: Member's wearable device
            verification_method: "csi_only", "wearable_only", or "csi_wearable_pair"
            
        Returns:
            Check-in result with session info
        """
        from .fusion import CardiacFusion
        
        session_id = f"{self.gym_id}_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        if verification_method == "csi_wearable_pair":
            fusion = CardiacFusion(csi_sensor, wearable_connector)
            result = fusion.verify_identity(user_id)
            
            if not result.identity_verified:
                return {
                    "success": False,
                    "reason": "Identity verification failed",
                    "session_id": None
                }
                
        # Create workout session
        session = WorkoutSession(
            session_id=session_id,
            user_id=user_id,
            start_time=datetime.utcnow().isoformat(),
            end_time=None,
            heart_rate_zones={"rest": 0, "fat_burn": 0, "cardio": 0, "peak": 0},
            calories_burned=0.0,
            csi_movement_score=0.0,
            recovery_time=None
        )
        
        self._active_sessions[user_id] = session
        
        logger.info(f"Member {user_id} checked in at {self.gym_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "welcome_message": f"Welcome back! Your workout is being tracked.",
            "personal_record": self._get_personal_records(user_id)
        }
        
    def update_session_metrics(
        self,
        user_id: str,
        wearable_data: Dict,
        csi_movement: Optional[float] = None
    ):
        """
        Update workout metrics in real-time.
        
        Args:
            user_id: Member identifier
            wearable_data: Current wearable readings
            csi_movement: Movement intensity from CSI (0-1)
        """
        if user_id not in self._active_sessions:
            return
            
        session = self._active_sessions[user_id]
        
        # Update heart rate zones
        hr = wearable_data.get("heart_rate", 70)
        max_hr = self._member_profiles.get(user_id, {}).get("max_hr", 200)
        
        hr_percent = hr / max_hr
        
        if hr_percent < 0.5:
            zone = "rest"
        elif hr_percent < 0.7:
            zone = "fat_burn"
        elif hr_percent < 0.85:
            zone = "cardio"
        else:
            zone = "peak"
            
        session.heart_rate_zones[zone] += 1  # 1 minute increment
        
        # Estimate calories (simplified formula)
        weight_kg = self._member_profiles.get(user_id, {}).get("weight_kg", 75)
        calories_per_min = self._calculate_calories(hr, weight_kg)
        session.calories_burned += calories_per_min
        
        # Update movement score
        if csi_movement:
            session.csi_movement_score = (
                session.csi_movement_score * 0.9 + csi_movement * 0.1
            )
            
    def checkout(
        self,
        user_id: str,
        wearable_connector=None
    ) -> Dict:
        """
        End workout session and generate summary.
        
        Args:
            user_id: Member identifier
            wearable_connector: For recovery heart rate measurement
            
        Returns:
            Workout summary
        """
        if user_id not in self._active_sessions:
            return {"error": "No active session found"}
            
        session = self._active_sessions[user_id]
        session.end_time = datetime.utcnow().isoformat()
        
        # Measure recovery heart rate
        if wearable_connector:
            import time
            time.sleep(60)  # Wait 1 minute
            recovery_hr = wearable_connector.get_heart_rate()
            session.recovery_time = 60 / (recovery_hr - 60) if recovery_hr > 60 else 0
            
        duration_minutes = self._calculate_duration(session)
        
        summary = {
            "session_id": session.session_id,
            "duration_minutes": duration_minutes,
            "calories_burned": round(session.calories_burned, 1),
            "heart_rate_zones": session.heart_rate_zones,
            "movement_score": round(session.csi_movement_score, 2),
            "recovery_time_seconds": session.recovery_time,
            "achievements": self._check_achievements(user_id, session)
        }
        
        del self._active_sessions[user_id]
        
        return summary
        
    def get_session_analytics(
        self,
        user_id: str,
        date: str = "today"
    ) -> Dict:
        """
        Get workout analytics for a member.
        
        Args:
            user_id: Member identifier
            date: Date to analyze ("today", "week", "month")
            
        Returns:
            Analytics summary
        """
        # Placeholder for analytics
        return {
            "total_workouts": 12,
            "total_calories": 8400,
            "avg_heart_rate": 142,
            "favorite_zone": "cardio",
            "improvement_score": 0.15  # 15% improvement
        }
        
    def get_leaderboard(
        self,
        metric: str = "calories_this_week",
        limit: int = 10
    ) -> List[Dict]:
        """
        Get gym leaderboard.
        
        Args:
            metric: Metric to rank by
            limit: Number of top performers
            
        Returns:
            Leaderboard entries
        """
        # Placeholder
        return [
            {"rank": 1, "user_id": "user_001", "value": 3500, "metric": "calories"},
            {"rank": 2, "user_id": "user_002", "value": 3200, "metric": "calories"},
            {"rank": 3, "user_id": "user_003", "value": 3100, "metric": "calories"}
        ]
        
    def _calculate_calories(self, heart_rate: float, weight_kg: float) -> float:
        """Estimate calories burned per minute."""
        # Simplified formula
        return (heart_rate - 60) * weight_kg / 1000
        
    def _calculate_duration(self, session: WorkoutSession) -> float:
        """Calculate session duration in minutes."""
        start = datetime.fromisoformat(session.start_time)
        end = datetime.fromisoformat(session.end_time) if session.end_time else datetime.utcnow()
        return (end - start).total_seconds() / 60
        
    def _get_personal_records(self, user_id: str) -> Dict:
        """Get member's personal records."""
        return {
            "longest_workout": "90 minutes",
            "max_calories": 850,
            "best_recovery": "45 seconds"
        }
        
    def _check_achievements(self, user_id: str, session: WorkoutSession) -> List[str]:
        """Check for earned achievements."""
        achievements = []
        
        if session.calories_burned > 500:
            achievements.append("Calorie Crusher")
            
        if session.heart_rate_zones.get("peak", 0) > 10:
            achievements.append("Peak Performer")
            
        return achievements
