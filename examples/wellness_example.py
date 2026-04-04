#!/usr/bin/env python3
"""
Wellness & Fitness Example
Demonstrates gym member tracking with automatic check-in
"""

from nwo_cardiac import CSISensor, BLECardiac, FitnessTracker


def main():
    print("=" * 60)
    print("NWO Cardiac SDK - Wellness & Fitness Example")
    print("=" * 60)
    
    # Initialize sensors
    print("\n[1] Initializing sensors...")
    csi = CSISensor(interface="wlan0", channel=36)
    csi.start_capture()
    
    watch = BLECardiac.connect_polar_h10("XX:YY:ZZ:11:22:33")
    watch.connect()
    print("    ✓ Sensors ready")
    
    # Create fitness tracker
    print("\n[2] Setting up fitness tracker...")
    tracker = FitnessTracker(
        gym_id="goldsgym_downtown",
        csi_zones=["cardio_area", "weight_room", "pool"]
    )
    print("    ✓ Tracker configured")
    
    # Member arrives - automatic check-in
    print("\n[3] Member arrival - automatic check-in...")
    checkin = tracker.auto_checkin(
        user_id="member_456",
        csi_sensor=csi,
        wearable_connector=watch,
        verification_method="csi_wearable_pair"
    )
    
    if checkin['success']:
        print(f"    ✓ Welcome! Session ID: {checkin['session_id']}")
        print(f"    Personal Records: {checkin['personal_record']}")
    else:
        print(f"    ✗ Check-in failed: {checkin['reason']}")
        return
    
    # Simulate workout with real-time tracking
    print("\n[4] Simulating workout session...")
    print("    (Updating metrics every minute)")
    
    import time
    for minute in range(1, 6):  # 5-minute workout
        time.sleep(0.5)  # Simulated delay
        
        # Update metrics
        tracker.update_session_metrics(
            user_id="member_456",
            wearable_data={"heart_rate": 130 + minute * 5},
            csi_movement=0.7
        )
        print(f"    Minute {minute}: HR={130 + minute * 5} bpm")
    
    # Checkout and get summary
    print("\n[5] Workout complete - generating summary...")
    summary = tracker.checkout("member_456", watch)
    
    print(f"\n    Workout Summary:")
    print(f"    - Duration: {summary['duration_minutes']} minutes")
    print(f"    - Calories: {summary['calories_burned']}")
    print(f"    - Heart Rate Zones: {summary['heart_rate_zones']}")
    print(f"    - Movement Score: {summary['movement_score']}")
    print(f"    - Achievements: {summary['achievements']}")
    
    # Get leaderboard
    print("\n[6] Gym Leaderboard (Calories this week):")
    leaderboard = tracker.get_leaderboard(metric="calories_this_week", limit=3)
    for entry in leaderboard:
        print(f"    {entry['rank']}. {entry['user_id']}: {entry['value']} cal")
    
    # Cleanup
    csi.stop_capture()
    print("\n✓ Example completed")


if __name__ == "__main__":
    main()
