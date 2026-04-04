"""
NWO Cardiac SDK CLI
Command-line interface for the cardiac biometric SDK
"""

import argparse
import sys
from typing import Optional


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="nwo-cardiac",
        description="NWO Cardiac SDK - Dual-modal cardiac biometrics"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Enroll command
    enroll_parser = subparsers.add_parser(
        "enroll",
        help="Enroll a new user"
    )
    enroll_parser.add_argument("user_id", help="User identifier")
    enroll_parser.add_argument("--wearable", required=True, help="Wearable device ID")
    enroll_parser.add_argument("--csi", action="store_true", help="Enable CSI calibration")
    
    # Verify command
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify user identity"
    )
    verify_parser.add_argument("user_id", help="User identifier")
    verify_parser.add_argument("--wearable", required=True, help="Wearable device ID")
    verify_parser.add_argument("--csi", action="store_true", help="Use CSI for liveness")
    
    # Monitor command
    monitor_parser = subparsers.add_parser(
        "monitor",
        help="Start continuous monitoring"
    )
    monitor_parser.add_argument("patient_id", help="Patient identifier")
    monitor_parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds")
    
    # Access control command
    access_parser = subparsers.add_parser(
        "access",
        help="Access control mode"
    )
    access_parser.add_argument("--entry-id", default="main", help="Entry point ID")
    access_parser.add_argument("--wearable-required", action="store_true", help="Require wearable")
    
    # Wellness command
    wellness_parser = subparsers.add_parser(
        "wellness",
        help="Wellness tracking mode"
    )
    wellness_parser.add_argument("gym_id", help="Gym identifier")
    wellness_parser.add_argument("--user", help="User ID for check-in")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Command handlers
    if args.command == "enroll":
        print(f"Enrolling user: {args.user_id}")
        print(f"Wearable: {args.wearable}")
        print(f"CSI calibration: {args.csi}")
        # TODO: Implement enrollment
        
    elif args.command == "verify":
        print(f"Verifying user: {args.user_id}")
        print(f"Wearable: {args.wearable}")
        print(f"CSI liveness: {args.csi}")
        # TODO: Implement verification
        
    elif args.command == "monitor":
        print(f"Starting monitoring for patient: {args.patient_id}")
        print(f"Interval: {args.interval}s")
        print("Press Ctrl+C to stop")
        # TODO: Implement monitoring loop
        
    elif args.command == "access":
        print(f"Access control mode: {args.entry_id}")
        print(f"Wearable required: {args.wearable_required}")
        print("Waiting for entry requests...")
        # TODO: Implement access control
        
    elif args.command == "wellness":
        print(f"Wellness mode for gym: {args.gym_id}")
        if args.user:
            print(f"User check-in: {args.user}")
        # TODO: Implement wellness tracking
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
