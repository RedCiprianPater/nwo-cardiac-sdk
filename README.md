# NWO Cardiac SDK

**Dual-Modal Cardiac Biometrics Platform**

WiFi CSI (contactless) + BLE Wearables (identity-grade) for robust biometric verification.

---

## 🎯 Key Insight

WiFi CSI reliably extracts **heart rate and presence** but NOT identity-grade cardiac morphology. BLE wearables (Apple Watch, Polar H10) provide the missing **identity layer**.

Together they create a system that is:
- ✅ **Hard to spoof** (need both signals)
- ✅ **Privacy-preserving** (contactless until identity needed)
- ✅ **Continuous** (CSI always on, wearable periodic)
- ✅ **Multi-market** (4 independent verticals)

---

## 🚀 Quick Start

```bash
pip install nwo-cardiac
```

```python
from nwo_cardiac import CSISensor, BLECardiac, CardiacFusion

# Initialize sensors
csi = CSISensor(interface="wlan0", channel=36)
watch = BLECardiac.connect_apple_watch("AA:BB:CC:DD:EE:FF")

# Create fusion engine
fusion = CardiacFusion(csi, watch)

# Enroll identity
fusion.enroll_identity("user_123")

# Verify
result = fusion.verify_identity("user_123")
print(f"Verified: {result.identity_verified}, Confidence: {result.confidence}")
```

---

## 📦 Four Independent Markets

### 1. Access Control
```python
from nwo_cardiac import SecureEntry

entry = SecureEntry(
    entry_id="main_door",
    csi_enabled=True,
    wearable_required=True
)

# Walk up, get verified, door opens
result = entry.process_entry_request(
    csi_sensor=csi,
    wearable_connector=watch
)
```

### 2. Wellness & Fitness
```python
from nwo_cardiac import FitnessTracker

tracker = FitnessTracker(gym_id="goldsgym_downtown")

# Automatic check-in
tracker.auto_checkin("member_456", csi, watch)

# Get workout summary
summary = tracker.checkout("member_456")
```

### 3. Clinical Research
```python
from nwo_cardiac import RemoteMonitor

monitor = RemoteMonitor(
    patient_id="patient_789",
    diagnosis="afib_history",
    csi_enabled=True
)

# Detect anomalies
alert = monitor.detect_anomaly(
    anomaly_types=["arrhythmia", "bradycardia"]
)
```

### 4. Robotics (NWO Integration)
```python
from nwo_cardiac import HumanAwareRobot

robot = HumanAwareRobot(robot_id="arm_01")

# Assess human state
state = robot.assess_human_state("work_area", csi, watch)

# Adapt behavior
if state.stress_level > 0.7:
    robot.pause_operation()
```

---

## 🔧 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  WiFi CSI (RuView)          BLE Wearable (Apple/Polar)      │
│  - Presence detection         - ECG morphology                │
│  - Heart rate                 - Clinical-grade signals        │
│  - Liveness                   - Identity signatures           │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               └──────────┬───────────────────┘
                          │
               ┌──────────▼───────────────────┐
               │   Multi-Modal Fusion Engine   │
               │   - Liveness verification     │
               │   - Identity binding          │
               │   - Anomaly detection         │
               └──────────┬────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐     ┌─────▼─────┐    ┌─────▼──────┐
   │ Access  │     │ Wellness  │    │  Clinical  │
   │ Control │     │  & Fitness│    │  Research  │
   └─────────┘     └───────────┘    └────────────┘
```

---

## 📊 Specifications

| Feature | WiFi CSI | BLE Wearable | Combined |
|---------|----------|--------------|----------|
| Range | 0.5-3m | 0-0.5m | 0-3m |
| Heart Rate | ✅ Yes | ✅ Yes | ✅ Yes |
| Identity | ⚠️ No | ✅ Yes | ✅ Yes |
| Liveness | ✅ Yes | ✅ Yes | ✅ Yes |
| Contactless | ✅ Yes | ❌ No | ✅ Yes |
| Clinical Grade | ❌ No | ✅ Yes | ✅ Yes |

---

## 🔒 Security

- **Anti-spoofing**: Requires both CSI motion + wearable ECG
- **Replay protection**: Signal entropy analysis
- **Privacy**: Raw ECG never stored, only identity vectors
- **Compliance**: GDPR-ready, HIPAA-compatible

---

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Integration Guide](docs/INTEGRATION.md)
- [Clinical Use Cases](docs/CLINICAL.md)

---

## 🤝 Integration with NWO Robotics

The SDK is designed to work standalone OR as part of NWO Robotics:

```python
# Standalone
from nwo_cardiac import SecureEntry

# Within NWO Robotics
from nwo.robotics import HumanAwareRobot
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**NWO Capital** | ciprian.pater@publicae.org | https://nwo.capital
