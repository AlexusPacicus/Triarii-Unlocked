# hackaton_web/python/policy_engine.py
import json
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_POLICY = [
    {"tool_name": "brightdata_ingress", "expected_argument_key": "endpoint_api", "physical_effect": "NETWORK", "boundary_constraint": ["api.brightdata.com", "enterprise-egress.com"]},
    {"tool_name": "git_add", "expected_argument_key": "path", "physical_effect": "FILESYSTEM", "boundary_constraint": "./data/exports"},
    {"tool_name": "html_parser", "expected_argument_key": "path", "physical_effect": "FILESYSTEM", "boundary_constraint": "./data/exports"}
]

def evaluate_agent_proposal(proposal_json_str, policy_json_str=None):
    """
    Triarii Core Engine (Deterministic Execution Gateway).
    """
    try:
        # Dynamic matrix reconstruction from the analyst JSON input string
        raw_policy = json.loads(policy_json_str) if policy_json_str else DEFAULT_POLICY
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

        # 2. Perimeter Access Control to the Dynamic Capability Matrix
        tool_clauses = tuple(cap for cap in CAPABILITY_MATRIX if cap[0] == tool_name)
        if not tool_clauses:
            return json.dumps({"verdict": "QUARANTINE", "violation_code": "PRIVILEGE_OVER_STEP", "details": f"Capability key '{tool_name}' denied."})

        if tool_name == "git_add" and not arguments:
            return json.dumps({"verdict": "QUARANTINE", "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT", "details": "git_add requires active path descriptors."})

        # 3. HARDENED CAPABILITY ACTIVATION ENFORCEMENT
        for key, value in arguments.items():
            # 🔒 DEFENSIVE TDD GUARD: Immediate sanitization of null byte injections
            if isinstance(value, str) and "\x00" in value:
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
                
                try:
                    # Geographical Validation (Path Traversal / Sandbox Escape Containment)
                    if not requested_target.is_relative_to(allowed_base):
                        return json.dumps({
                            "verdict": "QUARANTINE",
                            "violation_code": "CAPABILITY_LAUNDERING",
                            "details": f"Host filesystem physical escape containment triggered on '{key}': {value}"
                        })
                    
                    # 🔒 MULTI-LAYER TDD RULE: Strict case-insensitive (.lower()) verification of compliant extensions
                    if tool_name == "html_parser" and requested_target.suffix.lower() not in [".html", ".htm", ".json"]:
                        return json.dumps({
                            "verdict": "QUARANTINE",
                            "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT",
                            "details": f"File extension '{requested_target.suffix}' restricted for target capability {tool_name}."
                        })
                        
                except AttributeError:
                    # Compatibility fallback for legacy runtimes lacking Path.is_relative_to
                    if requested_target != allowed_base and allowed_base not in requested_target.parents:
                        return json.dumps({"verdict": "QUARANTINE", "violation_code": "CAPABILITY_LAUNDERING", "details": f"Host filesystem physical escape containment triggered: {value}"})
                    
                    if tool_name == "html_parser" and requested_target.suffix.lower() not in [".html", ".htm", ".json"]:
                        return json.dumps({
                            "verdict": "QUARANTINE",
                            "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT",
                            "details": f"File extension '{requested_target.suffix}' restricted for target capability configuration."
                        })

            elif expected_effect == "NETWORK":
                if not isinstance(value, str):
                    return json.dumps({"verdict": "QUARANTINE", "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT", "details": "Invalid network token typing."})
                
                raw_domain = urlparse(value).netloc
                
                # 🔒 TRACK 3 HARDENING: Network Homoglyph Attack Mitigation (IDN Punycode Enforced)
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

        return json.dumps({"verdict": "ALLOW"})
        
    except Exception as e:
        return json.dumps({"verdict": "QUARANTINE", "violation_code": "ANOMALOUS_STRUCTURE_ATTEMPT", "details": str(e)})


def get_active_policy_schema():
    """
    Contractual schema exporter for the primary JavaScript thread (SSOT).
    Guarantees the client UI mirrors identical rule invariants tested via Pytest.
    """
    return json.dumps(DEFAULT_POLICY)