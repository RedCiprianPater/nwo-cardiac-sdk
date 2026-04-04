#!/usr/bin/env python3
"""
Clinical Research Example
Demonstrates remote patient monitoring with anomaly detection
"""

from nwo_cardiac import CSISensor, BLECardiac, RemoteMonitor


def alert_callback(alert):
    """Handle clinical alerts."""
    print(f"\n    🚨 ALERT: {alert.alert_type}")
    print(f"       Severity: {alert.severity}")
    print(f"       Message: {alert.message}")
    print(f"       Action: {alert.recommended_action}")


def main():
    print("=" * 60)
    print("NWO Cardiac SDK - Clinical Research Example")
    print("=" * 60)
    
    # Initialize sensors
    print("\n[1] Initializing clinical monitoring setup...")
    csi = CSISensor(interface="wlan0", channel=36)
    csi.start_capture()
    
    # Use Polar H10 for clinical-grade ECG
    polar = BLECardiac.connect_polar_h10("XX:YY:ZZ:11:22:33")
    polar.connect()
    polar.start_ecg_stream()
    print("    ✓ Clinical sensors ready")
    
    # Create remote monitor
    print("\n[2] Setting up remote patient monitor...")
    monitor = RemoteMonitor(
        patient_id="patient_789",
        diagnosis="afib_history",
        csi_enabled=True,  # For medication adherence
        wearable_model="polar_h10",
        alert_callbacks=[alert_callback]
    )
    print("    ✓ Monitor configured")
    
    # Simulate patient monitoring
    print("\n[3] Starting patient monitoring...")
    print("    (Checking for anomalies)")
    
    # Simulate a few checks
    import time
    for check in range(1, 4):
        print(f"\n    Check {check}:")
        
        # Get ECG sample
        ecg = polar.get_ecg_sample(duration=10)
        print(f"      - ECG quality: {ecg['quality_score']:.2%}")
        
        # Check for arrhythmia
        arrhythmia = polar.detect_arrhythmia(ecg)
        print(f"      - Sinus rhythm: {arrhythmia['sinus_rhythm']:.2%}")
        print(f"      - AFib probability: {arrhythmia['atrial_fibrillation']:.2%}")
        
        # Detect anomalies
        alert = monitor.detect_anomaly(
            anomaly_types=["arrhythmia", "bradycardia", "tachycardia"],
            csi_sensor=csi,
            wearable_connector=polar
        )
        
        if alert:
            print(f"      - Alert generated: {alert.alert_id}")
        else:
            print(f"      - No anomalies detected")
        
        time.sleep(1)
    
    # Get patient summary
    print("\n[4] Generating patient summary...")
    summary = monitor.get_patient_summary(days=7)
    
    print(f"\n    Patient Summary (Last 7 days):")
    print(f"    - Patient ID: {summary['patient_id']}")
    print(f"    - Diagnosis: {summary['diagnosis']}")
    print(f"    - Avg Heart Rate: {summary['avg_heart_rate']} bpm")
    print(f"    - Avg HRV: {summary['avg_hrv']} ms")
    print(f"    - Arrhythmia Episodes: {summary['arrhythmia_episodes']}")
    print(f"    - Device Adherence: {summary['device_adherence']:.1%}")
    print(f"    - Trend: {summary['trend']}")
    
    # Export clinical data
    print("\n[5] Exporting clinical data (HL7 format)...")
    hl7_data = monitor.export_clinical_data(format="hl7")
    print(f"    {hl7_data[:200]}...")
    
    # Cleanup
    polar.stop_ecg_stream()
    csi.stop_capture()
    print("\n✓ Example completed")


if __name__ == "__main__":
    main()
