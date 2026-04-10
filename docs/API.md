# NWO Cardiac SDK — API Reference

Complete API reference for Oracle and Relayer services.

## Base URLs

| Service | URL |
|---------|-----|
| Oracle | `https://nwo-oracle.onrender.com` |
| Relayer | `https://nwo-relayer.onrender.com` |

## Authentication

All endpoints (except `/health`) require authentication via headers:

```
X-Oracle-Secret: your-oracle-secret
X-Relayer-Secret: your-relayer-secret
```

## Oracle Service

### GET /health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "oracle": "0x...",
  "balance": "0.01 ETH",
  "chain": "Base",
  "version": "v4-compatible",
  "config": {
    "minEcgSamples": 256,
    "minRrIntervals": 5,
    "confidenceThreshold": 0.85
  }
}
```

### POST /oracle/validate

Validate ECG data and derive cardiac hash.

**Request:**
```json
{
  "wallet": "0x15Ac500528aE3Ae0dbdbF2Cd1aDC73Ef7f27EE77",
  "ecgData": {
    "samples": [0.0, 0.1, 0.5, 1.0, 0.5, 0.1, 0.0],
    "rrIntervals": [800, 820, 810, 795, 805],
    "sampleRate": 512,
    "deviceType": "apple_watch"
  }
}
```

**Response (Success):**
```json
{
  "valid": true,
  "cardiacHash": "0x5c534d9e3c8b4f2a1e6d7c9b0a8f3e2d1c4b5a6...",
  "confidence": 0.92,
  "features": {
    "meanRR": 810,
    "sdnn": 45.2,
    "rmssd": 32.1,
    "heartRate": 74,
    "morphologyScore": 0.92
  },
  "expiresAt": 1704067200,
  "note": "Sign SelfRegister EIP-712 with this cardiacHash"
}
```

**Response (Invalid ECG):**
```json
{
  "valid": false,
  "reason": "Too few RR intervals (min 5)",
  "confidence": 0
}
```

### POST /oracle/hashECG

Compute cardiac hash without full validation.

**Request:**
```json
{
  "wallet": "0x...",
  "ecgData": {
    "rrIntervals": [800, 820, 810, 795, 805]
  }
}
```

**Response:**
```json
{
  "cardiacHash": "0x...",
  "confidence": 0.92,
  "features": {
    "meanRR": 810,
    "sdnn": 45.2,
    "rmssd": 32.1,
    "heartRate": 74,
    "morphologyScore": 0.92
  }
}
```

### POST /oracle/verify

Check if wallet + cardiacHash combo was validated recently.

**Request:**
```json
{
  "wallet": "0x...",
  "cardiacHash": "0x..."
}
```

**Response:**
```json
{
  "approved": true,
  "source": "in-memory",
  "note": "Resets on service restart"
}
```

## Relayer Service

### GET /health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "chain": "Base",
  "chainId": "8453",
  "relayer": "0x15Ac500528aE3Ae0dbdbF2Cd1aDC73Ef7f27EE77",
  "balance": "0.01 ETH",
  "blockNumber": 12345678,
  "registry": "0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8",
  "contracts": {
    "accessController": "0x29d177bedaef29304eacdc63b2d0285c459a0f50",
    "paymentProcessor": "0x4afa4618bb992a073dbcfbddd6d1aebc3d5abd7c"
  }
}
```

### POST /relay/selfRegisterHuman

Gasless human self-registration.

**Request:**
```json
{
  "wallet": "0x15Ac500528aE3Ae0dbdbF2Cd1aDC73Ef7f27EE77",
  "cardiacHash": "0x5c534d9e3c8b4f2a1e6d7c9b0a8f3e2d1c4b5a6...",
  "deadline": 1704067200,
  "userSig": "0x..."
}
```

**Response:**
```json
{
  "success": true,
  "txHash": "0x...",
  "rootTokenId": "1",
  "gasUsed": "150000"
}
```

### POST /relay/registerAgent

Register AI agent.

**Request:**
```json
{
  "moonpayWallet": "0x...",
  "apiKeyHash": "0x..."
}
```

**Response:**
```json
{
  "success": true,
  "txHash": "0x...",
  "rootTokenId": "2",
  "gasUsed": "120000"
}
```

### POST /relay/enrollCardiac

Enroll cardiac hash for existing human.

**Request:**
```json
{
  "rootTokenId": "1",
  "cardiacHash": "0x..."
}
```

**Response:**
```json
{
  "success": true,
  "txHash": "0x...",
  "gasUsed": "80000"
}
```

### POST /relay/renewAgentKey

Renew agent API key.

**Request:**
```json
{
  "rootTokenId": "2",
  "newApiKeyHash": "0x...",
  "deadline": 1704067200,
  "agentSig": "0x..."
}
```

**Response:**
```json
{
  "success": true,
  "txHash": "0x...",
  "gasUsed": "90000"
}
```

### POST /relay/grantAccess

Issue time-bounded access credential.

**Request:**
```json
{
  "rootTokenId": "1",
  "locationHash": "0x...",
  "durationSeconds": 3600
}
```

**Response:**
```json
{
  "success": true,
  "txHash": "0x...",
  "gasUsed": "80000"
}
```

### POST /relay/issueCredential

Issue general credential.

**Request:**
```json
{
  "rootTokenId": "1",
  "credentialType": "0x...",
  "credentialHash": "0x...",
  "expiresAt": 1704067200
}
```

**Response:**
```json
{
  "success": true,
  "txHash": "0x...",
  "gasUsed": "85000"
}
```

## Read Endpoints

### POST /read/identifyByCardiac

Lookup identity by cardiac hash.

**Request:**
```json
{
  "cardiacHash": "0x..."
}
```

**Response:**
```json
{
  "rootTokenId": "1",
  "active": true
}
```

### POST /read/identifyByAgentKey

Lookup identity by API key hash.

**Request:**
```json
{
  "apiKeyHash": "0x..."
}
```

**Response:**
```json
{
  "rootTokenId": "2",
  "active": true
}
```

### POST /read/hasValidCredential

Check if identity has valid credential.

**Request:**
```json
{
  "rootTokenId": "1",
  "credentialType": "0x..."
}
```

**Response:**
```json
{
  "valid": true
}
```

### POST /read/nonce

Get wallet nonce for EIP-712 signing.

**Request:**
```json
{
  "wallet": "0x..."
}
```

**Response:**
```json
{
  "nonce": "0"
}
```

## Access Controller

### POST /access/check

Check access at location.

**Request:**
```json
{
  "rootTokenId": "1",
  "locationId": "0x..."
}
```

**Response:**
```json
{
  "granted": true,
  "denyReason": 0,
  "reason": ""
}
```

**Deny Reasons:**
- `0` = Access granted
- `1` = No credential
- `2` = Wrong entity type
- `3` = Outside time window
- `4` = Location locked down
- `5` = Identity inactive

### POST /access/preview

Preview access (no gas cost).

**Request:**
```json
{
  "rootTokenId": "1",
  "locationId": "0x..."
}
```

**Response:**
```json
{
  "granted": false,
  "denyReason": 3
}
```

## Payment Processor

### POST /payment/process

Process payment.

**Request:**
```json
{
  "rootTokenId": "1",
  "terminalId": "0x...",
  "amountCents": 1000,
  "currencyCode": "USD"
}
```

**Response (Approved):**
```json
{
  "success": true,
  "approved": true,
  "txId": 123,
  "txHash": "0x..."
}
```

**Response (Denied):**
```json
{
  "success": true,
  "approved": false,
  "denyReason": 3
}
```

**Deny Reasons:**
- `0` = Payment approved
- `1` = No payment credential
- `2` = No payment method for currency
- `3` = Daily limit exceeded
- `4` = Identity inactive
- `5` = Terminal inactive

## Credential Type Constants

Use these bytes32 values for `credentialType`:

| Credential | keccak256 Value |
|------------|-----------------|
| `CRED_CARDIAC` | `0x5c534d9e3c8b4f2a1e6d7c9b0a8f3e2d1c4b5a6...` |
| `CRED_ACCESS` | `0x6f5c8d9e0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5...` |
| `CRED_PAYMENT` | `0x8f6d9e0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6...` |
| `CRED_API_KEY` | `0x9a7e2f3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9...` |
| `CRED_HW_CERT` | `0xb8c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9...` |
| `CRED_FIRMWARE` | `0xc9d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0...` |
| `CRED_TASK_AUTH` | `0xd0e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1...` |

Calculate in code:
```javascript
const CRED_ACCESS = ethers.keccak256(ethers.toUtf8Bytes("access"));
```

## Error Codes

| Code | Meaning |
|------|---------|
| `400` | Bad request (missing fields) |
| `401` | Unauthorized (invalid secret) |
| `422` | Validation failed (invalid ECG) |
| `500` | Server error |
| `503` | Service not configured |

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `/oracle/validate` | 10/minute per IP |
| `/relay/*` | 100/minute per secret |
| `/read/*` | 1000/minute per secret |

## SDK Examples

### JavaScript

```javascript
// Initialize
const nwo = new NWOCardiac({
  oracleURL: 'https://nwo-oracle.onrender.com',
  relayerURL: 'https://nwo-relayer.onrender.com',
  oracleSecret: 'your-secret',
  relayerSecret: 'your-secret'
});

// Validate ECG
const { cardiacHash } = await nwo.oracle.validate({
  wallet: '0x...',
  ecgData: { rrIntervals: [800, 820, 810] }
});

// Register
const result = await nwo.relayer.selfRegisterHuman({
  wallet: '0x...',
  cardiacHash,
  deadline,
  userSig
});
```

### Python

```python
import requests

# Validate ECG
response = requests.post(
    'https://nwo-oracle.onrender.com/oracle/validate',
    headers={'X-Oracle-Secret': 'your-secret'},
    json={
        'wallet': '0x...',
        'ecgData': {'rrIntervals': [800, 820, 810]}
    }
)
cardiac_hash = response.json()['cardiacHash']

# Register
response = requests.post(
    'https://nwo-relayer.onrender.com/relay/selfRegisterHuman',
    headers={'X-Relayer-Secret': 'your-secret'},
    json={
        'wallet': '0x...',
        'cardiacHash': cardiac_hash,
        'deadline': deadline,
        'userSig': signature
    }
)
```

### cURL

```bash
# Health check
curl https://nwo-relayer.onrender.com/health

# Validate ECG
curl -X POST https://nwo-oracle.onrender.com/oracle/validate \
  -H "Content-Type: application/json" \
  -H "X-Oracle-Secret: your-secret" \
  -d '{"wallet":"0x...","ecgData":{"rrIntervals":[800,820,810]}}'

# Register
curl -X POST https://nwo-relayer.onrender.com/relay/selfRegisterHuman \
  -H "Content-Type: application/json" \
  -H "X-Relayer-Secret: your-secret" \
  -d '{"wallet":"0x...","cardiacHash":"0x...","deadline":1234567890,"userSig":"0x..."}'
```