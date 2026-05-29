# Threat Modeling & Vulnerability Research

This document establishes the theoretical security boundaries, threat taxonomy, and attack vectors evaluated during the design of TRIARII. Security engineering requires moving away from probabilistic mitigation toward deterministic runtime constraints.

---

## 1. The Agentic Surface Attack Evolution

[cite_start]The transition of the browser interface from a passive content renderer driven by human interactions to an autonomous execution actor (e.g., Atlas, Comet, GenSpark) invalidates classical perimeter security frameworks[cite: 4, 5]. [cite_start]In agentic workflows, the primary operational threat is no longer malicious code running on the client thread, but the semantic manipulation of the agent's deterministic intent[cite: 6].

The runtime surface area presents three structural architectural flaws:
* [cite_start]**Operational Opacity:** Agent frameworks frequently execute as multi-layered black boxes, making granular step-logging, internal state visibility, and transactional rollbacks difficult to capture[cite: 7].
* [cite_start]**Over-Permissioning:** To achieve automation autonomy, agents are routinely granted extensive underlying host privileges, transforming them into high-value proxies for lateral movement and local host compromise[cite: 8].
* [cite_start]**Indirect Prompt Injection (IDPI):** The capability to ingest untrusted, third-party external data sources permits threat actors to embed adversarial payloads into standard operational inputs, hijacking the execution thread[cite: 9].

---

## 2. Deep Dive: Capability Laundering

[cite_start]**Capability Laundering** is a design vulnerability where an compromised agent abuses a legitimate tool invocation to generate unauthorized, secondary physical effects on the underlying host system[cite: 11]. 

[ Compromised LLM Planner ] ──► Invokes: "git_add" ──► [ Execution Runtime / MCP Server ]
│
└──► Secondary Physical Effect:
Reads: "../../../.ssh/id_rsa"

This exploit is powered by the **Approval Gap**[cite: 12]. While a user or a gateway infrastructure validates and approves a tool call based solely on its semantic identifier or function name (e.g., `git_add`), the actual execution happens within a detached Model Context Protocol (MCP) server or host runtime[cite: 12]. The security validation check checks the label, but fails to model or restrict the physical side effects on the network layer or the local file hierarchy[cite: 13, 14].

### Exploitation Prerequisites
For a capability laundering exploit to succeed, three logical systemic conditions must converge:
1. **Insufficient Contractual Scope:** The tool implementation exposes parameters that allow execution outside its core stated utility[cite: 16].
2. **Addressable Physical Inputs:** The arguments supplied dynamically by the LLM planner can directly manipulate execution destinations (such as path strings or IP addresses)[cite: 17].
3. **Label-Based Control Fallacy:** The gateway validates the *identity* of the tool instead of the physical *effect* of its parameters[cite: 18].

### Real-World Reference Case Vector Analysis
* **Memory MCP Vulnerability:** A component engineered for routine memory storage was manipulated via structural input to perform arbitrary file writes, leading to terminal hijacking inside development sandboxes like VS Code[cite: 19].
* **Git-Init Capability Abuse (CVE-2025-68143):** Insufficient directory constraints allowed agents to initialize arbitrary repositories outside the intended current working directory (CWD), gaining unauthorized write vectors to protected system folders like `~/.ssh`[cite: 20].
* **Git-Add Relative Path Escape (CVE-2026-27735):** A vulnerability inside the `GitPython` library (`_to_relative_path`) failed to properly check relative directory configurations[cite: 21]. By feeding `../` sequences into the tool arguments, a compromised planner could force the library to read highly sensitive system secrets—such as active AWS access tokens or Kubernetes cluster configurations—and stage them silently into the Git index for extraction[cite: 21].

---

## 3. Adversarial Payload Taxonomy (IDPI)

Indirect Prompt Injection attacks are classified by TRIARII based on their systemic severity and their deployment methodology[cite: 39].

### Threat Matrix (Based on Unit 42 Framework)

| Severity Level | Adversarial Objective / Intent | Direct Technical Impact |
| :--- | :--- | :--- |
| **Low (Disruption)** | Induce repetitive token loops, resource depletion, or arbitrary context pollution[cite: 41, 42]. | Denial of Service (DoS) via token-bloat exhaustion[cite: 42]. |
| **Medium (Manipulation)** | Bias the logical evaluation loops of the agent (e.g., forcing biased reviews or falsifying automated HR screening metrics)[cite: 43, 44]. | Integrity failure within automated decision pipelines[cite: 44]. |
| **High (Predatory)** | Bypass ad-review moderation filters, inject malicious SEO data, or initiate unauthorized transactions[cite: 45, 46]. | Compliance breaches and localized financial/operational risk[cite: 46]. |
| **Critical (Estructural)** | Execute mass data deletion, trigger System Prompt Leakage, or exfiltrate environment variables and PII[cite: 47, 48]. | Total compromise of host data integrity and confidentiality[cite: 48]. |

### Advanced Obfuscation Delivery Methods
Adversarial payloads bypass traditional static text scanning through three primary delivery vectors:
* **Visual Cloaking:** Rendering text strings invisible to human operators using zero-size typography, matching color hex codes to backgrounds, or enforcing an `opacity: 0` CSS state while remaining readable to the agent's scraper[cite: 49].
* **HTML Attribute Injection:** Hiding executable instructions inside structural metadata parameters (such as `data-*` fields) or commented brackets that are processed directly during tokenization[cite: 50].
* **Runtime Document Assembly:** Storing the malicious payload in encoded formats (e.g., Base64 strings) inside the document body, forcing the agent to programmatically decode and execute it after initial text sanitizers have completed their pass[cite: 51].

---

## 4. Supply Chain Vulnerability Mechanics

Orchestration and workflow frameworks currently process untrusted metadata buffers without enforcing a clear separation between control signals and data streams[cite: 53].

### LangChain Core (CVE-2025-68664)
The vulnerability stems from the implicit trust of reserved structural keywords during serialization routines[cite: 54]. When using data parsing methods like `dumps()` or `dumpd()`, encountering a dictionary containing the specific reserved key `lc` causes the framework to automatically process the payload as a verified **Trusted Object** instead of standard user data[cite: 55]. Attackers exploit this behavior by crafting dictionaries that force the instantiation of unauthorized arbitrary classes, triggering remote code execution (RCE) and immediate secret harvesting[cite: 56].

### CrewAI Infrastructure (VU#221883)
This vulnerability stems from an insecure structural fallback architecture[cite: 57]. When an active agent fails to establish a secure connection to its designated Docker container environment, the system automatically degrades its isolation state to a local fallback interpreter (`SandboxPython`)[cite: 58]. Because this local fallback module failed to explicitly include `ctypes` within its internal `BLOCKED_MODULES` array, adversaries could leverage C-level function mapping to execute low-level operating system commands, completely breaking the Python sandbox boundary[cite: 59].

---

## 5. Architectural Countermeasures Counter-Strategy

TRIARII implements a physical mitigation model designed to neutralize these findings before data inputs reach the context window of the LLM core[cite: 64]:

1. **Rupture of the Adversarial Feedback Loop (Silent Denial):** Traditional security frameworks return descriptive error messages (e.g., `Error: Path Transversal Detected`)[cite: 69]. This gives attackers a clear diagnostic feedback loop to refine their injection text until it passes[cite: 70]. TRIARII catches infractions, records them to an unmodifiable SIEM log, and returns a synthetic, clean, empty status block[cite: 68, 75]. The attacker is left completely blind, unable to verify if the payload failed due to a core prompt logic error or a hard security enforcement block[cite: 70].
2. **Shifting Enforcement to the Physical Layer:** Rather than relying on the agent's internal sandbox to monitor itself, boundaries are enforced through strict path canonicalization and Punycode transformation loops compiled inside an isolated, client-side WebAssembly thread[cite: 77]. The natural language stream is treated with the same zero-trust sanitization rigor as an untrusted raw SQL query[cite: 78].