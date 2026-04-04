#!/usr/bin/env python3
"""
Access Control Example
Demonstrates secure facility entry using cardiac biometrics
"""

from nwo_cardiac import CSISensor, BLECardiac, SecureEntry


def main():
    print("=" * 60)
    print("NWO Cardiac SDK - Access Control Example")
    print("=" * 60)
    
    # Initialize WiFi CSI sensor
    print("\n[1] Initializing WiFi CSI sensor...")
    csi = CSISensor(
        interface="wlan0",
        channel=36,
        sampling_rate=1000
    )
    csi.start_capture()
    print("    ✓ CSI sensor active")
    
    # Connect to wearable
    print("\n[2] Connecting to Apple Watch...")
    watch = BLECardiac.connect_apple_watch(
        device_id="AA:BB:CC:DD:EE:FF"
    )
    watch.connect()
    print("    ✓ Apple Watch connected")
    
    # Create secure entry point
    print("\n[3] Creating secure entry point...")
    entry = SecureEntry(
        entry_id="main_entrance",
        csi_enabled=True,
        wearable_required=True,
        anti_spoofing_level="maximum"
    )
    print("    ✓ Entry point configured")
    
    # Enroll authorized user
    print("\n[4] Enrolling authorized user...")
    profile = entry.enroll_user(
        user_id="employee_007",
        wearable_connector=watch,
        csi_sensor=csi
    )
    print(f"    ✓ User enrolled: {profile['user_id']}")
    
    # Simulate entry attempt
    print("\n[5] Processing entry request...")
    print("    (Simulating user approaching door)")
    
    result = entry.process_entry_request(
        user_id="employee_007",
        csi_sensor=csi,
        wearable_connector=watch
    )
    
    print(f"\n[6] Access Decision:")
    print(f"    Granted: {result.granted}")
    print(f"    User: {result.user_id}")
    print(f"    Confidence: {result.confidence:.2%}")
    print(f"    Method: {result.method}")
    print(f"    Audit ID: {result.audit_id}")
    print(f"    Reason: {result.reason}")
    
    # Cleanup
    csi.stop_capture()
    print("\n✓ Example completed")


if __name__ == "__main__":
    main()
