# System Architecture & Runtime Isolation Topology

This document details the structural mechanics, memory isolation topology, and execution flow of TRIARII. The system is engineered to enforce zero-trust capability constraints on autonomous agents operating within browser runtimes.

---

## 1. The *Acies Triplex* Enforcement Model

TRIARII rejects flat validation architectures. Instead, it deploys a sequential, multi-layered defensive pipeline modeled after the *Acies Triplex*. However, to maintain high throughput and avoid false positives, the layers have asymmetric operational weights: the front lines act as telemetry collection points, while the final layer serves as the absolute physical boundary.

[ UNTRUSTED MCP / AGENT INTENT ]
│
▼
┌────────────────────────┐
│     HASTATI LAYER      │ ──► Lexical Telemetry & Signatures (Low Weight)
└────────────────────────┘
│
▼
┌────────────────────────┐
│    PRINCIPES LAYER     │ ──► Structural Schema Verification (Medium Weight)
└────────────────────────┘
│
▼
┌────────────────────────┐
│     TRIARII LAYER      │ ──► HARD RUNTIME ISOLATION BOUNDARY (Absolute Weight)
│   (WebAssembly Core)   │     [Path Canonicalization & Punycode Translation]
└────────────────────────┘
│
▼
[ AUTHORIZED HOST EXECUTION ]

### Layer Operational Mechanics

| Layer Name | Execution Context | Primary Objective | Failure Mode | Architectural Weight |
| :--- | :--- | :--- | :--- | :--- |
| **Hastati** | Main JS Thread (`app.js`) | Fast lexical analysis of incoming data buffers for generic exploit signatures. | **Fail-Open:** Logs anomaly to telemetry; passes data to next line. | 10% (Observability Anchor) |
| **Principes** | Worker Gateway (`app.js` / Web Worker) | Strict deserialization validation. Enforces context typing rules against JSON schemas. | **Fail-Closed:** Drops execution immediately if structure is corrupted. | 30% (Protocol Integrity) |
| **Triarii** | **Isolated WASM Sandbox** (`policy_engine.py`) | Deterministic validation of physical parameters (`pathlib`, Punycode bytes) against the capability matrix. | **Fail-Closed:** Triggers Silent Denial countermeasure; isolates the execution thread. | 60% (Absolute Boundary) |

---

## 2. Memory Isolation & Sandbox Topology

To guarantee that a compromised LLM planner cannot manipulate the security engine itself, TRIARII enforces strict decoupling at the browser process level using a dedicated **Web Worker** running compiled **WebAssembly (WASM)** via Pyodide.

┌──────────────────────────────────────────┐         ┌──────────────────────────────────────┐
│          MAIN BROWSER THREAD             │         │       ISOLATED WEB WORKER THREAD     │
│                                          │         │                                      │
│  ┌─────────────────┐   ┌──────────────┐  │         │  ┌────────────────────────────────┐  │
│  │ Autonomous Agent│   │ Telemetry UI │  │         │  │       PYODIDE WASM RUNTIME     │  │
│  │ (LLM Planner)   │   │  (DOM View)  │  │         │  │                                │  │
│  └────────┬────────┘   └──────────────┘  │         │  │  ┌──────────────────────────┐  │  │
│           │                             │         │  │  │    policy_engine.py      │  │  │
│           │ (Tool Proposal JSON)        │         │  │  │                          │  │  │
│           ▼                             │         │  │  │ ┌──────────────────────┐ │  │  │
│   [ app.js Orchestrator ]                │         │  │  │ │ Capability Matrix  │ │  │  │
│           │                             │         │  │  │ └──────────────────────┘ │  │  │
│           │  postMessage()              │         │  │  └──────────────────────────┘  │  │
│           └─────────────────────────────┼─────────┼─►│                                │  │
│                                          │         │  └────────────────────────────────┘  │
└──────────────────────────────────────────┘         └──────────────────────────────────────┘

### Architectural Safeguards of the WASM Boundary:
1. **Zero DOM/Global Context Access:** The Web Worker thread possesses no access to the `window` object, document cookies, local storage, or the main thread's DOM. If an agent attempts an XSS injection or environment variable hijacking via tool manipulation, the malicious memory space remains entirely trapped inside the worker thread.
2. **Immutable Memory Space:** The compiled Pyodide WASM state allocates its own isolated memory heap. The security matrix (`policy_engine.py`) loads authoritatively from cold, static assets at boot time and cannot be overwritten or redefined by JavaScript runtime assignments executing on the main thread.
3. **No Direct Network Access:** The worker does not initialize network fetches based on agent text inputs. Network intents are translated exclusively into cryptographic Punycode representations within the sandbox and passed back as strict boolean verdicts to the orchestrator layer.

---

## 3. Synchronous In-Flight Interception Flow

Security validation must happen *in-flight*—meaning a tool call is intercepted after the agent proposes it, but before the underlying JavaScript execution layer triggers the physical API call or system execution loop. 

### Execution Sequence

Agent/LLM            app.js (Main)        pyodide.worker.js       policy_engine.py (WASM)
│                       │                       │                         │
│ 1. Propose Tool Call  │                       │                         │
├──────────────────────►│                       │                         │
│    (JSON Payload)     │ 2. Extract Arguments  │                         │
│                       ├──────────────────────┐│                         │
│                       │                      ││                         │
│                       │ 3. Forward Payload   ││                         │
│                       │    via postMessage() ││                         │
│                       │─────────────────────►│                         │
│                       │                       │ 4. Initialize Function  │
│                       │                       ├────────────────────────►│
│                       │                       │                         │ 5. Canonicalize Paths
│                       │                       │                         │    & Verify Contract
│                       │                       │                         │─────────────────┐
│                       │                       │                         │                 │
│                       │                       │ 6. Emit Return Code     │◄────────────────┘
│                       │                       │    ( Verdict / Flags )  │
│                       │                       │◄────────────────────────┤
│                       │ 7. Return Binary      │                         │
│                       │    Enforcement State  │                         │
│                       │◄──────────────────────┤                         │
│                       │                       │                         │
│                       │ 8. ENFORCEMENT ACTION │                         │
│                       │    (Execute / Block)  │                         │
│                       ├───────────────────────┘                         │
│                       │                                                 │

### The Transactional Gatekeeper Mechanics
* When a capability (such as `git_add`) is called, the orchestrator blocks the tool handler loop using an asynchronous callback anchor.
* The payload is serialized into an immutable JSON dictionary and dispatched across the worker channel.
* The main thread remains suspended for the specific agent workflow execution until the WebAssembly core returns a binary verdict: `ALLOW` or `QUARANTINE`.
* If `ALLOW`, the loop resumes and triggers the physical tool function. If `QUARANTINE`, the tool pipeline triggers the **Silent Denial** module, skipping the host execution phase entirely.

---

## 4. Control Plane vs. Data Plane Separation

The core technical failure of current agent frameworks is treating control signals (tool parameters) and data streams (untrusted ingress text) interchangeably within the same logical layer. TRIARII strictly separates these paths:

* **The Data Plane (Untrusted):** Contains the raw text, scraped web outputs, and prompt templates processed by the agent. This plane has zero system authority and is treated as malicious input by design.
* **The Control Plane (Trusted):** Comprises the strict schemas managed by `app.js` and the physical boundaries checked by `policy_engine.py`. 

Once data leaves the agent context to execute an action, **the text loses all authority**. It must conform entirely to the physical constraints of the control plane. If an agent tries to use an argument key to alter the behavior of a tool (e.g., injecting options like `--exec` inside a file path parameter), the control plane flags it as a structural mutation error (`ANOMALOUS_STRUCTURE_ATTEMPT`) and neutralizes the execution mid-flight.