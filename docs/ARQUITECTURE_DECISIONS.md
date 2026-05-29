# Architecture Decision Records (ADR)

This document serves as an unembellished, authoritative ledger documenting the foundational technical decisions, trade-offs, and structural constraints established during the engineering of TRIARII.

---

## ADR-001: Separation of Control Plane and Data Plane (The Von Neumann Analogy)

### Context
Autonomous LLM agents consolidate system instructions, contextual variables, and untrusted runtime data into a single, contiguous token vector. This structural layout mirrors the classic vulnerability of the **Von Neumann computer architecture**, which stores program instructions and execution data within the same shared memory heap. 

Historically, this unification allowed adversaries to perform low-level exploit injections (e.g., buffer overflows) by forcing the processing unit to evaluate data strings as executable instructions. Modern prompt injections are not linguistic anomalies; they are the deterministic result of running a Von Neumann architecture over a natural language space.

### Decision
We reject the practice of building semantic firewalls or intent-classification loops within the agent's context window. Instead, TRIARII enforces an absolute decoupling of the **Control Plane** (authoritative tool structures and physical boundaries) and the **Data Plane** (the agent's internal linguistic reasoning and ingress text). 

Once the agent issues a tool proposal, the semantic context loses all validation authority. The parameter dictionary is treated strictly as an unvalidated raw data stream and subjected to physical validation inside an isolated execution environment, effectively replicating the isolation principles of a **Harvard Architecture** at the execution boundary.

### Consequences
* **Positive:** Complete neutralization of semantic obfuscation tactics. An agent can be completely compromised ideologically, yet it remains physically constrained from executing unauthorized host operations.
* **Negative:** Requires deterministic configuration of tool capability matrices prior to agent deployment. Structural flexibility is restricted in favor of predictable runtime behavior.

---

## ADR-002: Client-Edge Execution via WebAssembly (Pyodide)

### Context
Traditional enterprise API guardrails and security proxies route validation traffic through centralized cloud infrastructure. When securing autonomous agents, this model introduces two severe operational limitations:
1. **Network Latency:** Adding external network hops to evaluate string vectors introduces a cumulative processing overhead of over 200ms, rendering real-time UX interactions sluggish.
2. **Compute Cost Inflation:** Parsing massive token streams through secondary cloud inference layers or hosted validation firewalls generates linear, unsustainable infrastructure costs when scaling to concurrent production agents.

### Decision
We reject the reliance on cloud-based validation proxies. TRIARII compiles its core contract verification matrix into an isolated **WebAssembly (WASM)** binary runtime driven by Pyodide, executing natively inside a browser Web Worker. 

All path canonicalization, null-byte scanning, and IDN domain translations are processed locally within the client-side execution thread, entirely independent of central cloud routing.

### Consequences
* **Positive:** Reduces transactional evaluation latency to sub-5ms intervals. Eliminates recurring central server infrastructure overhead, establishing a sustainable economic model where security compute cost scales at precisely $0 to the enterprise.
* **Negative:** Increases the initial application cold-start payload size, as the browser must ingest the Pyodide runtime components during initial asset load.

---

## ADR-003: Operational Countermeasure via Silent Denial

### Context
Standard access control systems operate on explicit validation logging: when an action violates a boundary constraint, the system breaks the pipeline and emits an explicit error trace (e.g., `403 Forbidden: Destination directory outside authorized root`). 

In agentic security, this pattern creates an adversarial optimization channel. Autonomous agents operate on closed loop planners; receiving detailed technical error logs provides the compromised planner with immediate diagnostic feedback, allowing it to dynamically mutate its prompt injection structure until it bypasses the validation rule.

### Decision
TRIARII implements a **Silent Denial** interception strategy. When the WebAssembly policy core registers a capability infraction (`CAPABILITY_LAUNDERING` or `NETWORK_EXFILTRATION_ATTEMPT`), the orchestrator layer drops the physical tool invocation loop to protect the host. 

However, instead of raising an execution exception, the interface intercepts the pipeline and returns a synthetic, successful, and structurally compliant empty payload back to the agent loop (e.g., a mock `Status: 200 OK` network payload). Concurrently, the unvarnished incident details are dispatched to an isolated, append-only SIEM log for administrator review.

### Consequences
* **Positive:** Successfully ruptures the attacker's feedback loop. The adversary remains completely blind, unable to ascertain whether the exploit failed due to a structural filter interception or an internal logic flaw within their prompt execution string.
* **Negative:** Debugging legitimate tool integration mismatches during the development phase becomes more complex, as runtime errors are intentionally masked on the main application execution path.

## ADR-004: Secure Serverless Proxy for API Credential Isolation (CWE-798 Mitigation)

### Context
Executing live network web crawling via third-party cloud infrastructure (Bright Data API) requires active bearer tokens and collector identification hashes. In standard client-side browser architectures, executing these network calls directly from the main thread requires hardcoding credentials within JavaScript source assets or exposing them inside the browser's public network transaction logs. 

For an infrastructure engineering project competing within a **Security & Compliance** track, this layout introduces a critical vulnerability: **CWE-798 (Use of Hardcoded Credentials)**, allowing any malicious entity or client-side scraper to harvest enterprise API keys.

### Decision
We reject the placement of API authentication tokens within the client-side codebase or the public runtime browser space. Instead, TRIARII routes all ingress data pipeline tracking through an isolated **Serverless Proxy Pattern** located at `/api/scrape.js`. 

The frontend orchestrator sends an unauthenticated parameter payload to this internal route. The serverless function executes within a protected backend server container, populates the authentic authorization headers dynamically via secure environment variables (`process.env`), and communicates server-to-server with Bright Data. The client thread only handles the non-sensitive operational responses.

### Consequences
* **Positive:** Complete remediation of CWE-798 credential exposure vectors. The enterprise API keys remain 100% invisible to the user's browser, network sniffers, and public GitHub code repositories.
* **Negative:** Shifts the deployment topology requirement from a purely static HTML host (like raw GitHub Pages) to a platform capable of compiling serverless gateway routes (such as Vercel or Netlify).