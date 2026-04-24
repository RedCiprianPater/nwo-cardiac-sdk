# NWO Cardiac SDK v4

**Programmable Identity & Digital ID System.** Biometric identity using ECG/heartbeat signatures from smart watches, anchored on Base mainnet as soul-bound NFTs.

> **Live:** [Oracle](https://nwo-oracle.onrender.com) · [Relayer](https://nwo-relayer.onrender.com)
>
> **Status:** ✅ Core on-chain + off-chain services live · 🟡 Smart watch skeletons in progressive release

Cardiac is the **identity root** for the NWO ecosystem. Humans, AI agents, and robots all register here. Every other NWO system (Agent Graph, Own Robot, NWO Robotics L5 Gateway) references Cardiac rootTokenIds through the cross-system Identity Hub.

---

## Quick Links

### Live Services

| Service  | URL                              | Purpose                                |
|----------|----------------------------------|----------------------------------------|
| Oracle   | https://nwo-oracle.onrender.com  | ECG validation, returns `cardiacHash`  |
| Relayer  | https://nwo-relayer.onrender.com | Gasless meta-transactions to Base      |

### Deployed Contracts (Base Mainnet · Chain ID 8453)

| Contract                | Address                                      |
|-------------------------|----------------------------------------------|
| NWOIdentityRegistry     | `0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8` |
| NWOAccessController     | `0x29d177bedaef29304eacdc63b2d0285c459a0f50` |
| NWOPaymentProcessor     | `0x4afa4618bb992a073dbcfbddd6d1aebc3d5abd7c` |

### Documentation

- [Architecture](#architecture-overview)
- [Smart Watch Integration](docs/smart-watch-integration.md)
- [API Reference](docs/api-reference.md)
- [NWO Robotics Integration](#nwo-robotics--ecosystem-integration)
- [Contract ABI](docs/contract-abi.md)

---

## What is Programmable Identity?

Programmable Identity means your identity is:

- **Self-sovereign** — You own your identity, not a corporation
- **Biometrically-secured** — ECG heartbeat is your private key
- **Portable** — Works across all NWO services
- **Composable** — Can be used by AI agents on your behalf
- **Privacy-preserving** — Zero-knowledge proofs for verification

### Identity Types

| Type   | Use Case            | Registration                             |
|--------|---------------------|------------------------------------------|
| Human  | Individual users    | ECG scan + wallet signature              |
| Agent  | AI assistants       | MoonPay wallet + keccak256(api_key)      |
| Robot  | Physical robots     | Serial number + firmware hash            |

All three types share the **same on-chain primitive** — a soul-bound NFT issued by `NWOIdentityRegistry`. Protocol-level, they're indistinguishable. A robot can legally sign contracts, own property, and spawn children — same as a human.

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
│                             │                                            │
│                             │ rootTokenIds referenced by                 │
│                             ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │     NWO IDENTITY HUB (L5 Gateway · public.identities table)      │   │
│  │  Cross-system Rosetta Stone linking:                             │   │
│  │   supabase_user_id · nwo_did · cardiac_root_token_id · wallet    │   │
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

### 1. Register as a Digital ID Holder

```javascript
// Step 1: Capture ECG from smart watch (30 seconds of rhythm)
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

### 2. Register the Identity in the NWO Hub (optional but recommended)

After minting your rootTokenId, register it in the L5 Identity Hub so other NWO systems (Agent Graph, Own Robot, NWO Robotics) can resolve your identity by any anchor:

```javascript
await fetch('https://nwo-robotics-api.onrender.com/v1/identities', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Service-Key': 'your-identity-service-key'  // server-side only
  },
  body: JSON.stringify({
    identity_type: 'human',
    supabase_user_id: 'a73acb52-...',  // from Agent Graph, if present
    cardiac_root_token_id: rootTokenId.toString(),
    cardiac_hash: cardiacHash,
    primary_wallet: userWallet,
    display_name: 'Your Name'
  })
});
```

Now any NWO system can ask "who is this cardiac hash?" and get the full identity graph in one call.

### 3. Use Your Digital ID

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

Skeleton apps for developers building Digital ID watch apps:

| Platform     | Location                   | Status          |
|--------------|----------------------------|-----------------|
| Apple Watch  | `/skeletons/apple-watch/`  | ✅ Ready         |
| Wear OS      | `/skeletons/wear-os/`      | ✅ Ready         |
| Fitbit       | `/skeletons/fitbit/`       | 🟡 Planned       |
| Garmin       | `/skeletons/garmin/`       | 🟡 Planned       |

See [Smart Watch Integration Guide](docs/smart-watch-integration.md) for details.

---

## NWO Robotics & Ecosystem Integration

Cardiac is one of **four concurrent systems** in the NWO stack. Identity is its job; the other three consume it.

### 1. Cardiac SDK (this repo) — identity root
### 2. NWO Robotics L1–L6 — design → parts → print → skills → gateway → market
### 3. NWO Own Robot — Conway contract, 35/35/30 guardian revenue split
### 4. Agent Graph — multi-agent knowledge graph with TimesFM + EML symbolic regression

### How other systems consume Cardiac

**Own Robot** — when a guardian deploys an agent, Own Robot calls the Cardiac Relayer to mint the agent's rootTokenId. The same MoonPay wallet address becomes the agent's Cardiac identity, Conway identity, and Identity Hub record. One address, four registrations.

**L5 Gateway** — when any system creates a new identity, it can reference an existing `cardiac_root_token_id` from this registry. The Hub table has a unique constraint on the rootTokenId column so the mapping is 1:1.

**Agent Graph** — optional ECG verification step for humans. The Supabase `user_profiles.is_cardiac_verified` flag is set after the Relayer confirms a successful mint.

### Agent task-authorization flow

Your Digital ID can authorize AI agents and robots to act on your behalf:

```javascript
// Human issues a task-authorization credential for an agent
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

This is how humans delegate to agents — without giving away their private key. The credential is time-bounded, scope-bounded, and revocable.

See [NWO Robotics Integration Guide](docs/robotics-integration.md) for full details.

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

| Endpoint              | Method | Description                            |
|-----------------------|--------|----------------------------------------|
| `/health`             | GET    | Service status                         |
| `/oracle/validate`    | POST   | Validate ECG, return cardiacHash       |
| `/oracle/hashECG`     | POST   | Compute hash without validation        |
| `/oracle/verify`      | POST   | Check recent validation                |

### Relayer Service

| Endpoint                          | Method | Description                         |
|-----------------------------------|--------|-------------------------------------|
| `/health`                         | GET    | Service status                      |
| `/relay/selfRegisterHuman`        | POST   | Gasless registration                |
| `/relay/registerAgent`            | POST   | AI agent registration               |
| `/relay/enrollCardiac`            | POST   | Add cardiac hash to existing identity |
| `/relay/grantAccess`              | POST   | Issue access credential             |
| `/relay/issueCredential`          | POST   | General credential                  |
| `/read/identifyByCardiac`         | POST   | Lookup by heartbeat                 |
| `/read/hasValidCredential`        | POST   | Check credential validity           |
| `/access/check`                   | POST   | Check location access               |
| `/payment/process`                | POST   | Process payment                     |

See [API Reference](docs/api-reference.md) for complete documentation, request/response schemas, and error codes.

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

### 3. Robotics & AI Agents

- **Task authorization** — Approve robot tasks with your identity
- **Swarm control** — Command drone/robot swarms
- **Autonomous agents** — AI acts on your behalf with credentials
- **Revenue splits** — Conway contract directs 35% to your guardian wallet forever

### 4. Healthcare

- **Patient ID** — Unforgeable medical identity
- **Emergency access** — First responders verify identity
- **Clinical trials** — Verified participant tracking

---

## Security

### On-chain guarantees

- **Soul-bound NFTs** — rootTokenIds cannot be transferred. Identity is literally non-fungible.
- **EIP-712 signatures** — User signs typed-structured data; Relayer cannot forge on their behalf
- **Time-bounded credentials** — Auto-expire after specified deadline
- **Role-based access** — Granular permission system on `NWOAccessController`

### Off-chain practices (integrator responsibilities)

The Oracle and Relayer secrets (`X-Oracle-Secret`, `X-Relayer-Secret`) are server-to-server credentials. If you're integrating:

- **Never ship secrets to the browser.** Put your integration server between the browser and the Cardiac services. The browser should never see the raw oracle/relayer secrets.
- **Rotate on suspected leak.** If any secret appears in logs, screenshots, or a git history, contact state@nwo.capital immediately for rotation.
- **Verify the `cardiacHash` locally** before submitting — the Oracle returns a hash bound to a specific wallet + timestamp; reject tampered responses.
- **Rate-limit your endpoints.** A compromised API key on your side could spam the Oracle/Relayer.
- **Monitor rootTokenId collisions.** If your integration creates multiple identities for the same wallet, the registry will reject; handle the 409 gracefully.

### Privacy notes

- **ECG data never leaves the Oracle.** The watch sends raw rrIntervals to the Oracle; the Oracle returns only a hash. No biometric data is stored on-chain.
- **Zero-knowledge verification roadmap.** Future releases will support ZK proofs of identity without revealing the rootTokenId itself.

---

## Position in the NWO ecosystem — all live URLs

| System                       | URL                                                                      |
|------------------------------|--------------------------------------------------------------------------|
| **Cardiac Oracle (this)**    | https://nwo-oracle.onrender.com                                          |
| **Cardiac Relayer (this)**   | https://nwo-relayer.onrender.com                                         |
| L5 Gateway (identity hub)    | https://nwo-robotics-api.onrender.com/docs                               |
| L1 Design                    | https://nwo-design-engine.onrender.com                                   |
| L2 Parts Gallery             | https://nwo-parts-gallery.onrender.com                                   |
| L3 Printer Connectors        | https://nwo-printer-connectors.onrender.com                              |
| L4 Skill Engine              | https://nwo-skill-engine.onrender.com                                    |
| L6 Market Layer              | https://nwo-market-layer.onrender.com                                    |
| TimesFM + EML                | https://nwo-timesfm.onrender.com                                         |
| Own Robot (Conway)           | https://cpater-nwo-own-robot.hf.space                                    |
| Agent Graph                  | https://cpater-nwo-agent-graph.hf.space                                  |

### Related contracts across the ecosystem

| Contract                  | Chain      | Address                                      |
|---------------------------|------------|----------------------------------------------|
| NWOIdentityRegistry       | Base 8453  | `0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8` |
| NWOAccessController       | Base 8453  | `0x29d177bedaef29304eacdc63b2d0285c459a0f50` |
| NWOPaymentProcessor       | Base 8453  | `0x4afa4618bb992a073dbcfbddd6d1aebc3d5abd7c` |
| Conway Agent Registry     | Base 8453  | `0xC699b07f997962e44d3b73eB8E95d5E0082456ac` |
| NWO API Tier Contract     | Ethereum 1 | `0x1ed4A655F622c09332fA7a67e3F449fe591BC9F6` |

---

## Resources

- [Architecture Deep Dive](docs/architecture.md)
- [Smart Watch Skeletons](skeletons/)
- [Contract ABIs](docs/contract-abi.md)
- [NWO Robotics API](https://github.com/RedCiprianPater/nwo-robotics-api)
- [NWO Cardiac Portal](https://nwo.capital/cardiac)

---

## License

MIT License — See [LICENSE](LICENSE)

---

## Support

- **Email:** state@nwo.capital
- **GitHub Issues:** [Report bugs](https://github.com/RedCiprianPater/nwo-cardiac-sdk/issues)

Built with ❤️ by NWO Capital.
