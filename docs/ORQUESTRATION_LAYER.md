# Orchestration Layer & Asynchronous WebAssembly Bridge

This document details the engineering of the JavaScript orchestration layer (`app.js`) and the background isolation thread (`pyodide.worker.js`), including the secure serverless ingestion proxy (`api/scrape.js`). Together, they establish a secure, bidirectional, and isolated pipeline that hooks into agent tool dispatches to enforce constraints before host execution.

---

## 1. Asynchronous Messaging Pipeline (`postMessage` API)

Because loading and executing a Python environment via WebAssembly inside the browser is computationally demanding, executing it on the main thread would block user interactions. TRIARII delegates the entire policy engine to a dedicated background **Web Worker**.

Communication across this process boundary is strictly governed by the browser's native structured clone algorithm using the `postMessage` API. 

```json
// Outbound Tool Proposal Payload Structure (Main Thread ──► Web Worker)
{
  "type": "VERIFY_CAPABILITY",
  "payload": {
    "tool_name": "git_add",
    "arguments": {
      "path": "../../../.kube/config"
    }
  }
}
2. Ingress Pipeline Architecture & Secure Serverless Proxy
To fully comply with enterprise security practices and eliminate CWE-798 (Use of Hardcoded Credentials) within client-side codebases, TRIARII decouples the network ingress plane into a serverless proxy layout.
The client browser thread never stores, transmits, or possesses the Bright Data Cloud API tokens. Instead, live web-crawling commands are routed through a secure gateway.
 [ Browser Thread (app.js) ] ──► POST (/api/scrape) ──► [ Secure Serverless Environment ]
                                                                   │
                                                                   ├── Reads: process.env.BRIGHT_DATA_API_TOKEN
                                                                   ▼
 [ Authorized Host Effection ] ◄── Verified Payload ◄── [ Bright Data Cloud API Gateway ]
Execution Steps:
The user inputs the target URL (e.g., the deployed security Honeypot repository).
app.js dispatches an asynchronous POST request to the local serverless route /api/scrape.
The serverless function running in the isolated cloud environment intercepts the call, injects the credentials from protected environment variables (process.env), and handles the server-to-server transaction with the Bright Data API.
The client browser receives only the structural transaction metadata, ensuring that sensitive access hashes never enter the DOM, network logs, or client memory heaps.
3. Engineering Silent Denial Mechanics
When an agent is compromised via an Indirect Prompt Injection attack, the adversary relies on explicit application feedback to refine their payload. If the system drops the connection and returns an explicit security diagnostic error (e.g., SecurityError: Access to path denied by policy), the attacker instantly learns the boundary layout.
TRIARII mitigates this optimization vector by implementing Silent Denial inside the orchestration layer.
 [ Agent Issues Exploit ] ──► [ Triarii Core Returns: QUARANTINE ] 
                                          │
                                          ▼
                         ┌─────────────────────────────────┐
                         │      app.js Interception        │
                         └────────────────┬────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
     [ Operational Data Control Plane ]              [ Security Log Control Plane ]
                  │                                               │
                  ▼                                               ▼
     Bypasses Physical Host Tool Call               Appends Forensic Violation Entry
                  │                                 to Immutable SIEM Ledger
                  ▼                                               │
     Injects Synthetic Safe Payload Data                          ▼
     Returns Mocked State: "Status 200 OK"          Fires Telemetry Update Alert
Implementation Execution Workflow:
The orchestrator intercepts the QUARANTINE verdict sent back by the WebWorker thread.
Host Protection: The orchestrator execution routing short-circuits, completely bypassing the invocation handler of the real physical tool. The true filesystem or network resource is never touched.
Feedback Loop Rupture: Instead of passing an execution exception back to the autonomous agent's loop, app.js crafts a synthetic, benign, and empty response state matching the structural requirements of the expected output (e.g., returning an empty successful directory array). Concurrently, the unvarnished incident details are dispatched to an isolated, append-only SIEM log for dashboard telemetry display.