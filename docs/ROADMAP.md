# Engineering Roadmap & Enterprise Scaling Evolution

This document outlines the transition vector of TRIARII from its current architectural state (MVP/Browser Prototype) into a hardened, enterprise-grade, distributed agent governance framework. 

---

## Current Architecture State (MVP Baseline)
The current implementation serves as a functional validation prototype operating strictly within client-side browser processes. It demonstrates synchronous *in-flight* tool interception, isolated memory validation using a local WebAssembly heap (Pyodide), and the execution of deterministic sanitization algorithms (path canonicalization and network Punycode translation). 

To transition this architecture into production systems, evolution must scale across three vectors: Automation, Governance, and Platform Hardening.

---

## 🗺️ Evolution Phases

[ PHASE 1: AUTOMATION ] ──► Automated Contract Generation & Asymmetric Policy Signing
│
▼
[ PHASE 2: GOVERNANCE ] ──► Centralized Enterprise Control Plane & Streaming SIEM Sink
│
▼
[ PHASE 3: HARDENING  ] ──► Cross-Platform Execution (Node/Python) & Kernel-Level eBPF Confinement

### Phase 1: Automation & Cryptographic Integrity (Short-Term)
*Objective: Eliminate manual JSON policy definitions and secure the delivery of capability matrices.*

* **Automated Contract Discovery:** Implement static code analysis modules within the CI/CD pipeline. Instead of requiring developers to manually write capability clauses, the system will parse Model Context Protocol (MCP) tool configurations and Python docstrings, automatically compiling the strict JSON schemas and physical constraints during the application build phase.
* **Asymmetric Policy Cryptography:** To prevent an adversary from tampering with the capability matrix at the distribution layer, matrices will be cryptographically signed by the enterprise authority using private keys ($K_{\text{private}}$). The client-side WebWorker will verify the payload integrity at boot time using the corresponding public key ($K_{\text{public}}$) embedded inside the immutable WASM image. Any unauthorized modification to the boundary constraints will trigger an immediate initialization failure.

### Phase 2: Enterprise Control Plane & Observability Scale (Medium-Term)
*Objective: Scale policy management and threat telemetry horizontally across thousands of distributed concurrent clients.*

* **Decentralized Execution, Centralized Governance:** While the physical evaluation compute overhead remains decentralized at the client edge (maintaining the zero-cost infrastructure model), policy distribution will be centralized. A lightweight, encrypted REST API endpoint will synchronize active capability matrices across client runtimes dynamically.
* **Structured SIEM Streaming Sinks:** Expand the *Silent Denial* telemetry plane. Local infraction logs currently captured in temporary client-side buffers will be serialized into compressed JSON blobs and streamed via secure, non-blocking asynchronous requests to centralized enterprise SIEM infrastructures (e.g., Splunk, Datadog, or localized AWS Kinesis data firehoses) for automated SOC alerting.

### Phase 3: Platform Hardening & Low-Level Kernels (Long-Term)
*Objective: Move the Triarii Layer beyond browser threads into server-side autonomous agent infrastructures.*

* **Cross-Runtime Portability:** Recompile the core Python validation matrix (`policy_engine.py`) using lightweight native runtimes (such as Wasmtime or Wasmer). This allows TRIARII to deploy as a native wrapper plugin inside server-side agent frameworks executing on Node.js, Python (LangChain, CrewAI), or Go.
* **Kernel-Level Sandboxing (eBPF & Seccomp-BPF):** For server-side agent execution clusters, the *Triarii Layer* will interface directly with low-level Linux kernel protection mechanisms. Verified tool calls that require physical system invocation will be bound to **eBPF (Extended Berkeley Packet Filter)** hooks and strict **seccomp** profiles. If an agent process attempts an unauthorized system call or attempts to write to a path outside its canonical container space, the Linux kernel will drop the instruction at the processor ring layer, completely hardening the system against zero-day sandbox escapes.