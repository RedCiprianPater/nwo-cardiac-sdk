# NWO Cardiac SDK — Architecture

## System Architecture

The NWO Cardiac Digital ID system is a multi-layer architecture combining off-chain services, on-chain smart contracts, and hardware integrations.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Web App    │  │  Watch App  │  │  Mobile App │  │  Robotics Dashboard │ │
│  │  (React/Vue)│  │  (Swift/Kt) │  │  (iOS/And)  │  │  (nworobotics.cloud)│ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
└─────────┼────────────────┼────────────────┼────────────────────┼────────────┘
          │                │                │                    │
          └────────────────┴────────────────┴────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SERVICE LAYER                                   │
│                                                                              │
│  ┌──────────────────────────────┐  ┌──────────────────────────────────────┐ │
│  │      NWO Oracle Service      │  │        NWO Relayer Service           │ │
│  │  https://nwo-oracle.onrender │  │   https://nwo-relayer.onrender.com   │ │
│  │                              │  │                                      │ │
│  │  • ECG validation            │  │  • Meta-transactions                 │ │
│  │  • Cardiac hash derivation   │  │  • Credential issuance               │  │
│  │  • ML confidence scoring     │  │  • Access control                    │ │
│  │  • Rate limiting             │  │  • Payment processing                │ │
│  │                              │  │  • Event indexing                    │ │
│  └──────────────┬───────────────┘  └──────────────────┬───────────────────┘ │
│                 │                                      │                     │
│                 │  ┌──────────────────────────────────┘                     │
│                 │  │                                                       │
│                 └──┼──────────────────────────────────────────────────────▶│
│                    │                                                       │
└────────────────────┼───────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BLOCKCHAIN LAYER                                   │
│                         Base Mainnet (Chain ID: 8453)                        │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    NWOIdentityRegistry                               │   │
│  │                    0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8       │   │
│  │                                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   Humans     │  │   Agents     │  │   Robots     │              │   │
│  │  │              │  │              │  │              │              │   │
│  │  │ • ECG-based  │  │ • API keys   │  │ • Serial #   │              │   │
│  │  │ • Soul-bound │  │ • MoonPay    │  │ • Firmware   │              │   │
│  │  │ • Credentials│  │ • Delegation │  │ • Updates    │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                    Child SBTs (Credentials)                   │   │   │
│  │  │  • CRED_CARDIAC    • CRED_ACCESS    • CRED_PAYMENT          │   │   │
│  │  │  • CRED_API_KEY    • CRED_HW_CERT   • CRED_FIRMWARE         │   │   │
│  │  │  • CRED_TASK_AUTH  • CRED_CAPABILITY                        │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────────┐  │
│  │   NWOAccessController   │  │        NWOPaymentProcessor              │  │
│  │   0x29d177be...a0f50    │  │        0x4afa4618...abd7c               │  │
│  │                         │  │                                         │  │
│  │  • Location registry    │  │  • Terminal registration                │  │
│  │  • Time-based access    │  │  • Payment method linking               │  │
│  │  • Entity filtering     │  │  • Daily limits                         │  │
│  │  • Lockdown controls    │  │  • Multi-currency                       │  │
│  │  • Access logs          │  │  • Transaction history                  │  │
│  └─────────────────────────┘  └─────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           HARDWARE LAYER                                     │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Apple Watch  │  │   Wear OS    │  │   ESP32-S3   │  │  NWO Robotics  │  │
│  │              │  │              │  │              │  │                │  │
│  │ • HealthKit  │  │ • Health Svcs│  │ • BLE GATT   │  │ • ROS2         │  │
│  │ • ECG access │  │ • Heart rate │  │ • ECG sensor │  │ • Autonomous   │  │
│  │ • Secure En. │  │ • Wearable   │  │ • Door ctrl  │  │ • Swarm        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flows

### 1. Human Self-Registration (Gasless)

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Watch   │────▶│  Oracle  │────▶│   User   │────▶│ Relayer  │
│ ECG Scan │     │ Validate │     │  Sign    │     │  Submit  │
└──────────┘     └──────────┘     └──────────┘     └────┬─────┘
                                                        │
                                                        ▼
                                               ┌────────────────┐
                                               │ Base Mainnet   │
                                               │ Identity NFT   │
                                               └────────────────┘
```

**Steps:**
1. Watch captures ECG signal
2. Oracle validates and derives `cardiacHash`
3. User signs EIP-712 `SelfRegister` message
4. Relayer submits meta-transaction (pays gas)
5. Identity NFT minted on Base

### 2. Door Access (Physical)

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   ESP32  │────▶│  Relayer │────▶│  Access  │────▶│  Door    │
│  BLE NFC │     │ Identify │     │ Controller│    │  Unlock  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

**Steps:**
1. User taps wrist to ESP32 reader
2. ESP32 sends `cardiacHash` to Relayer
3. Relayer identifies `rootTokenId`
4. Access Controller checks credentials
5. Door unlocks if authorized

### 3. Payment (Tap-to-Pay)

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Watch   │────▶│  Relayer │────▶│  Payment │────▶│  Bank/   │
│   NFC    │     │ Identify │     │ Processor│     │  Crypto  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

**Steps:**
1. User taps watch to POS terminal
2. Terminal sends `cardiacHash` + amount
3. Payment Processor verifies identity
4. Checks payment credential + daily limits
5. Approves or denies transaction

### 4. Robotics Task Authorization

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   User   │────▶│  Relayer │────▶│   NWO    │────▶│  Robot   │
│  Approve │     │ Issue Cred│    │ Robotics │     │ Execute  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

**Steps:**
1. User approves robot task in app
2. Relayer issues `CRED_TASK_AUTH` SBT
3. NWO Robotics API verifies credential
4. Robot executes task with auth proof

## Smart Contract Architecture

### NWOIdentityRegistry

```solidity
// Core identity storage
mapping(uint256 => Identity) public identities;
mapping(address => uint256) public walletToRootToken;
mapping(bytes32 => uint256) public cardiacHashToToken;

// Soul-bound NFT (non-transferable)
function _update(address to, uint256 tokenId, address auth) internal override {
    require(_ownerOf(tokenId) == address(0), "NT"); // Non-transferable
    return super._update(to, tokenId, auth);
}

// Credential SBTs
struct ChildSBT {
    bool revoked;
    address issuedBy;
    uint48 issuedAt;
    uint48 expiresAt;
    bytes32 credentialType;
    bytes32 credentialHash;
}
```

### Role System

```
┌─────────────────────────────────────────────────────────┐
│                    ROLE HIERARCHY                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  DEFAULT_ADMIN_ROLE                                      │
│  └── Can grant/revoke any role                          │
│                                                          │
│  ├── REGISTRAR_ROLE ──────► registerHuman()             │
│  │                         registerRobot()              │
│  │                                                        │
│  ├── ISSUER_ROLE ─────────► issueCredential()           │
│  │                         grantAccess()                │
│  │                         enrollCardiac()              │
│  │                                                        │
│  ├── RELAYER_ROLE ────────► selfRegisterHuman()         │
│  │                         renewAgentKey()              │
│  │                         updateRobotFirmware()        │
│  │                                                        │
│  ├── SENSOR_ROLE ─────────► registerHuman() (idempotent)│
│  │                                                        │
│  └── ROBOT_ROLE ──────────► updateRobotFirmware()       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Security Model

### Trust Assumptions

| Component | Trust Level | Notes |
|-----------|-------------|-------|
| **Oracle** | Medium | Off-chain ECG validation; compromise allows fake registrations |
| **Relayer** | High | Holds all roles; compromise = full system control |
| **Contracts** | High | On-chain, immutable, audited |
| **User Wallet** | Critical | Self-sovereign; user controls identity |

### Security Measures

1. **Multi-sig Admin** (recommended for production)
2. **Rate Limiting** on oracle/relayer
3. **Credential Expiry** — time-bounded access
4. **Revocation** — issuers can revoke credentials
5. **Audit Logs** — all access on-chain

## Gas Optimization

| Operation | Gas | Cost (@ 0.1 gwei) |
|-----------|-----|-------------------|
| selfRegisterHuman | 150,000 | ~$0.03 |
| registerAgent | 120,000 | ~$0.025 |
| grantAccess | 80,000 | ~$0.016 |
| checkAccess | 45,000 | ~$0.009 |
| processPayment | 60,000 | ~$0.012 |

## Scalability

### Current Limits

- **Registration**: ~50/hour per oracle (rate limited)
- **Access checks**: Unlimited (view functions)
- **Credentials**: Unlimited per identity
- **Locations**: Unlimited (with LOCATION_ADMIN_ROLE)

### Future Scaling

- **Layer 2**: Already on Base (low gas)
- **The Graph**: Indexing for fast queries
- **IPFS**: Off-chain credential metadata
- **ZK Proofs**: Privacy-preserving verification

## Integration Points

### For Developers

```javascript
// Initialize SDK
import { NWOCardiac } from '@nwo/cardiac-sdk';

const nwo = new NWOCardiac({
  oracleURL: 'https://nwo-oracle.onrender.com',
  relayerURL: 'https://nwo-relayer.onrender.com',
  registryAddress: '0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8',
  chainId: 8453
});

// Register user
const identity = await nwo.register({
  wallet: userAddress,
  ecgData: watchData,
  signature: userSig
});
```

### For Hardware Manufacturers

See [Smart Watch Integration](./SMARTWATCH.md) for:
- ECG capture specifications
- API communication protocols
- Security requirements
- Certification process

### For Robotics Developers

See [Robotics Integration](./ROBOTICS_INTEGRATION.md) for:
- Agent authentication
- Task authorization flows
- Swarm coordination
- Safety mechanisms

---

## Resources

- [Contract Source Code](https://github.com/RedCiprianPater/nwo-identity-services)
- [API Documentation](./API.md)
- [Smart Watch Skeletons](../skeletons/)
- [NWO Robotics API](https://nworobotics.cloud/docs)