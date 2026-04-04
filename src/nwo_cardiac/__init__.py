"""
NWO Cardiac SDK - Standalone Biometric Platform
Dual-modal cardiac biometrics: WiFi CSI + BLE Wearables
"""

__version__ = "1.0.0"
__author__ = "NWO Capital"

from .csi_sensor import CSISensor
from .ble_cardiac import BLECardiac
from .fusion import CardiacFusion
from .access import SecureEntry
from .wellness import FitnessTracker
from .clinical import RemoteMonitor
from .robotics import HumanAwareRobot

__all__ = [
    "CSISensor",
    "BLECardiac", 
    "CardiacFusion",
    "SecureEntry",
    "FitnessTracker",
    "RemoteMonitor",
    "HumanAwareRobot"
]
