# Smart Watch Integration Guide

Complete guide for integrating NWO Digital ID with Apple Watch, Wear OS, and other smart watch platforms.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Apple Watch (Swift)](#apple-watch-swift)
3. [Wear OS (Kotlin)](#wear-os-kotlin)
4. [API Reference](#api-reference)
5. [Security Best Practices](#security-best-practices)
6. [Testing & Certification](#testing--certification)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     SMART WATCH APP                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  ECG Capture │  │  API Client  │  │  Wallet/Signing      │  │
│  │              │  │              │  │                      │  │
│  │ • HealthKit  │  │ • Oracle     │  │ • Secure Enclave     │  │
│  │ • Sensors    │  │ • Relayer    │  │ • Keychain           │  │
│  │ • Processing │  │ • Polling    │  │ • Biometric Auth     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                  │                      │              │
│         └──────────────────┼──────────────────────┘              │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     NWO SERVICES                                 │
│         Oracle: https://nwo-oracle.onrender.com                 │
│        Relayer: https://nwo-relayer.onrender.com                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Apple Watch (Swift)

### Prerequisites

- Xcode 15+
- watchOS 10+
- iOS 17+ (companion app)
- Apple Watch Series 4+ (ECG capable)

### Project Setup

#### 1. Create Watch App

```bash
# In Xcode: File → New → Project → watchOS → App
# Enable: Include Notification Scene
```

#### 2. Add Capabilities

In your WatchKit Extension:
- **HealthKit** — ECG access
- **App Groups** — Share data with iPhone
- **Keychain Sharing** — Secure key storage

#### 3. Info.plist

```xml
<key>NSHealthShareUsageDescription</key>
<string>NWO Digital ID uses your ECG to create a secure biometric identity.</string>

<key>NSHealthUpdateUsageDescription</key>
<string>NWO Digital ID uses your ECG to create a secure biometric identity.</string>
```

### Implementation

#### ECGManager.swift

```swift
import HealthKit
import Combine

class ECGManager: NSObject, ObservableObject {
    private let healthStore = HKHealthStore()
    
    @Published var isAuthorized = false
    @Published var isCapturing = false
    @Published var lastECG: ECGData?
    @Published var error: Error?
    
    // MARK: - Authorization
    
    func requestAuthorization() async throws {
        guard let ecgType = HKObjectType.electrocardiogramType() else {
            throw ECGError.notAvailable
        }
        
        try await healthStore.requestAuthorization(toShare: [], read: [ecgType])
        isAuthorized = true
    }
    
    // MARK: - ECG Capture
    
    func captureECG() async throws -> ECGData {
        isCapturing = true
        defer { isCapturing = false }
        
        // Get latest ECG from HealthKit
        guard let ecg = try await fetchLatestECG() else {
            throw ECGError.noData
        }
        
        // Extract voltage measurements
        let samples = try await extractVoltageMeasurements(from: ecg)
        
        // Calculate RR intervals
        let rrIntervals = calculateRRIntervals(from: samples)
        
        let ecgData = ECGData(
            samples: samples,
            rrIntervals: rrIntervals,
            sampleRate: 512.0,
            deviceType: "apple_watch",
            timestamp: Date()
        )
        
        lastECG = ecgData
        return ecgData
    }
    
    private func fetchLatestECG() async throws -> HKElectrocardiogram? {
        guard let ecgType = HKObjectType.electrocardiogramType() else {
            return nil
        }
        
        return try await withCheckedThrowingContinuation { continuation in
            let query = HKSampleQuery(
                sampleType: ecgType,
                predicate: nil,
                limit: 1,
                sortDescriptors: [NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)]
            ) { _, samples, error in
                if let error = error {
                    continuation.resume(throwing: error)
                } else {
                    continuation.resume(returning: samples?.first as? HKElectrocardiogram)
                }
            }
            
            healthStore.execute(query)
        }
    }
    
    private func extractVoltageMeasurements(from ecg: HKElectrocardiogram) async throws -> [Double] {
        var measurements: [Double] = []
        
        return try await withCheckedThrowingContinuation { continuation in
            let query = HKElectrocardiogramQuery(ecg) { query, result in
                switch result {
                case .measurement(let measurement):
                    if let voltage = measurement.quantity(for: .appleWatchAnalogVoltage) {
                        let value = voltage.doubleValue(for: .volt())
                        measurements.append(value)
                    }
                    
                case .done:
                    continuation.resume(returning: measurements)
                    
                case .error(let error):
                    continuation.resume(throwing: error)
                }
            }
            
            self.healthStore.execute(query)
        }
    }
    
    private func calculateRRIntervals(from samples: [Double]) -> [Double] {
        // Peak detection algorithm
        let peaks = detectRPeaks(in: samples, sampleRate: 512.0)
        
        var intervals: [Double] = []
        for i in 1..<peaks.count {
            let interval = (peaks[i] - peaks[i-1]) / 512.0 * 1000.0 // Convert to ms
            intervals.append(interval)
        }
        
        return intervals
    }
    
    private func detectRPeaks(in samples: [Double], sampleRate: Double) -> [Int] {
        // Simplified Pan-Tompkins algorithm
        // In production, use a proper implementation
        var peaks: [Int] = []
        let threshold = 0.5 // Adjust based on signal
        
        for i in 1..<samples.count-1 {
            if samples[i] > threshold &&
               samples[i] > samples[i-1] &&
               samples[i] > samples[i+1] {
                peaks.append(i)
            }
        }
        
        return peaks
    }
}

// MARK: - Data Models

struct ECGData: Codable {
    let samples: [Double]
    let rrIntervals: [Double]
    let sampleRate: Double
    let deviceType: String
    let timestamp: Date
}

enum ECGError: Error {
    case notAvailable
    case notAuthorized
    case noData
    case invalidSignal
}
```

#### NWOAPIClient.swift

```swift
import Foundation
import CryptoKit

class NWOAPIClient {
    static let shared = NWOAPIClient()
    
    private let oracleURL = "https://nwo-oracle.onrender.com"
    private let relayerURL = "https://nwo-relayer.onrender.com"
    
    private var oracleSecret: String {
        // Load from secure storage
        return KeychainManager.shared.oracleSecret
    }
    
    private var relayerSecret: String {
        return KeychainManager.shared.relayerSecret
    }
    
    // MARK: - Oracle
    
    func validateECG(wallet: String, ecgData: ECGData) async throws -> OracleResponse {
        let url = URL(string: "\(oracleURL)/oracle/validate")!
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(oracleSecret, forHTTPHeaderField: "X-Oracle-Secret")
        
        let body = OracleValidateRequest(
            wallet: wallet,
            ecgData: ECGDataPayload(
                samples: Array(ecgData.samples.prefix(100)), // Limit samples
                rrIntervals: ecgData.rrIntervals,
                sampleRate: ecgData.sampleRate,
                deviceType: ecgData.deviceType
            )
        )
        
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.validationFailed
        }
        
        return try JSONDecoder().decode(OracleResponse.self, from: data)
    }
    
    // MARK: - Relayer
    
    func selfRegisterHuman(
        wallet: String,
        cardiacHash: String,
        signature: String,
        deadline: Int
    ) async throws -> RegistrationResponse {
        let url = URL(string: "\(relayerURL)/relay/selfRegisterHuman")!
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(relayerSecret, forHTTPHeaderField: "X-Relayer-Secret")
        
        let body = SelfRegisterRequest(
            wallet: wallet,
            cardiacHash: cardiacHash,
            deadline: deadline,
            userSig: signature
        )
        
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.registrationFailed
        }
        
        return try JSONDecoder().decode(RegistrationResponse.self, from: data)
    }
    
    func identifyByCardiac(cardiacHash: String) async throws -> IdentityResponse {
        let url = URL(string: "\(relayerURL)/read/identifyByCardiac")!
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(relayerSecret, forHTTPHeaderField: "X-Relayer-Secret")
        
        let body = ["cardiacHash": cardiacHash]
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(IdentityResponse.self, from: data)
    }
}

// MARK: - Request/Response Models

struct OracleValidateRequest: Codable {
    let wallet: String
    let ecgData: ECGDataPayload
}

struct ECGDataPayload: Codable {
    let samples: [Double]?
    let rrIntervals: [Double]?
    let sampleRate: Double?
    let deviceType: String?
}

struct OracleResponse: Codable {
    let valid: Bool
    let cardiacHash: String
    let confidence: Double
    let features: ECGFeatures
    let expiresAt: Int
}

struct ECGFeatures: Codable {
    let meanRR: Int
    let sdnn: Double
    let rmssd: Double
    let heartRate: Int
    let morphologyScore: Double
}

struct SelfRegisterRequest: Codable {
    let wallet: String
    let cardiacHash: String
    let deadline: Int
    let userSig: String
}

struct RegistrationResponse: Codable {
    let success: Bool
    let txHash: String
    let rootTokenId: String
    let gasUsed: String
}

struct IdentityResponse: Codable {
    let rootTokenId: String
    let active: Bool
}

enum APIError: Error {
    case validationFailed
    case registrationFailed
    case networkError
}
```

#### WalletManager.swift

```swift
import Foundation
import CryptoKit

class WalletManager: ObservableObject {
    @Published var walletAddress: String?
    @Published var isAuthenticated = false
    
    private let registryAddress = "0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8"
    private let chainId = 8453
    
    // MARK: - EIP-712 Signing
    
    func signSelfRegister(
        wallet: String,
        cardiacHash: String,
        nonce: Int
    ) async throws -> (signature: String, deadline: Int) {
        let deadline = Int(Date().timeIntervalSince1970) + 600 // 10 minutes
        
        let domain = EIP712Domain(
            name: "NWOIdentityRegistry",
            version: "1",
            chainId: chainId,
            verifyingContract: registryAddress
        )
        
        let message = SelfRegisterMessage(
            wallet: wallet,
            cardiacHash: cardiacHash,
            nonce: nonce,
            deadline: deadline
        )
        
        // Sign with secure enclave
        let signature = try await signTypedData(domain: domain, message: message)
        
        return (signature, deadline)
    }
    
    private func signTypedData(domain: EIP712Domain, message: SelfRegisterMessage) async throws -> String {
        // Implementation depends on your wallet setup
        // Could be: Secure Enclave, WalletConnect, or embedded key
        
        // Example with embedded key (not recommended for production):
        // let privateKey = try loadPrivateKey()
        // return try privateKey.sign(hash: hashTypedData(domain, message))
        
        throw WalletError.notImplemented
    }
}

struct EIP712Domain: Codable {
    let name: String
    let version: String
    let chainId: Int
    let verifyingContract: String
}

struct SelfRegisterMessage: Codable {
    let wallet: String
    let cardiacHash: String
    let nonce: Int
    let deadline: Int
}

enum WalletError: Error {
    case notImplemented
    case keyNotFound
    case signingFailed
}
```

#### ContentView.swift

```swift
import SwiftUI

struct ContentView: View {
    @StateObject private var ecgManager = ECGManager()
    @StateObject private var apiClient = NWOAPIClient.shared
    @StateObject private var walletManager = WalletManager()
    
    @State private var walletAddress = ""
    @State private var isRegistering = false
    @State private var registrationResult: String?
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Header
                Text("NWO Digital ID")
                    .font(.largeTitle)
                    .bold()
                
                Text("Biometric Identity on Base")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                // Wallet Input
                TextField("Wallet Address", text: $walletAddress)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding(.horizontal)
                
                // Status
                if ecgManager.isCapturing {
                    ProgressView("Capturing ECG...")
                }
                
                if let error = errorMessage {
                    Text(error)
                        .foregroundColor(.red)
                        .font(.caption)
                }
                
                if let result = registrationResult {
                    Text(result)
                        .foregroundColor(.green)
                        .font(.caption)
                }
                
                Spacer()
                
                // Actions
                VStack(spacing: 10) {
                    Button("Authorize HealthKit") {
                        Task {
                            try? await ecgManager.requestAuthorization()
                        }
                    }
                    .disabled(ecgManager.isAuthorized)
                    
                    Button("Register Identity") {
                        Task {
                            await registerIdentity()
                        }
                    }
                    .disabled(!ecgManager.isAuthorized || walletAddress.isEmpty || isRegistering)
                    
                    Button("Check Identity") {
                        Task {
                            await checkIdentity()
                        }
                    }
                    .disabled(walletAddress.isEmpty)
                }
                .buttonStyle(.borderedProminent)
            }
            .padding()
            .navigationTitle("NWO Cardiac")
        }
    }
    
    private func registerIdentity() async {
        isRegistering = true
        errorMessage = nil
        registrationResult = nil
        
        do {
            // 1. Capture ECG
            let ecgData = try await ecgManager.captureECG()
            
            // 2. Validate with Oracle
            let oracleResponse = try await apiClient.validateECG(
                wallet: walletAddress,
                ecgData: ecgData
            )
            
            guard oracleResponse.valid else {
                throw RegistrationError.invalidECG
            }
            
            // 3. Sign message
            let (signature, deadline) = try await walletManager.signSelfRegister(
                wallet: walletAddress,
                cardiacHash: oracleResponse.cardiacHash,
                nonce: 0 // Fetch from contract
            )
            
            // 4. Submit to Relayer
            let registration = try await apiClient.selfRegisterHuman(
                wallet: walletAddress,
                cardiacHash: oracleResponse.cardiacHash,
                signature: signature,
                deadline: deadline
            )
            
            registrationResult = "Success! Token ID: \(registration.rootTokenId)"
            
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isRegistering = false
    }
    
    private func checkIdentity() async {
        // Implementation for checking existing identity
    }
}

enum RegistrationError: Error {
    case invalidECG
}
```

---

## Wear OS (Kotlin)

### Prerequisites

- Android Studio Hedgehog+
- Wear OS 4+
- Android 14+ (companion app)
- Watch with heart rate sensor

### Project Setup

#### 1. Create Wear OS App

```bash
# In Android Studio: File → New → New Project → Wear OS → Empty Activity
```

#### 2. Add Dependencies

```kotlin
// build.gradle.kts (app level)
dependencies {
    // Health Services
    implementation("androidx.health.services:health-services-client:1.0.0-rc01")
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.7.3")
    
    // Retrofit for API calls
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    
    // Web3j for Ethereum
    implementation("org.web3j:core:4.10.0")
    
    // Security
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
}
```

#### 3. Permissions

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.BODY_SENSORS" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

<uses-feature android:name="android.hardware.type.watch" />
```

### Implementation

#### ECGManager.kt

```kotlin
import android.content.Context
import androidx.health.services.client.HealthServices
import androidx.health.services.client.data.DataType
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.tasks.await

class ECGManager(private val context: Context) {
    private val healthClient = HealthServices.getClient(context)
    private val measureClient = healthClient.measureClient
    
    suspend fun hasECGSensor(): Boolean {
        val capabilities = measureClient.getCapabilitiesAsync().await()
        return capabilities.supportedDataTypes.contains(DataType.HEART_RATE_BPM)
    }
    
    fun heartRateFlow(): Flow<Int> = callbackFlow {
        val callback = object : MeasureCallback {
            override fun onDataReceived(data: DataPointContainer) {
                val heartRate = data.getData(DataType.HEART_RATE_BPM)
                trySend(heartRate.toInt())
            }
        }
        
        measureClient.registerMeasureCallback(DataType.HEART_RATE_BPM, callback)
        
        awaitClose {
            measureClient.unregisterMeasureCallback(DataType.HEART_RATE_BPM, callback)
        }
    }
    
    suspend fun captureECG(durationMs: Long = 30000): ECGData {
        val samples = mutableListOf<Double>()
        val rrIntervals = mutableListOf<Double>()
        
        // Collect heart rate data
        heartRateFlow().collect { hr ->
            // Convert HR to RR interval
            val rr = 60000.0 / hr
            rrIntervals.add(rr)
            
            if (rrIntervals.size >= 10) { // Collect 10 beats
                close()
            }
        }
        
        return ECGData(
            samples = samples,
            rrIntervals = rrIntervals,
            sampleRate = 512.0,
            deviceType = "wear_os",
            timestamp = System.currentTimeMillis()
        )
    }
}

data class ECGData(
    val samples: List<Double>,
    val rrIntervals: List<Double>,
    val sampleRate: Double,
    val deviceType: String,
    val timestamp: Long
)
```

#### NWOApiService.kt

```kotlin
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

interface NWOApiService {
    @POST("/oracle/validate")
    suspend fun validateECG(
        @Header("X-Oracle-Secret") secret: String,
        @Body request: OracleValidateRequest
    ): Response<OracleResponse>
    
    @POST("/relay/selfRegisterHuman")
    suspend fun selfRegisterHuman(
        @Header("X-Relayer-Secret") secret: String,
        @Body request: SelfRegisterRequest
    ): Response<RegistrationResponse>
    
    @POST("/read/identifyByCardiac")
    suspend fun identifyByCardiac(
        @Header("X-Relayer-Secret") secret: String,
        @Body request: IdentifyRequest
    ): Response<IdentityResponse>
}

data class OracleValidateRequest(
    val wallet: String,
    val ecgData: ECGDataPayload
)

data class ECGDataPayload(
    val samples: List<Double>?,
    val rrIntervals: List<Double>?,
    val sampleRate: Double?,
    val deviceType: String?
)

data class OracleResponse(
    val valid: Boolean,
    val cardiacHash: String,
    val confidence: Double,
    val features: ECGFeatures,
    val expiresAt: Long
)

data class ECGFeatures(
    val meanRR: Int,
    val sdnn: Double,
    val rmssd: Double,
    val heartRate: Int,
    val morphologyScore: Double
)

data class SelfRegisterRequest(
    val wallet: String,
    val cardiacHash: String,
    val deadline: Long,
    val userSig: String
)

data class RegistrationResponse(
    val success: Boolean,
    val txHash: String,
    val rootTokenId: String,
    val gasUsed: String
)

data class IdentifyRequest(
    val cardiacHash: String
)

data class IdentityResponse(
    val rootTokenId: String,
    val active: Boolean
)

class NWOApiClient {
    private val oracleRetrofit = Retrofit.Builder()
        .baseUrl("https://nwo-oracle.onrender.com")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    private val relayerRetrofit = Retrofit.Builder()
        .baseUrl("https://nwo-relayer.onrender.com")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val oracleService: NWOApiService = oracleRetrofit.create(NWOApiService::class.java)
    val relayerService: NWOApiService = relayerRetrofit.create(NWOApiService::class.java)
}
```

#### MainActivity.kt

```kotlin
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.lifecycleScope
import androidx.wear.compose.material.MaterialTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private lateinit var ecgManager: ECGManager
    private val apiClient = NWOApiClient()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        ecgManager = ECGManager(this)
        
        setContent {
            MaterialTheme {
                NWOApp()
            }
        }
    }
    
    @Composable
    fun NWOApp() {
        var walletAddress by remember { mutableStateOf("") }
        var isLoading by remember { mutableStateOf(false) }
        var result by remember { mutableStateOf<String?>(null) }
        var error by remember { mutableStateOf<String?>(null) }
        
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "NWO Digital ID",
                style = MaterialTheme.typography.titleLarge
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            OutlinedTextField(
                value = walletAddress,
                onValueChange = { walletAddress = it },
                label = { Text("Wallet") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            if (isLoading) {
                CircularProgressIndicator()
            }
            
            error?.let {
                Text(
                    text = it,
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall,
                    textAlign = TextAlign.Center
                )
            }
            
            result?.let {
                Text(
                    text = it,
                    color = MaterialTheme.colorScheme.primary,
                    style = MaterialTheme.typography.bodySmall,
                    textAlign = TextAlign.Center
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = {
                    lifecycleScope.launch {
                        registerIdentity(walletAddress)
                    }
                },
                enabled = walletAddress.isNotEmpty() && !isLoading
            ) {
                Text("Register")
            }
        }
    }
    
    private suspend fun registerIdentity(wallet: String) {
        // Implementation similar to iOS version
    }
}
```

---

## API Reference

### Oracle Endpoints

#### POST /oracle/validate
Validate ECG and derive cardiac hash.

**Request:**
```json
{
  "wallet": "0x...",
  "ecgData": {
    "samples": [0.0, 0.1, 0.5, ...],
    "rrIntervals": [800, 820, 810, 795, 805],
    "sampleRate": 512,
    "deviceType": "apple_watch"
  }
}
```

**Response:**
```json
{
  "valid": true,
  "cardiacHash": "0x...",
  "confidence": 0.92,
  "features": {
    "meanRR": 810,
    "sdnn": 45.2,
    "rmssd": 32.1,
    "heartRate": 74,
    "morphologyScore": 0.92
  },
  "expiresAt": 1704067200
}
```

### Relayer Endpoints

#### POST /relay/selfRegisterHuman
Gasless registration.

**Request:**
```json
{
  "wallet": "0x...",
  "cardiacHash": "0x...",
  "deadline": 1704067200,
  "userSig": "0x..."
}
```

**Response:**
```json
{
  "success": true,
  "txHash": "0x...",
  "rootTokenId": "123",
  "gasUsed": "150000"
}
```

---

## Security Best Practices

### 1. Key Storage

**iOS (Secure Enclave):**
```swift
let key = try SecureEnclave.P256.Signing.PrivateKey()
// Store only public key on device
```

**Android (Keystore):**
```kotlin
val keyStore = KeyStore.getInstance("AndroidKeyStore")
keyStore.load(null)
// Generate key pair in hardware
```

### 2. API Secrets

- Store in Keychain/Keystore, not UserDefaults/SharedPreferences
- Rotate regularly
- Use different secrets for dev/prod

### 3. ECG Privacy

- Never store raw ECG samples locally
- Transmit only derived hash
- Clear memory after use

### 4. Network Security

- Certificate pinning for API calls
- HTTPS only
- Validate SSL certificates

---

## Testing & Certification

### Test ECG Data

```json
{
  "rrIntervals": [800, 820, 810, 795, 805, 815, 800, 825],
  "deviceType": "test"
}
```

### Certification Requirements

For official NWO certification:

1. **Accuracy**: >95% successful registrations
2. **Latency**: <5s from scan to registration
3. **Security**: Pass security audit
4. **UX**: Intuitive user flow
5. **Compliance**: GDPR/CCPA compliant

### Submit for Certification

Email: certification@nwo.capital
Include:
- App binary
- Source code (for audit)
- Test results
- Privacy policy

---

## Resources

- [Apple HealthKit Docs](https://developer.apple.com/documentation/healthkit)
- [Wear OS Health Services](https://developer.android.com/training/wearables/health-services)
- [NWO Cardiac SDK](https://github.com/RedCiprianPater/nwo-cardiac-sdk)
- [Base Mainnet](https://base.org)

---

## Support

- **Discord:** [NWO Developers](https://discord.gg/nwo)
- **Email:** dev-support@nwo.capital
- **GitHub Issues:** [Report bugs](https://github.com/RedCiprianPater/nwo-cardiac-sdk/issues)