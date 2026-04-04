#!/usr/bin/env python3
"""
Robotics Integration Example
Demonstrates human-aware robot behavior
"""

from nwo_cardiac import CSISensor, BLECardiac, HumanAwareRobot


def main():
    print("=" * 60)
    print("NWO Cardiac SDK - Robotics Integration Example")
    print("=" * 60)
    
    # Initialize sensors
    print("\n[1] Initializing robot sensors...")
    csi = CSISensor(interface="wlan0", channel=36)
    csi.start_capture()
    
    watch = BLECardiac.connect_apple_watch("AA:BB:CC:DD:EE:FF")
    watch.connect()
    print("    ✓ Robot sensors ready")
    
    # Create human-aware robot
    print("\n[2] Creating human-aware robot...")
    robot = HumanAwareRobot(
        robot_id="collaborative_arm_01",
        csi_enabled=True,
        wearable_pairing_optional=True,
        safety_zones=["work_area", "approach_zone"]
    )
    print("    ✓ Robot initialized")
    
    # Register certified operator
    print("\n[3] Registering certified operator...")
    robot.register_certified_operator("operator_123")
    print("    ✓ Operator certified")
    
    # Assess human state
    print("\n[4] Assessing human state...")
    print("    (Detecting operator in work area)")
    
    state = robot.assess_human_state(
        detection_zone="work_area",
        csi_sensor=csi,
        wearable_connector=watch
    )
    
    print(f"\n    Human State Detected:")
    print(f"    - Identity: {state.identity}")
    print(f"    - Heart Rate: {state.heart_rate} bpm")
    print(f"    - Stress Level: {state.stress_level:.1%}")
    print(f"    - Fatigue Level: {state.fatigue_level:.1%}")
    print(f"    - Attention Level: {state.attention_level:.1%}")
    print(f"    - Liveness: {state.liveness_confirmed}")
    print(f"    - Distance: {state.distance_meters}m")
    
    # Identify worker
    print("\n[5] Identifying worker...")
    worker_id = robot.identify_worker(csi, watch)
    
    if worker_id:
        print(f"    ✓ Worker identified: {worker_id}")
        
        if worker_id in robot._certified_operators:
            print("    ✓ Certified operator - enabling advanced mode")
            robot.enable_advanced_mode()
        else:
            print("    ⚠ Uncertified operator - restricting to safe mode")
            robot.restrict_to_safe_mode()
    else:
        print("    ⚠ Worker not identified")
    
    # Adapt behavior based on state
    print("\n[6] Adapting robot behavior...")
    adaptations = robot.adapt_behavior(state)
    
    print(f"\n    Behavior Adaptations:")
    print(f"    - Speed Reduction: {adaptations['speed_reduction']:.0%}")
    print(f"    - Pause Operation: {adaptations['pause_operation']}")
    print(f"    - Request Supervisor: {adaptations['request_supervisor']}")
    print(f"    - Voice Prompts: {adaptations['enable_voice_prompts']}")
    print(f"    - Safety Distance Increase: {adaptations['safety_distance_increase']:.1f}m")
    
    # Get collaboration recommendation
    print("\n[7] Collaboration recommendation...")
    mode = robot.get_collaboration_recommendation()
    print(f"    Recommended Mode: {mode.upper()}")
    
    if mode == "paused":
        print("    → Robot paused for safety")
    elif mode == "supervised":
        print("    → Supervisor oversight required")
    elif mode == "collaborative":
        print("    → Full human-robot collaboration enabled")
    else:
        print("    → Autonomous operation")
    
    # Simulate high-stress scenario
    print("\n[8] Simulating high-stress scenario...")
    state.stress_level = 0.85  # Elevated stress
    state.fatigue_level = 0.70  # High fatigue
    
    print("    ⚠ Operator showing signs of stress and fatigue")
    
    adaptations = robot.adapt_behavior(state)
    
    if adaptations['pause_operation']:
        print("    🛑 ROBOT PAUSED - Operator safety concern")
    
    if adaptations['request_supervisor']:
        print("    📢 Supervisor requested")
    
    # Cleanup
    csi.stop_capture()
    print("\n✓ Example completed")


if __name__ == "__main__":
    main()
