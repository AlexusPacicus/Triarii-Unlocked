# Engine Core & Contractual Policy Logic

This document describes the internal engineering, deterministic algorithms, and mathematical validation loops implemented within `python/policy_engine.py`. This component compiles into WebAssembly (WASM) to act as the final physical boundary for tool execution requests.

---

## 1. Mathematical Representation of Policy Invariants

TRIARII avoids heuristic evaluation. The core engine models safety as a strict state validation problem where a tool dispatch proposal $P$ is authorized if and only if it satisfies the structural and physical invariants mapped within a static cryptographic matrix $M$.

Every capability contract is defined as a tuple of clauses:

$$\mathbf{\text{Clause}} = (\text{tool\_name}, \ \text{argument\_key}, \ \text{physical\_effect}, \ \text{boundary\_constraint})$$

Where:
* $\text{tool\_name} \in \Sigma^*$ represents the authoritative identifier of the tool (e.g., `git_add`).
* $\text{argument\_key} \in \Sigma^*$ represents the targeted primitive input parameter (e.g., `path` or `destination`).
* $\text{physical\_effect} \in \{\text{FILESYSTEM}, \ \text{NETWORK}, \ \text{PROCESS}\}$ defines the underlying host subsystem type.
* $\text{boundary\_constraint}$ represents the immutable constraint limit (e.g., an authorized directory root prefix or a verified domain string).

When the engine processes a payload, it iterates over these mappings. If an incoming argument violates the mapped boundary constraint, the system instantly triggers an infraction state, transitions to a **Fail-Closed** pipeline, and raises a specific structural error code.

---

## 2. Deterministic Filesystem Containment (Path Canonicalization)

String-based path checking (e.g., `if "../" in user_path` or `if user_path.startswith("/safe")`) is a primary vector for supply chain sandbox escapes. Attackers bypass these filters using tricks like symlinks, redundant relative components, or prefix-clipping evasions (e.g., pointing to `/data_backup` when only `/data` is allowed).

TRIARII neutralizes filesystem threats using an isolation loop powered by Python's native `pathlib.Path` library running within the WASM environment.

   [ Raw Unsanitized Argument Path ] (e.g., "./data/exports/../../.ssh/id_rsa")
                   │
                   ▼
     ┌──────────────────────────┐
     │ pathlib.Path().resolve() │  ──► Truncates logical redundancy
     └──────────────────────────┘      & flattens symbolic shifts
                   │
                   ▼
 [ Canonical Path Evaluation State ] (e.g., "/absolute/host/path/.ssh/id_rsa")
                   │
                   ▼
┌──────────────────────────────────────────┐
│  Is Canonical Path prefixed by Boundary? │ ──► Standardized Prefix Matching Loop
└─────────────────────┬────────────────────┘
│
┌─────────┴─────────┐
▼                   ▼
[ YES ]               [ NO ]
│                     │
▼                     ▼
Status: ALLOW       Status: QUARANTINE (CAPABILITY_LAUNDERING)

### Path Sanitization Algorithm:
1. **Isolation Check:** The engine reads the raw path string parameter supplied by the agent planner.
2. **Canonical Transformation:** The string is ingested into an isolated `pathlib.Path` object and fully evaluated via `.resolve()`. This forces the compiler to resolve all relative symlinks, truncate redundant directory movements (`../`), and flatten the path to its absolute physical location inside the virtual file framework.
3. **Prefix Constraint Check:** The resolved path is verified against the authorized execution directory. If the absolute path string does not explicitly share the parent boundary prefix, execution drops into a `CAPABILITY_LAUNDERING` infraction.
4. **Case-Insensitive Normalization:** To prevent host-level bypasses on case-insensitive filesystems (such as macOS or Windows NTFS environments), paths are lowered before the string prefix evaluation step is performed.

---

## 3. Network Egress Integrity & Punycode Transformation

Modern exfiltration techniques—such as **EchoLeak attacks**—exploit the text processing limits of traditional firewalls. If an agent is hijacked via Indirect Prompt Injection, the attacker can extract environment secrets by forcing the agent to connect to an external server under their control.

To evade simple domain string blacklists, attackers use **IDN Homoglyph Attacks**, replacing standard ASCII characters with lookalike Unicode characters from other alphabets (e.g., swapping a standard Latin `i` with a Cyrillic `і` in `api.brightdata.com`). To a human validator or a basic regex engine, the strings look identical; to the DNS resolver, they represent a completely different network sink destination.

[ Untrusted Outbound Domain ] ──► "api.brіghtdata.com" (Contains Cyrillic 'і')
│
▼
┌───────────────────────────┐
│   IDN Punycode Encoding   │ ──► Encodes Unicode characters into deterministic
└─────────────┬─────────────┘     standardized ASCII representations
│
▼
[ Canonical Byte String ]     ──► "xn--api-6hd.brightdata.com"
│
▼
┌───────────────────────────┐
│ Cryptographic Match Loop  │ ──► Evaluated against active contract lists
└─────────────┬─────────────┘
│
┌───────┴───────┐
▼               ▼
[ MATCH ]      [ MISMATCH ]
│               │
▼               ▼
Status: ALLOW   Status: QUARANTINE (NETWORK_EXFILTRATION_ATTEMPT)

### The Punycode Verification Loop:
* The engine intercepts the target destination string before network resources are initialized on the host side.
* The domain string undergoes standard **Internationalized Domain Name (IDN) Punycode** transformation using Python's native string encoding layer (`.encode('idna')`).
* The result is a unified, low-level ASCII byte stream (e.g., `xn--api-6hd.brightdata.com`).
* This canonical byte stream is evaluated directly against the authorized destination array. Because homoglyphs resolve to completely unique `xn--` signatures, any spoofing attempt results in an immediate mismatch and triggers a `NETWORK_EXFILTRATION_ATTEMPT` verdict.

---

## 4. Input Sanitization & Structural Invariants

Before physical or path checks are performed, the payload is checked for low-level memory and structural anomalies:

### Null Byte Pointer Poisoning Protection
Adversaries frequently inject null byte strings (`\x00` or `%00`) into path parameters. In underlying systems written in C/C++, encountering a null byte acts as a string termination character. An attacker can supply a path argument like `./exports/document.pdf\x00/../../etc/passwd`. High-level string checks see a safe extension (`.pdf`), but low-level file APIs truncate the string at the null byte, reading a completely different target path.

TRIARII scans every incoming string argument for null byte signatures. If a `\x00` character is found anywhere within the payload, the evaluation loop halts immediately, rejects the transaction, and issues an `ANOMALOUS_STRUCTURE_ATTEMPT` violation.

### Explicit Primitive Type Integrity
To bypass application logic, attackers use type confusion attacks—such as passing an array or a dictionary object into a field where the system expects a primitive string. This can cause down-stream functions to break or crash, causing safe-guards to fail open.

`policy_engine.py` validates that all incoming arguments match their strict primitive definitions before passing them to the validation handlers:
```python
if not isinstance(proposed_argument, str):
    return {
        "verdict": "QUARANTINE",
        "infraction_code": "ANOMALOUS_STRUCTURE_ATTEMPT"
    }
By enforcing type checking at the WASM border, TRIARII ensures that no malicious data types can contaminate the operational stability of the system.