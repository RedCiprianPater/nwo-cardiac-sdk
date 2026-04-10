# NWO Robotics Integration

Complete guide for integrating NWO Digital ID with the NWO Robotics API for autonomous agent authentication and task authorization.

## Overview

The NWO Cardiac Digital ID system integrates seamlessly with **NWO Robotics** (`nworobotics.cloud`), enabling:

- **Agent Authentication** — AI agents prove identity via Digital ID
- **Task Authorization** — Humans authorize robot tasks with biometric credentials
- **Swarm Coordination** — Command multiple robots with single identity
- **Autonomous Operations** — Robots verify permissions without human intervention

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         NWO ROBOTICS INTEGRATION                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────┐ │
│  │    Human     │────▶│   NWO Cardiac │────▶│     NWO Robotics        │ │
│  │   (Owner)    │     │   Digital ID  │     │       API               │ │
│  └──────────────┘     └──────────────┘     └──────────────────────────┘ │
│         │                      │                      │                  │
│         │                      │                      │                  │
│         │              ┌───────┴───────┐              │                  │
│         │              │               │              │                  │
│         ▼              ▼               ▼              ▼                  │
│  ┌──────────────┐ ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │  Watch ECG   │ │  Oracle  │  │ Relayer  │  │    Robot Fleet       │  │
│  │   Scan       │ │ Service  │  │ Service  │  │                      │  │
│  └──────────────┘ └──────────┘  └──────────┘  │  ┌────┐ ┌────┐      │  │
│                                               │  │ R1 │ │ R2 │ ...  │  │
│                                               │  └────┘ └────┘      │  │
│                                               └──────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Authentication Flows

### 1. Agent Registration

AI agents (MoonPay wallets) register as Digital ID holders:

```javascript
// Agent registers with MoonPay wallet
const agent = await nwo.registerAgent({
  moonpayWallet: agentAddress,
  apiKeyHash: keccak256(apiKey)
});

// Agent receives rootTokenId and API key credential
console.log(`Agent registered: Token ID ${agent.rootTokenId}`);
```

### 2. Task Authorization

Human authorizes robot to perform task:

```javascript
// Human issues task authorization credential
const auth = await nwo.issueCredential({
  rootTokenId: humanTokenId,
  credentialType: 'CRED_TASK_AUTH',
  credentialHash: keccak256(taskId),
  expiresAt: Date.now() / 1000 + 3600 // 1 hour
});

// Robot verifies before executing
const canExecute = await nwoRobotics.verifyTaskAuth(agentWallet, taskId);
```

### 3. Swarm Command

Human commands multiple robots:

```javascript
// Issue swarm command credential
const swarmAuth = await nwo.issueCredential({
  rootTokenId: humanTokenId,
  credentialType: 'CRED_SWARM_CMD',
  credentialHash: keccak256(swarmCommandId),
  expiresAt: Date.now() / 1000 + 300 // 5 minutes
});

// All robots in swarm verify and execute
const results = await nwoRobotics.executeSwarm(swarmCommandId, robots);
```

## API Integration

### Initialize SDK

```javascript
import { NWOCardiac } from '@nwo/cardiac-sdk';
import { NWORobotics } from '@nwo/robotics-sdk';

// Cardiac SDK
const cardiac = new NWOCardiac({
  oracleURL: 'https://nwo-oracle.onrender.com',
  relayerURL: 'https://nwo-relayer.onrender.com',
  registryAddress: '0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8',
  chainId: 8453
});

// Robotics SDK
const robotics = new NWORobotics({
  apiURL: 'https://api.nworobotics.cloud',
  apiKey: 'your-robotics-api-key'
});
```

### Human Authorizes Robot Task

```javascript
// 1. Human captures ECG (from watch)
const ecgData = await watch.captureECG();

// 2. Verify identity
const identity = await cardiac.identifyByECG(ecgData);

// 3. Create task specification
const task = {
  id: uuid(),
  type: 'pick_and_place',
  robotId: 'robot-001',
  location: { x: 10, y: 20, z: 0 },
  object: 'box-A',
  deadline: Date.now() + 300000 // 5 minutes
};

// 4. Issue task authorization credential
const taskAuth = await cardiac.issueCredential({
  rootTokenId: identity.rootTokenId,
  credentialType: CRED_TASK_AUTH,
  credentialHash: keccak256(task.id),
  expiresAt: task.deadline / 1000
});

// 5. Submit to Robotics API
const job = await robotics.submitTask({
  task,
  humanTokenId: identity.rootTokenId,
  credentialProof: taskAuth.proof
});

console.log(`Task submitted: ${job.id}`);
```

### Robot Verifies & Executes

```javascript
// Robot receives task
const task = await robotics.getPendingTask(robotId);

// Verify human authorization
const isAuthorized = await cardiac.verifyCredential({
  rootTokenId: task.humanTokenId,
  credentialType: CRED_TASK_AUTH,
  credentialHash: keccak256(task.id)
});

if (isAuthorized) {
  // Execute task
  await robot.execute(task);
  
  // Report completion
  await robotics.reportCompletion(task.id, {
    status: 'success',
    duration: 120,
    robotId
  });
} else {
  await robotics.reportFailure(task.id, 'unauthorized');
}
```

### Autonomous Agent with Delegation

```javascript
// Human delegates authority to AI agent
const delegation = await cardiac.issueCredential({
  rootTokenId: humanTokenId,
  credentialType: CRED_CAPABILITY,
  credentialHash: keccak256('inventory_management'),
  expiresAt: Date.now() / 1000 + 86400 // 24 hours
});

// Agent operates autonomously within scope
const agent = new AutonomousAgent({
  humanTokenId,
  capabilities: ['inventory_management'],
  robotics
});

// Agent makes decisions and executes tasks
await agent.run();
```

## Credential Types for Robotics

| Credential | Purpose | Duration |
|------------|---------|----------|
| `CRED_TASK_AUTH` | Single task authorization | Task-specific |
| `CRED_CAPABILITY` | Ongoing capability | 1-24 hours |
| `CRED_SWARM_CMD` | Swarm command | 5-30 minutes |
| `CRED_EMERGENCY` | Emergency override | 10 minutes |
| `CRED_MAINTENANCE` | Maintenance access | Scheduled window |

## Use Cases

### 1. Warehouse Automation

```javascript
// Warehouse worker authorizes picking robot
const pickTask = await authorizeTask({
  robot: 'picker-01',
  action: 'pick',
  items: ['SKU-123', 'SKU-456'],
  destination: 'packing-station-A'
});

// Robot verifies and executes
await robot.execute(pickTask);
```

### 2. Drone Delivery

```javascript
// Customer authorizes drone delivery
const delivery = await authorizeTask({
  drone: 'drone-07',
  action: 'deliver',
  package: 'PKG-789',
  destination: customerLocation,
  signature: 'required'
});

// Drone verifies customer identity on arrival
const customerECG = await drone.scanCustomer();
const isRecipient = await cardiac.identifyByECG(customerECG);

if (isRecipient.rootTokenId === delivery.recipientId) {
  await drone.releasePackage();
}
```

### 3. Autonomous Security Patrol

```javascript
// Security guard authorizes patrol
const patrol = await authorizeCapability({
  robots: ['patrol-01', 'patrol-02'],
  capability: 'security_patrol',
  area: 'warehouse-district-3',
  shift: 'night'
});

// Robots patrol autonomously
await robotics.startPatrol(patrol);
```

### 4. Emergency Response

```javascript
// Emergency override for first responders
const emergency = await issueEmergencyCredential({
  responderTokenId: firstResponderId,
  scope: 'all_robots_in_building',
  action: 'evacuate_assist',
  duration: 600 // 10 minutes
});

// All robots respond to emergency
await robotics.executeEmergency(emergency);
```

## Security Model

### Trust Levels

| Component | Trust | Responsibility |
|-----------|-------|----------------|
| Human | Ultimate | Owns identity, authorizes tasks |
| Digital ID | High | Verifies human, issues credentials |
| Robotics API | Medium | Routes tasks, manages fleet |
| Robot | Low | Executes verified tasks only |

### Verification Chain

```
Robot verifies:
1. Task signature (cryptographic)
2. Credential validity (on-chain)
3. Human identity (Digital ID)
4. Authorization scope (capability check)
5. Time window (expiration)
```

### Safety Mechanisms

1. **Emergency Stop** — Human can halt all robots instantly
2. **Capability Limits** — Agents can't exceed authorized scope
3. **Audit Logs** — All actions recorded on-chain
4. **Rate Limiting** — Prevents spam/abuse
5. **Revocation** — Credentials can be revoked instantly

## Backend Integration

### PHP Example

```php
<?php
// NWO Robotics integration

class NWORoboticsController {
    private $cardiacSDK;
    private $roboticsAPI;
    
    public function __construct() {
        $this->cardiacSDK = new NWOCardiacSDK([
            'oracle_url' => 'https://nwo-oracle.onrender.com',
            'relayer_url' => 'https://nwo-relayer.onrender.com',
            'relayer_secret' => $_ENV['NWO_RELAYER_SECRET']
        ]);
        
        $this->roboticsAPI = new NWORoboticsAPI([
            'api_url' => 'https://api.nworobotics.cloud',
            'api_key' => $_ENV['NWO_ROBOTICS_API_KEY']
        ]);
    }
    
    public function submitTask(Request $request) {
        // Verify human identity
        $identity = $this->cardiacSDK->identifyByCardiac(
            $request->input('cardiac_hash')
        );
        
        if (!$identity['active']) {
            return response()->json(['error' => 'Identity not active'], 403);
        }
        
        // Issue task authorization
        $credential = $this->cardiacSDK->issueCredential([
            'rootTokenId' => $identity['rootTokenId'],
            'credentialType' => 'CRED_TASK_AUTH',
            'credentialHash' => hash('sha256', $request->input('task_id')),
            'expiresAt' => time() + 3600
        ]);
        
        // Submit to robotics API
        $job = $this->roboticsAPI->submitTask([
            'task' => $request->input('task'),
            'humanTokenId' => $identity['rootTokenId'],
            'credentialProof' => $credential['proof']
        ]);
        
        return response()->json([
            'job_id' => $job['id'],
            'status' => 'submitted'
        ]);
    }
}
```

### Node.js Example

```javascript
// Express middleware for robotics auth
const { NWOCardiac } = require('@nwo/cardiac-sdk');
const { NWORobotics } = require('@nwo/robotics-sdk');

const cardiac = new NWOCardiac(config);
const robotics = new NWORobotics(config);

// Middleware to verify robot task authorization
async function verifyTaskAuth(req, res, next) {
  const { taskId, robotId, credentialProof } = req.body;
  
  // Verify credential on-chain
  const isValid = await cardiac.verifyCredential({
    rootTokenId: credentialProof.humanTokenId,
    credentialType: 'CRED_TASK_AUTH',
    credentialHash: keccak256(taskId)
  });
  
  if (!isValid) {
    return res.status(403).json({ error: 'Unauthorized' });
  }
  
  // Check robot is assigned to task
  const task = await robotics.getTask(taskId);
  if (task.robotId !== robotId) {
    return res.status(403).json({ error: 'Robot not assigned' });
  }
  
  req.task = task;
  next();
}

// Robot reports task completion
app.post('/robot/task/complete', verifyTaskAuth, async (req, res) => {
  const { taskId, result } = req.body;
  
  await robotics.reportCompletion(taskId, result);
  
  res.json({ status: 'recorded' });
});
```

## Testing

### Test Credentials

```javascript
// Test task authorization
const testAuth = await cardiac.issueCredential({
  rootTokenId: '123',
  credentialType: 'CRED_TASK_AUTH',
  credentialHash: keccak256('test-task-001'),
  expiresAt: Date.now() / 1000 + 3600
});

// Verify
const isValid = await cardiac.verifyCredential({
  rootTokenId: '123',
  credentialType: 'CRED_TASK_AUTH',
  credentialHash: keccak256('test-task-001')
});

console.log('Credential valid:', isValid);
```

### Integration Tests

```javascript
describe('NWO Robotics Integration', () => {
  test('human can authorize robot task', async () => {
    const human = await createTestIdentity();
    const robot = await createTestRobot();
    
    const task = await authorizeTask(human, robot);
    
    expect(task.authorized).toBe(true);
    expect(await verifyOnChain(task.proof)).toBe(true);
  });
  
  test('robot verifies before execution', async () => {
    const task = await createTestTask();
    
    const verified = await robot.verifyTask(task);
    
    expect(verified).toBe(true);
  });
  
  test('expired credentials rejected', async () => {
    const expiredAuth = await createExpiredCredential();
    
    const result = await robot.verifyTask({ credential: expiredAuth });
    
    expect(result).toBe(false);
  });
});
```

## Resources

- [NWO Robotics API Docs](https://nworobotics.cloud/docs)
- [NWO Cardiac SDK](./README.md)
- [Base Mainnet Explorer](https://basescan.org)
- [Smart Contract Source](https://github.com/RedCiprianPater/nwo-identity-services)

## Support

- **Discord:** [NWO Robotics](https://discord.gg/nwo-robotics)
- **Email:** robotics-support@nwo.capital
- **GitHub:** [Issues](https://github.com/RedCiprianPater/nwo-cardiac-sdk/issues)

---

Integrate. Automate. Verify.