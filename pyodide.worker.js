// pyodide.worker.js (Self-Contained Authoritative WASM Enforcement Engine - Hardened Bridge)

importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");

let pyodideReady = false;
let pyodideInstance;

async function initPyodideEngine() {
    try {
        pyodideInstance = await loadPyodide();
        
        // Immutable synchronization of the Deterministic Core into the WASM Memory Heap
        await pyodideInstance.runPythonAsync(`
import json
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_POLICY = [
    {"tool_name": "brightdata_ingress", "expected_argument_key": "endpoint_api", "physical_effect": "NETWORK", "boundary_constraint": ["api.brightdata.com", "enterprise-egress.com"]},
    {"tool_name": "git_add", "expected_argument_key": "path", "physical_effect": "FILESYSTEM", "boundary_constraint": "./data/exports"},
    {"tool_name": "html_parser", "expected_argument_key": "path", "physical_effect": "FILESYSTEM", "boundary_constraint": "./data/exports"}
]

def evaluate_agent_proposal(proposal_json_str, policy_json_str=None):
    try:
        # Reconstruct matrix with a robust fallback for partial frontend schemas
        try:
            raw_policy = json.loads(policy_json_str) if policy_json_str else DEFAULT_POLICY
            if not raw_policy or not isinstance(raw_policy, list) or "physical_effect" not in raw_policy[0]:
                raw_policy = DEFAULT_POLICY
        except Exception:
            raw_policy = DEFAULT_POLICY

        CAPABILITY_MATRIX = tuple(
            (r["tool_name"], r["expected_argument_key"], r["physical_effect"], tuple(r["boundary_constraint"]) if isinstance(r["boundary_constraint"], list) else r["boundary_constraint"])
            for r in raw_policy
        )

        proposal = json.loads(proposal_json_str)
        
        # 1. Protocol Structural Integrity Guards (Fail-Closed)
        if not isinstance(proposal, dict):
            return json.dumps({"verdict": "QUARANTINE", "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT", "details": "Unstructured payload blueprint."})

        tool_name = proposal.get("tool_name", None)
        arguments = proposal.get("arguments", {})

        if not isinstance(tool_name, str) or not isinstance(arguments, dict):
            return json.dumps({"verdict": "QUARANTINE", "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT", "details": "Invalid protocol type token."})

        # 2. Perimeter Access Control against Declarative Capability Matrix
        tool_clauses = tuple(cap for cap in CAPABILITY_MATRIX if cap[0] == tool_name)
        if not tool_clauses:
            return json.dumps({"verdict": "QUARANTINE", "violation_code": "PRIVILEGE_OVER_STEP", "details": f"Capability key '{tool_name}' denied."})

        if tool_name == "git_add" and not arguments:
            return json.dumps({"verdict": "QUARANTINE", "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT", "details": "git_add requires active path descriptors."})

        # 3. Hardened Physical Containment Rules (Pytest Alignment)
        for key, value in arguments.items():
            # 🔒 Pointer Injection Safeguard (Null Byte Execution Block)
            if isinstance(value, str) and "\\x00" in value:
                return json.dumps({
                    "verdict": "QUARANTINE",
                    "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT",
                    "details": f"Null byte detected within parameter '{key}'."
                })

            clause = next((c for c in tool_clauses if c[1] == key), None)
            
            if clause is None:
                if isinstance(value, str) and value.startswith(("http://", "https://")):
                    return json.dumps({
                        "verdict": "QUARANTINE",
                        "violation_code": "NETWORK_EXFILTRATION_ATTEMPT",
                        "details": f"Capability laundering signature detected: anomalous parameter '{key}' with network signature."
                    })
                return json.dumps({
                    "verdict": "QUARANTINE",
                    "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT",
                    "details": f"Schema mutation: parameter '{key}' not authorized for target capability '{tool_name}'."
                })

            expected_effect = clause[2]
            boundary = clause[3]

            if expected_effect == "FILESYSTEM":
                if not isinstance(value, str):
                    return json.dumps({"verdict": "QUARANTINE", "violation_code": "CAPABILITY_LAUNDERING", "details": "Primitive type confusion detected."})
                
                allowed_base = Path(boundary).resolve()
                requested_target = Path(value).resolve()
                
                # Real Path Traversal Mitigation
                if not requested_target.is_relative_to(allowed_base):
                    return json.dumps({
                        "verdict": "QUARANTINE",
                        "violation_code": "CAPABILITY_LAUNDERING",
                        "details": f"Host filesystem physical escape containment triggered on '{key}': {value}"
                    })
                
                # Strict Extension Validation (Case-Insensitive)
                if tool_name == "html_parser" and requested_target.suffix.lower() not in [".html", ".htm", ".json"]:
                    return json.dumps({
                        "verdict": "QUARANTINE",
                        "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT",
                        "details": f"File extension '{requested_target.suffix}' restricted for target capability {tool_name}."
                    })

            elif expected_effect == "NETWORK":
                if not isinstance(value, str):
                    return json.dumps({"verdict": "QUARANTINE", "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT", "details": "Invalid network token typing."})
                
                raw_domain = urlparse(value).netloc
                
                # 🔒 Network Homoglyph Attack Mitigation (IDN Punycode Enforced)
                try:
                    domain = raw_domain.encode('idna').decode('utf-8')
                except Exception:
                    domain = raw_domain

                if domain not in boundary:
                    return json.dumps({
                        "verdict": "QUARANTINE",
                        "violation_code": "NETWORK_EXFILTRATION_ATTEMPT",
                        "details": f"Egress network exfiltration intercepted synchronously (Punycode Enforced): {domain}"
                    })

        return json.dumps({"verdict": "ALLOW", "violation_code": "NONE", "details": "Capability request successfully validated against SSOT parameters."})
        
    except Exception as e:
        return json.dumps({"verdict": "QUARANTINE", "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT", "details": str(e)})
        `);
        
        pyodideReady = true;
        self.postMessage({ success: true, init_complete: true });
    } catch (err) {
        self.postMessage({ success: false, error: "Fatal WebAssembly Heap compilation error: " + err.message });
    }
}

self.onmessage = async (e) => {
    if (e.data.init_ping) {
        await initPyodideEngine();
        return;
    }

    if (!pyodideReady) {
        self.postMessage({ success: false, error: "Authorization core state remains uninitialized." });
        return;
    }

    try {
        const { proposal_str, policy_str } = e.data;
        
        // Direct bridge to the Pyodide isolated memory heap space
        pyodideInstance.globals.set("js_proposal_input", proposal_str);
        pyodideInstance.globals.set("js_policy_input", policy_str);
        
        const evaluationVerdictRaw = pyodideInstance.runPython("evaluate_agent_proposal(js_proposal_input, js_policy_input)");
        
        self.postMessage({ success: true, result: evaluationVerdictRaw });
    } catch (err) {
        self.postMessage({ success: false, error: "Python Core contract execution exception: " + err.message });
    }
};