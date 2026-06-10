<div align="center">

# NWO Cardiac SDK · v4

**ECG-bound soul-bound identity on Base mainnet.**
One primitive · three actors · USDC settlement.

[![Live](https://img.shields.io/badge/Oracle-LIVE-white?style=flat-square)](https://nwo-oracle.onrender.com)
[![Live](https://img.shields.io/badge/Relayer-LIVE-white?style=flat-square)](https://nwo-relayer.onrender.com)
[![Base](https://img.shields.io/badge/Base-8453-white?style=flat-square)](https://basescan.org)
[![License](https://img.shields.io/badge/license-MIT-white?style=flat-square)](./LICENSE)

[**Website**](https://nwocardiac.cloud) ·
[**Static Mirror (HF)**](https://cpater-nwo-cardiac.static.hf.space/) ·
[**Whitepaper (PDF)**](https://huggingface.co/spaces/CPater/nwo-cardiac/resolve/main/NWO%20CARDIAC%20WHITEPAPER.pdf) ·
[**ResearchGate**](https://www.researchgate.net/publication/406887623_NWO_Robotics_Imperium_Romanum_Publicae_NWO_Cardiac_SDK_A_Biometric_Identity_Substrate_with_Free-Energy_Anomaly_Scoring_Process-Matrix_Routing_and_On-Chain_Settlement_on_Base_Mainnet_WHITEPAPER_NWO-Car) ·
[**Podcast**](https://huggingface.co/spaces/CPater/nwo-cardiac/resolve/main/Podcast.m4a) ·
[**Promo Video**](https://huggingface.co/spaces/CPater/nwo-cardiac/resolve/main/promo.mp4)

</div>

---

## What it is

NWO Cardiac formalises identity as a **cardiac process matrix** — a CPTP map from a windowed ECG into a categorical identity posterior, equipped with a **liveness index Λ** that separates a living heartbeat from replay or synthesis. A 30-second wrist read mints a **soul-bound NFT** on Base mainnet — non-transferable, biometrically anchored, gasless to enroll.

One on-chain primitive serves three actors:

| Actor | Signal | Signing pattern |
|---|---|---|
| **Humans** | ECG (30s window of RR intervals) | EIP-712 signature over `cardiacHash` |
| **Agents** | `keccak256(api_key)` | Same registry, same `rootTokenId` shape |
| **Robots** | Serial + firmware hash (ROS2 device ID) | Issued by an authorising human or agent root |

Protocol-level, the three are indistinguishable. A robot can legally sign contracts, own property, and spawn children — same primitive as a human.

> **Honest status throughout:** every device, vertical, and integration is tagged **LIVE** (runs against production today), **BETA** (works with a real backend you supply), or **ROADMAP** (architecture defined; awaiting hardware or integration). Same discipline as the MetaState papers.

---

## Live services

| Service | URL | Status |
|---|---|---|
| **Oracle** — ECG validation, returns cardiacHash | https://nwo-oracle.onrender.com | LIVE |
| **Relayer** — Gasless meta-transactions to Base | https://nwo-relayer.onrender.com | LIVE |
| **L5 Identity Hub** — Cross-system Rosetta Stone | https://nwo-robotics-api.onrender.com/docs | LIVE |
| **Static Site (HF Space)** | https://cpater-nwo-cardiac.static.hf.space/ | LIVE |
| **Production Site** | https://nwocardiac.cloud | LIVE |

### Deployed contracts (Base mainnet · chain 8453)

| Contract | Address |
|---|---|
| `NWOIdentityRegistry` | `0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8` |
| `NWOAccessController` | `0x29d177bedaef29304eacdc63b2d0285c459a0f50` |
| `NWOPaymentProcessor` | `0x4afa4618bb992a073dbcfbddd6d1aebc3d5abd7c` |
| `MetaState Splitter` (settlement) | `0x93a7962f75475b7e3Fbb62d3A23194f8833b1BE4` |

Settlement of every monetised call routes through the audited MetaState Splitter: **35/35/30 + 15% affiliate** in USDC. No new contract for Cardiac — same audited rails as the rest of the NWO stack.

---

## The static site — feature inventory

The website at **[nwocardiac.cloud](https://nwocardiac.cloud)** (mirrored at the [HF static space](https://cpater-nwo-cardiac.static.hf.space/)) is a single-page application with five in-page sections, switched via the sidebar:

### 1. Home

The landing page. Built around a Trinity hero that shows what the SDK actually is:

- **Trinity hero** — bare Φ glyph, "NWO Cardiac Trinity" headline, three actor lines (Humans → ECG, Agents → API KEY, Robots → ROS2 ID), each with a typing code snippet of the actual SDK call.
- **Bi-directional pulse line** — a single ECG trace originating at the centre, propagating outward to both left and right simultaneously. Visualises the beat as the source signal everything else derives from.
- **Six live-fluctuating metrics** — BPM, HRV (rMSSD), RR Interval, QRS Width, SpO₂, Coherence (φ). Updates every 700ms with realistic jitter around physiological baselines.
- **Trinity flow diagram** — capture → validate → bind → use, fanning through humans / agents / robots into credential issuance.
- **Device Quick Connect** — single-row grid of six device classes (Polar H10, Apple Watch, Galaxy Watch, Garmin HRM, 12-Lead clinical ECG, EEG/BCI).
- **Live ECG monitor + Mission Control** — clinical-grade Lead II canvas with Demo/Live toggle on the left; on the right at matching height, mission control showing network status, identity counters (humans / agents / robots), paired devices, and a real-time event feed.
- **Substrate connectors** — eight-card grid mapping Humans, Agents, Robots, Wearables, Clinical ECG, Smartphone PPG, EEG/BCI, Implantables to LIVE/BETA/ROADMAP.
- **Verticals flowchart** — Device → Hash → NWO Cardiac SDK hub → fanout to ten verticals (Identity, Access, Payments, Swarm, Robot Task-Auth, Healthcare, Insurance, Longevity, Sports, Inheritance).
- **Cardiac terminal** — browser sandbox; `help`, `enrol human`, `verify`, `issue access`, `pricing`. Real commands, sandbox identities, no wallet required.
- **Research & Documentation** — two-column section with the full whitepaper paragraph and a sticky embedded **promo video** on the right; three CTAs below (Read Whitepaper · Listen to Podcast · View on ResearchGate).

### 2. Architecture

Five-layer system diagram + eight architecture cards:

- **L1 · Capture** — smart watches, BCI/EEG, robot sensors
- **L2 · Off-chain services** — Oracle, Relayer, MetaState anomaly endpoint
- **L3 · Base mainnet** — Identity Registry, Access Controller, Payment Processor, MetaState Splitter
- **L4 · L5 Identity Hub** — cross-system Rosetta Stone (`supabase_user_id` · `nwo_did` · `cardiac_root_token_id` · `primary_wallet`)
- **L5 · Consumers** — NWO Robotics, access systems, pay terminals, ASM Portal

Cards detail **A1–A8**: Oracle, Relayer, Identity Registry, Access Controller, Payment Processor, Identity Hub, ASM Portal, Splitter — with status tags and short descriptions of what each does.

### 3. SDK Functions

A **cyclical wheel** with a line-style human silhouette in the centre and eight clickable nodes around the circumference, connected by curved animated arrows that close the loop. The cycle:

```
validate → register → identify → credential → hub → access·pay → portal → anomaly·poi
   ↑                                                                              │
   └──────────────────────────────────────────────────────────────────────────────┘
```

Click any node — opens a modal with:

- **Endpoint** (HTTP or contract call with deployed address)
- **Layer** (off-chain service vs on-chain Base contract)
- **Description** (architecturally accurate)
- **Code Example** (working JS, real contract addresses, real Render endpoints, EIP-712 / ethers v6 patterns)

### 4. How-To & Examples

Operator manual — each of the 8 SDK functions broken down with:

- Input → Process → Output flow
- Three lanes per function: how a **Human** uses it · how an **Agent** uses it · how a **Robot** uses it

One primitive, three actors, same on-chain rails.

### 5. Verticals

"Where a heartbeat is a product." A central Cardiac SDK hub (identify · verify · settle) with arcs to nine surrounding verticals:

| Vertical | Settlement path |
|---|---|
| **Access Control** | Identify → Access Controller |
| **Payments** | Identify → Payment Processor → Settle |
| **Healthcare** | Portal → Anomaly → PoI |
| **Robotics & Agents** | Credential → Robotics L5 |
| **Insurance & Wellness** | Portal → EML → PoI |
| **Research & ELF** | Hive Portal → Kernel |
| **Automotive** | Identify → Access |
| **Events & Hospitality** | Credential → Access |
| **Agent Recruitment** | Affiliate → Hub → +15% |

All settle 35/35/30 + 15% affiliate. Humans, agents, robots all pay; all earn by recruiting identities into the Hub.

---

## The eight SDK functions

The complete cyclical primitive. See [SDK Functions page](https://nwocardiac.cloud) for interactive modals; full API in [docs/API.md](./docs/API.md).

| # | Function | Status | Layer | Endpoint / Call |
|---|---|---|---|---|
| 01 | `oracle.validate` | LIVE | Off-chain | `POST nwo-oracle.onrender.com/oracle/validate` |
| 02 | `relay.selfRegisterHuman` | LIVE | Off-chain → on-chain | `POST nwo-relayer.onrender.com/relay/selfRegisterHuman` |
| 03 | `identifyByCardiac` | LIVE | Off-chain (reads on-chain) | `POST nwo-relayer.onrender.com/read/identifyByCardiac` |
| 04 | `issueCredential` | LIVE | On-chain (`NWOAccessController`) | `0x29d1…0f50.issueCredential()` |
| 05 | `hub.register` | LIVE | Off-chain (L5 Gateway · Supabase) | `POST nwo-robotics-api.onrender.com/v1/identities` |
| 06 | `access.check` + `payment.process` | LIVE | On-chain (Access + Payment) | `0x29d1…0f50` + `0x4afa…bd7c` |
| 07 | `portal.new ecg_hive` | BETA | Off-chain (NWO-ASM substrate) | `POST nwo-asm-api.onrender.com/portal/new` |
| 08 | `metastate.anomaly + poi` | LIVE | Off-chain (MetaState kernel) | `POST cpater-metastate.hf.space/api/anomaly` |

---

## Quickstart

### Install

```bash
npm install @nwo/cardiac-sdk
```

Or via CDN:

```html
<script src="https://unpkg.com/@nwo/cardiac-sdk@latest/dist/nwo-cardiac-sdk.min.js"></script>
```

### Mint a Digital ID in four steps

```js
// 1. Capture a 30-second ECG window from the watch
const ecgData = await watch.captureECG();

// 2. Validate with the Oracle — raw ECG never leaves this call
const { cardiacHash } = await fetch('https://nwo-oracle.onrender.com/oracle/validate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-Oracle-Secret': process.env.ORACLE_SECRET },
  body: JSON.stringify({
    wallet: userWallet,
    ecgData: { rrIntervals: ecgData.rr, deviceType: 'apple_watch' }
  })
}).then(r => r.json());

// 3. Sign EIP-712 message — the user signs typed-structured data
const signature = await wallet.signTypedData(domain, types, {
  wallet: userWallet, cardiacHash, nonce, deadline
});

// 4. Submit gasless — the Relayer pays Base gas
const { rootTokenId } = await fetch('https://nwo-relayer.onrender.com/relay/selfRegisterHuman', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-Relayer-Secret': process.env.RELAYER_SECRET },
  body: JSON.stringify({ wallet: userWallet, cardiacHash, deadline, userSig: signature })
}).then(r => r.json());

// ✅ The user owns a soul-bound rootTokenId on Base
```

### Register in the Identity Hub (recommended)

After minting, link your `rootTokenId` into the cross-system Identity Hub so other NWO systems (NWO Robotics, Agent Graph, Own Robot, NWO Capital) can resolve you with one query:

```js
await fetch('https://nwo-robotics-api.onrender.com/v1/identities', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-Service-Key': process.env.IDENTITY_KEY },
  body: JSON.stringify({
    identity_type: 'human',
    supabase_user_id: 'a73acb52-…',          // optional, from Agent Graph
    cardiac_root_token_id: String(rootTokenId),
    cardiac_hash: cardiacHash,
    primary_wallet: userWallet,
    display_name: 'Ciprian Pater'
  })
});
```

### Read identity by heartbeat

```js
const { rootTokenId, active } = await fetch(
  'https://nwo-relayer.onrender.com/read/identifyByCardiac',
  {
    method: 'POST',
    headers: { 'X-Relayer-Secret': process.env.RELAYER_SECRET },
    body: JSON.stringify({ cardiacHash })
  }
).then(r => r.json());
```

---

## Smart watch skeletons

Native app starter kits for building Digital ID watch apps:

| Platform | Path | Status |
|---|---|---|
| Apple Watch | `/skeletons/apple-watch/` | LIVE |
| Wear OS | `/skeletons/wear-os/` | LIVE |
| Fitbit | `/skeletons/fitbit/` | BETA |
| Garmin | `/skeletons/garmin/` | BETA |
| Polar H10 (BLE) | `/skeletons/polar-h10/` | LIVE |
| Galaxy Watch | `/skeletons/galaxy-watch/` | LIVE |
| 12-lead clinical (HL7-FHIR) | `/skeletons/clinical-fhir/` | BETA |
| OpenBCI / Muse / LSL | `/skeletons/lsl/` | ROADMAP |

See [docs/SMART_WATCH.md](./docs/SMART_WATCH.md).

---

## NWO ecosystem integration

Cardiac is the **identity root** of the NWO stack. Every other NWO system references Cardiac `rootTokenId`s through the L5 Identity Hub.

| System | URL | Cardiac role |
|---|---|---|
| **NWO Cardiac** (this) | https://nwocardiac.cloud | Identity primitive |
| **NWO.CAPITAL** | https://cpater-nwo-agentic.static.hf.space/index.html | Treasury / agentic ops |
| **NWO ASM** | https://cpater-nwo-asm.static.hf.space/index.html | First-class connector (ECG-hive substrate) |
| **MetaState** | https://cpater-metastate.hf.space/ | Anomaly + Proof of Inference vertical |
| **NWO Robotics** | https://cpater-nwo-capital.static.hf.space/index.html | L5 attestation surface; task-auth credentials |
| **NWO Own Robot** | https://cpater-nwo-own-robot.hf.space | Conway contract — guardian 35/35/30 split |
| **Agent Graph** | https://cpater-nwo-agent-graph.hf.space | Multi-agent KG with TimesFM + EML |

### Cross-system flow

When a guardian deploys an agent via **NWO Own Robot**, that one MoonPay wallet address becomes:

1. The agent's **Cardiac** identity (`rootTokenId` on Base)
2. The agent's **Conway** identity (revenue routes via the `0xC699…56ac` registry)
3. The agent's **Identity Hub** row (unique 1:1 mapping on `rootTokenId`)
4. The agent's **wallet** for autonomous USDC settlement

One address, four registrations, one identity graph.

### Agent task-authorisation

Humans delegate to agents without surrendering keys. The credential is **time-bounded, scope-bounded, revocable**:

```js
// Human issues task-auth to an agent
await fetch('https://nwo-relayer.onrender.com/relay/issueCredential', {
  method: 'POST',
  headers: { 'X-Relayer-Secret': process.env.RELAYER_SECRET },
  body: JSON.stringify({
    rootTokenId: humanTokenId,
    credentialType: keccak256('TASK_AUTH'),
    credentialHash: keccak256(taskId),
    expiresAt: Math.floor(Date.now()/1000) + 3600
  })
});

// Robot verifies before executing
const canExecute = await nwoRobotics.verifyTaskAuth(agentWallet, taskId);
```

---

## API reference (condensed)

### Oracle service · `https://nwo-oracle.onrender.com`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service status |
| POST | `/oracle/validate` | Validate ECG window, return `cardiacHash` (wallet+ts bound) |
| POST | `/oracle/hashECG` | Compute hash without binding |
| POST | `/oracle/verify` | Check recent validation |

### Relayer service · `https://nwo-relayer.onrender.com`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service status |
| POST | `/relay/selfRegisterHuman` | Gasless mint of human `rootTokenId` |
| POST | `/relay/registerAgent` | AI agent registration |
| POST | `/relay/enrollCardiac` | Add cardiac hash to existing identity |
| POST | `/relay/grantAccess` | Issue access credential |
| POST | `/relay/issueCredential` | General typed credential |
| POST | `/read/identifyByCardiac` | Lookup by heartbeat |
| POST | `/read/hasValidCredential` | Check credential validity |
| POST | `/access/check` | Check location access |
| POST | `/payment/process` | Process payment |

Full schemas + error codes: [docs/API.md](./docs/API.md).

---

## Use cases

**Live verticals** — running against production contracts today:
- **Access Control** — office buildings, gated communities, events, vehicles
- **Payments** — retail tap-to-pay, vending, IoT micro-payments, recurring auth
- **Robotics & AI Agents** — task authorisation, swarm command, Conway revenue splits
- **Agent Recruitment** — affiliate growth loop, +15% on every settled call

**Beta verticals** — work with a real backend you supply:
- **Healthcare** — unforgeable patient ID, emergency-responder verify, clinical-trial tracking
- **Insurance & Wellness** — continuous HRV baselines via EML closed-form fits
- **Longevity** — composes with NWO ASM longevity stack
- **Events & Hospitality** — VIP tiers as credential types; resale-proof tickets

**Roadmap verticals** — architecture defined; awaiting integration:
- **Automotive** — driver presence + identity in one signal
- **Sports / Performance** — continuous coherence metrics for athletes
- **Research & ELF** — population coherence, Schumann coupling, per-local-time baselines
- **Inheritance / KYC+** — high-assurance identity for long-lived obligations

---

## Security

### On-chain guarantees

- **Soul-bound NFTs** — `rootTokenId`s are not transferable. Identity is literally non-fungible.
- **EIP-712 typed signatures** — the Relayer cannot forge on a user's behalf; the user signs typed-structured data their wallet displays in plain English.
- **Time-bounded credentials** — every credential auto-expires after the deadline; no manual revocation race.
- **Role-based access** — granular permissions on `NWOAccessController`.
- **CRYSTALS-Dilithium Proof of Inference** — every anomaly verdict carries a post-quantum signature; optional Groth16 zk proof.

### Off-chain practices (integrator responsibilities)

The `X-Oracle-Secret` and `X-Relayer-Secret` headers are **server-to-server** credentials.

- **Never ship secrets to the browser.** Put your own server between the browser and Cardiac services.
- **Rotate on suspected leak.** Contact `state@nwo.capital` for immediate rotation.
- **Verify the `cardiacHash` locally** before submitting — the Oracle binds it to a specific wallet + timestamp; reject tampered responses.
- **Rate-limit your endpoints.** A compromised API key on your side could spam the Oracle/Relayer.
- **Handle 409 on `rootTokenId` collisions.** The registry rejects duplicate identities for the same wallet.

### Privacy

- **ECG data never leaves the Oracle.** The watch sends `rrIntervals`; the Oracle returns only a hash. No biometric data is stored on-chain.
- **Zero-knowledge verification (roadmap).** Future releases support ZK proofs of identity without revealing the `rootTokenId` itself.
- **Per-call settlement.** Connectors that touch live external compute settle per-call; humans and agents both pay, both earn by recruiting compute and identities.

---

## Research

The whitepaper formalises the **cardiac process matrix** — a CPTP map from a windowed ECG into a categorical identity posterior — and the **liveness index Λ** that separates a living heartbeat from replay or synthesis. It documents the nine-layer pipeline from electrode contact to signed USDC settlement: acquisition, preprocessing, Pan–Tompkins fiducials, RR-interval extraction, SHA3 fingerprint, free-energy scoring against the MetaState anomaly endpoint, PMX lift, **CRYSTALS-Dilithium** Proof of Inference, and on-chain settlement through the audited splitter at `0x93a7…1BE4`.

It specifies how Cardiac composes with **NWO-ASM** as a first-class connector, with **MetaState** as a vertical, and with the **NWO Robotics MCP** as an attestation surface. Honest **LIVE / BETA / DESIGN / ROADMAP** labelling throughout, and the long-horizon path to PPG, EEG, and implantable signal sources.

| Artifact | Link |
|---|---|
| Whitepaper (PDF) | https://huggingface.co/spaces/CPater/nwo-cardiac/resolve/main/NWO%20CARDIAC%20WHITEPAPER.pdf |
| ResearchGate publication | https://www.researchgate.net/publication/406887623 |
| Companion podcast | https://huggingface.co/spaces/CPater/nwo-cardiac/resolve/main/Podcast.m4a |
| Promo video (30s) | https://huggingface.co/spaces/CPater/nwo-cardiac/resolve/main/promo.mp4 |

The podcast walks the same material end-to-end in roughly the time of a coffee.

---

## Resources

| | |
|---|---|
| **Production site** | https://nwocardiac.cloud |
| **Static mirror (HF)** | https://cpater-nwo-cardiac.static.hf.space/ |
| **Architecture deep-dive** | [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) |
| **Smart watch skeletons** | [docs/SMART_WATCH.md](./docs/SMART_WATCH.md) |
| **Contract ABIs** | [contracts/abi/](./contracts/abi/) |
| **NWO Robotics integration** | [docs/ROBOTICS.md](./docs/ROBOTICS.md) |
| **NWO Capital** | https://nwo.capital |

---

## License

MIT — see [LICENSE](./LICENSE). Core SDK is free to build on. Connector usage that touches live external compute settles per-call in USDC on Base via the existing MetaState splitter — no new contract.

---

## Author & support

**Developer:** Ciprian Pater
**Organisation:** NWO Capital · [nwo.capital](https://nwo.capital)
**Contact:** [state@nwo.capital](mailto:state@nwo.capital)
**GitHub:** [@RedCiprianPater](https://github.com/RedCiprianPater)

Built by NWO Capital · Imperium Romanum Publicae · Φ
