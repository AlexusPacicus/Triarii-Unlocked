<div align="center">

<p align="center">
  <img src="logo.jpg" width="220" alt="TRIARII Centurion Shield">
</p>

████████╗██████╗ ██╗ █████╗ ██████╗ ██╗██╗
╚══██╔══╝██╔══██╗██║██╔══██╗██╔══██╗██║██║
   ██║   ██████╔╝██║███████║██████╔╝██║██║
   ██║   ██╔══██╗██║██╔══██║██╔══██╗██║██║
   ██║   ██║  ██║██║██║  ██║██║  ██║██║██║
   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝

### **TRIARII // Distributed Runtime Agentic Boundary**
*Browser-Native Capability Enforcement Sandbox for Web-Connected Autonomous Agents*

[![Tests](https://img.shields.io/badge/pytest-15%2F15%20passing-10b981?style=flat-square&logo=pytest&logoColor=white)](test/test_policy_engine.py)
[![WASM](https://img.shields.io/badge/runtime-Pyodide%20WASM-00f2fe?style=flat-square)](https://pyodide.org)
[![Bright Data](https://img.shields.io/badge/ingress-Bright%20Data-f97316?style=flat-square)](https://brightdata.com)
[![Latency](https://img.shields.io/badge/enforcement%20latency-12ms--25ms-10b981?style=flat-square)](#4-operational-performance-metrics)

</div>

---

> **Director's Note:** *On May 27, 2025, I left military service for software engineering. In tactical defense, perimeters are never secured by negotiating with the threat's intent; they are enforced via physical, immutable barriers. TRIARII applies this exact structural discipline to AI capability containment.*

---
## 🚀 Live Interactive Demo
You do not need to install or configure anything locally to evaluate this project. The entire security platform, including the WebAssembly isolation sandboxing and adversarial stress testing harness, runs natively inside your browser.

👉 **[Access the Live Production Platform on Vercel](https://your-deployed-vercel-url.vercel.app)**

---


## 1. Core Thesis: The Von Neumann Fallacy

Modern LLM agent frameworks replicate the classic **Von Neumann architecture flaw** at a semantic level: they ingest system instructions (control signals) and untrusted third-party web data (data streams) within the same unified token context window. Because the natural language processing unit cannot physically separate authoritative commands from unvalidated execution parameters, threat actors inevitably hijack the execution loop via **Indirect Prompt Injections (IDPI)**.

TRIARII resolves this vulnerability by enforcing a localized **Harvard Architecture** at the tool-execution boundary. **Linguistic context has zero host authority.** Once an agent translates natural language into a structured tool invocation JSON, its semantic authority ends. TRIARII intercepts the payload *in-flight* within a browser-native sandboxed thread, evaluating parameter objects strictly against an invariant capability matrix before host defection occurs.

---

## 2. Architecture: The *Acies Triplex* Pipeline

TRIARII formats its security posture into three sequential lines of defense, shifting 100% of the enforcement and execution weights away from probabilistic LLM guardrails onto a deterministic sandbox boundary.

 [ UNTRUSTED AGENT / MCP TOOL PROPOSAL ]
                   │
                   ▼
⚔️  HASTATI LAYER    ──► Lexical Scan (Auxiliary Signatures / Telemetry Log)
│
▼
🛡️  PRINCIPES LAYER  ──► Structural Validation (Fail-Closed Context Typing)
│
▼
💎  TRIARII LAYER    ──► RUNTIME ENFORCEMENT (Isolated WASM Execution Boundary)
│
▼
[ AUTHORIZED HOST EFFECTIO ]

### Layer Operational Mechanics
* **Hastati Layer (10% Weight):** Executes fast lexical analysis of raw incoming data buffers for generic exploit signatures via JavaScript regex patterns. **Fail-Open:** Logs telemetry and transitions tracking state.
* **Principes Layer (30% Weight):** Enforces strict context typing and validation against authoritative JSON schemas. **Fail-Closed:** Drops the execution thread instantly if the object layout is corrupted.
* **Triarii Layer (60% Weight):** The ultimate physical boundary. Runs compiled Python verification routines inside an isolated WebAssembly (WASM) heap driven by Pyodide. Executes absolute path canonicalization and IDN domain translations. **Fail-Closed:** Completely blocks host resource access and triggers defensive counters.

---

## 3. Hardened Capability Activation Invariants

Every authorized capability within the governance boundary must strictly map to a multi-dimensional constraint contract clause:

$$\mathbf{\text{Clause}} = (\text{tool\_name}, \ \text{argument\_key}, \ \text{physical\_effect}, \ \text{boundary\_constraint})$$

```python
# Mapped Capability Matrix Clause Layout inside policy_engine.py
CapabilityMatrix = (
    ("git_add", "path", "FILESYSTEM", "./data/exports"),
    ("brightdata_ingress", "endpoint_api", "NETWORK", ("api.brightdata.com", "enterprise-egress.com")),
    ("html_parser", "path", "FILESYSTEM", "./data/exports")
)
Deterministic Containment Algorithms
Geographical Path Canonicalization: To neutralize advanced directory traversal sandbox escapes (../) and partial prefix-clipping evasions, path parameters undergo physical compilation lookups via Python's native pathlib.Path().resolve(). Logical tracking layers are flattened to absolute target strings and validated against parent constraints.
Network Egress Confinement: To block stealth environment secret harvesting channels (EchoLeak attacks), outbound connection parameters are normalized into native Internationalized Domain Name (IDN) Punycode bytes (.encode('idna')). Homoglyph spoofing attempts using identical Cyrillic unicode strings immediately compile to distinct xn-- signatures, triggering an instant mismatch block.
Null-Byte Pointer Protection: Immediate scanning for memory string termination characters (\x00). Encountering a null byte halts evaluation, drops the pipeline, and issues a structural anomaly infraction code.
4. Threat Countermeasures: Silent Denial
Standard security proxies emit descriptive error traces (403 Forbidden: Escape Detected), creating a feedback loop that allows a compromised agent planner to dynamically iterate its prompt injection structure until it evades the rules.
TRIARII mitigates this optimization channel by implementing Silent Denial:
The WebAssembly policy core drops the physical host tool call execution entirely, completely shielding the host system resources.
The raw incident metadata, latency timestamps, and violation codes are dispatched to an isolated, append-only SIEM ledger for security operations visibility.
The orchestrator injects a synthetic, safe, and structurally compliant empty payload back to the agent loop thread (e.g., a mock Status: 200 OK network payload). The adversary remains completely blind, unable to verify whether the exploit failed due to a security filter or an internal token logic error.
5. Enterprise Financial Viability (ROI Model)
Traditional agent guardrails route token verification vectors through centralized secondary cloud layers, generating unsustainable cloud infrastructure overhead and scaling costs.
TRIARII introduces a zero-cost infrastructure governance posture:
Decentralized Compute: Shift 100% of the policy parsing, path resolution, and Punycode compilation workloads directly onto the client's edge browser engine via WebAssembly.
Linear Cost Efficiency: Enterprise infrastructure compute cost scales exactly at $0 regardless of concurrent agent usage spikes, avoiding expensive secondary cloud inference hops or middleware API transactional taxes.
6. Test Verification Matrix
Security mechanics are continuously verified and certified against the automated adversarial red-team suite located in test_policy_engine.py:
Test ID	Threat Vector Profile	Target Input Parameter	System Verdict	Infraction Code
TC-01	Compliant File Staging	Path inside authorized ./data/exports/	ALLOW	NONE
TC-02	Valid Network Egress	Request targeting api.brightdata.com	ALLOW	NONE
TC-03	Path Traversal Escape	Directory escape attempts via ../../../	QUARANTINE	CAPABILITY_LAUNDERING
TC-04	Prefix Evasion Attempt	Path target using mirrored directory strings	QUARANTINE	CAPABILITY_LAUNDERING
TC-05	Structural Mutation	Root JSON schema token manipulation	QUARANTINE	ANOMALOUS_STRUCTURE_ATTEMPT
TC-06	Type Confusion Attack	Array injection into primitive string input parameters	QUARANTINE	CAPABILITY_LAUNDERING
TC-06b	Outbound Network Leak	Unauthorized external TCP data tunnels (EchoLeak)	QUARANTINE	NETWORK_EXFILTRATION_ATTEMPT
TC-10	Hot-Patch Rule Revocation	Dynamic contract removal during live session	QUARANTINE	PRIVILEGE_OVER_STEP
TC-11	Restricted File Format	Malicious scripts disguised within valid parent paths	QUARANTINE	ANOMALOUS_STRUCTURE_ATTEMPT
TC-12	Null Byte Poisoning	Injection of \x00 memory boundary termination strings	QUARANTINE	ANOMALOUS_STRUCTURE_ATTEMPT
TC-15	Homoglyph Spoofing Bypass	Target URL mimicking using Cyrillic lookalikes	QUARANTINE	NETWORK_EXFILTRATION_ATTEMPT
7. Setup & Execution
Local Adversarial Test Suite
To execute the automated matrix framework locally and verify contract compliance rules:
Bash
# Install testing dependencies
pip install pytest pytest-cov

# Run the validation suite with coverage checking tracking
pytest test/test_policy_engine.py -v --cov=python --cov-report=term-missing
Serverless Edge Deployment (Vercel)
To protect your production crawler architecture from CWE-798 (Use of Hardcoded Credentials), the infrastructure routes transactions via an isolated Serverless Proxy Pattern. Do not open index.html directly from a static file viewer; deploy or serve the system using serverless platforms:
Bash
# 1. Install Vercel CLI toolchain
npm install -g vercel

# 2. Login and link your workspace
vercel login
vercel link

# 3. Add your production Bright Data environment configurations
vercel env add BRIGHT_DATA_API_TOKEN production
vercel env add BRIGHT_DATA_DATASET_ID production

# 4. Trigger production compilation and edge deployment routing
vercel --prod