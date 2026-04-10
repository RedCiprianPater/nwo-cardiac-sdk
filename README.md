# NWO Cardiac SDK v4

## Programmable Identity & Digital ID System

The NWO Cardiac SDK enables **biometric digital identity** using ECG/heartbeat signatures from smart watches. This is a **standalone identity system** that can also integrate with NWO Robotics API for autonomous agent authentication.

---

## Quick Links

- **Live Services:**
  - Oracle: `https://nwo-oracle.onrender.com`
  - Relayer: `https://nwo-relayer.onrender.com`
  
- **Deployed Contracts (Base Mainnet):**
  - NWOIdentityRegistry: `0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8`
  - NWOAccessController: `0x29d177bedaef29304eacdc63b2d0285c459a0f50`
  - NWOPaymentProcessor: `0x4afa4618bb992a073dbcfbddd6d1aebc3d5abd7c`

- **Documentation:**
  - [Architecture](./docs/ARCHITECTURE.md)
  - [Smart Watch Integration](./docs/SMARTWATCH.md)
  - [API Reference](./docs/API.md)
  - [NWO Robotics Integration](./docs/ROBOTICS_INTEGRATION.md)
  - [Contract ABI](./docs/CONTRACT_ABI.md)

---

## What is Programmable Identity?

Programmable Identity means your identity is:

1. **Self-sovereign** — You own your identity, not a corporation
2. **Biometrically-secured** — ECG heartbeat is your private key
3. **Portable** — Works across all NWO services
4. **Composable** — Can be used by AI agents on your behalf
5. **Privacy-preserving** — Zero-knowledge proofs for verification

### Identity Types

| Type | Use Case | Registration |
|------|----------|--------------|
| **Human** | Individual users | ECG scan + wallet signature |
| **Agent** | AI assistants | MoonPay wallet + API key |
| **Robot** | Physical robots | Serial number + firmware hash |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         NWO CARDIAC SDK v4                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────┐  │
│  │  Smart Watch │───▶│    Oracle    │───▶│        Relayer           │  │
│  │  (ECG Scan)  │    │  (Validate)  │    │  (Submit to Blockchain)  │  │
│  └──────────────┘    └──────────────┘    └──────────────────────────┘  │
│                                                   │                      │
│                           ┌───────────────────────┘                      │
│                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    BASE MAINNET (Chain ID: 8453)                 │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │   │
│  │  │   NWOIdentity   │  │  NWOAccess      │  │  NWOPayment     │  │   │
│  │  │   Registry      │  │  Controller     │  │  Processor      │  │   │
│  │  │                 │  │                 │  │                 │  │   │
│  │  │ • Humans        │  │ • Locations     │  │ • Terminals     │  │   │
│  │  │ • Agents        │  │ • Access logs   │  │ • Payments      │  │   │
│  │  │ • Robots        │  │ • Time windows  │  │ • Limits        │  │   │
│  │  │ • Credentials   │  │ • Lockdown      │  │ • History       │  │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    INTEGRATION LAYER                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │   │
│  │  │ NWO Robotics│  │  Access     │  │  Payment    │              │   │
│  │  │    API      │  │  Control    │  │  Terminals  │              │   │
│  │  │             │  │  Systems    │  │             │              │   │
│  │  │ • Agent auth│  │ • Door locks│  │ • POS       │              │   │
│  │  │ • Task auth │  │ • Gates     │  │ • Vending   │              │   │
│  │  │ • Swarm     │  │ • Elevators │  │ • IoT       │              │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Getting Started

### 1. Register as Digital ID Holder

```javascript
// Step 1: Capture ECG from smart watch
const ecgData = await watch.captureECG();

// Step 2: Validate with Oracle
const { cardiacHash } = await fetch('https://nwo-oracle.onrender.com/oracle/validate', {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'X-Oracle-Secret': 'your-oracle-secret'
  },
  body: JSON.stringify({
    wallet: userWallet,
    ecgData: {
      rrIntervals: [800, 820, 810, 795, 805],
      deviceType: 'apple_watch'
    }
  })
}).then(r => r.json());

// Step 3: Sign EIP-712 message
const signature = await wallet.signTypedData(domain, types, {
  wallet: userWallet,
  cardiacHash,
  nonce,
  deadline
});

// Step 4: Submit to Relayer (gasless!)
const { rootTokenId } = await fetch('https://nwo-relayer.onrender.com/relay/selfRegisterHuman', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Relayer-Secret': 'your-relayer-secret'
  },
  body: JSON.stringify({
    wallet: userWallet,
    cardiacHash,
    deadline,
    userSig: signature
  })
}).then(r => r.json());

// ✅ You now have a Digital ID (rootTokenId)!
```

### 2. Use Your Digital ID

```javascript
// Check identity by heartbeat
const { rootTokenId, active } = await fetch('https://nwo-relayer.onrender.com/read/identifyByCardiac', {
  method: 'POST',
  headers: { 'X-Relayer-Secret': 'your-relayer-secret' },
  body: JSON.stringify({ cardiacHash })
}).then(r => r.json());

// Verify credentials
const hasAccess = await fetch('https://nwo-relayer.onrender.com/read/hasValidCredential', {
  method: 'POST',
  headers: { 'X-Relayer-Secret': 'your-relayer-secret' },
  body: JSON.stringify({
    rootTokenId,
    credentialType: '0x...' // keccak256("access")
  })
}).then(r => r.json());
```

---

## Smart Watch Integration

We provide skeleton apps for developers to build their own Digital ID watch apps:

| Platform | Location | Status |
|----------|----------|--------|
| **Apple Watch** | `/skeletons/apple-watch/` | ✅ Ready |
| **Wear OS** | `/skeletons/wear-os/` | ✅ Ready |
| **Fitbit** | `/skeletons/fitbit/` | 🚧 Planned |
| **Garmin** | `/skeletons/garmin/` | 🚧 Planned |

See [Smart Watch Integration Guide](./docs/SMARTWATCH.md) for details.

---

## NWO Robotics Integration

Your Digital ID can authorize AI agents and robots:

```javascript
// Agent uses your identity for task authorization
const taskAuth = await fetch('https://nwo-relayer.onrender.com/relay/issueCredential', {
  method: 'POST',
  headers: { 'X-Relayer-Secret': 'your-relayer-secret' },
  body: JSON.stringify({
    rootTokenId: humanTokenId,
    credentialType: '0x...', // CRED_TASK_AUTH
    credentialHash: keccak256(taskId),
    expiresAt: Date.now() / 1000 + 3600 // 1 hour
  })
});

// Robot verifies before executing
const canExecute = await nwoRobotics.verifyTaskAuth(agentWallet, taskId);
```

See [Robotics Integration Guide](./docs/ROBOTICS_INTEGRATION.md) for full details.

---

## SDK Installation

### npm

```bash
npm install @nwo/cardiac-sdk
```

### CDN

```html
<script src="https://unpkg.com/@nwo/cardiac-sdk@latest/dist/nwo-cardiac-sdk.min.js"></script>
```

---

## API Endpoints

### Oracle Service

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service status |
| `/oracle/validate` | POST | Validate ECG, return cardiacHash |
| `/oracle/hashECG` | POST | Compute hash without validation |
| `/oracle/verify` | POST | Check recent validation |

### Relayer Service

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service status |
| `/relay/selfRegisterHuman` | POST | Gasless registration |
| `/relay/registerAgent` | POST | AI agent registration |
| `/relay/enrollCardiac` | POST | Add cardiac hash |
| `/relay/grantAccess` | POST | Issue access credential |
| `/relay/issueCredential` | POST | General credential |
| `/read/identifyByCardiac` | POST | Lookup by heartbeat |
| `/access/check` | POST | Check location access |
| `/payment/process` | POST | Process payment |

See [API Reference](./docs/API.md) for complete documentation.

---

## Use Cases

### 1. Access Control
- **Office buildings** — Tap your wrist to enter
- **Gated communities** — Heartbeat-verified entry
- **Events** — VIP access with biometric check
- **Vehicles** — Car unlock via ECG

### 2. Payments
- **Retail** — Tap-to-pay with cardiac verification
- **Vending** — Biometric micro-payments
- **Subscriptions** — Recurring auth via heartbeat

### 3. Robotics
- **Task authorization** — Approve robot tasks with your identity
- **Swarm control** — Command drone/robot swarms
- **Autonomous agents** — AI acts on your behalf with credentials

### 4. Healthcare
- **Patient ID** — Unforgeable medical identity
- **Emergency access** — First responders verify identity
- **Clinical trials** — Verified participant tracking

---

## Security

- **Soul-bound NFTs** — Non-transferable identities
- **EIP-712 signatures** — Gasless, secure authentication
- **Off-chain oracle** — ECG validation without on-chain exposure
- **Role-based access** — Granular permission system
- **Time-bounded credentials** — Auto-expiring access rights

---

## Resources

- [Architecture Deep Dive](./docs/ARCHITECTURE.md)
- [Smart Watch Skeletons](./skeletons/)
- [Contract ABIs](./docs/CONTRACT_ABI.md)
- [NWO Robotics API](https://nworobotics.cloud)
- [NWO Cardiac Portal](https://nwocardiac.cloud)

---

## License

MIT License — See [LICENSE](./LICENSE)

---

## Support

- **Email:** state@nwo.capital
- **GitHub Issues:** [Report bugs](https://github.com/RedCiprianPater/nwo-cardiac-sdk/issues)

---

Built with ❤️ by NWO Capital
