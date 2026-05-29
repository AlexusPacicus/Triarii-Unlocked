# hackaton_web/test/test_policy_engine.py
import json
from python.policy_engine import evaluate_agent_proposal

def test_compliant_action_allowed(adversarial_payloads):
    """TC-01: Assures a legitimate filesystem action inside the isolated sandbox boundary returns ALLOW."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["legitimate"]))
    assert result["verdict"] == "ALLOW"

def test_compliant_url_allowed(adversarial_payloads):
    """TC-02: Assures a legitimate outbound network action targeting an authorized domain returns ALLOW."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["legitimate_url"]))
    assert result["verdict"] == "ALLOW"

def test_path_traversal_laundering_quarantined(adversarial_payloads):
    """TC-03: Synchronous mid-flight interception of legacy directory traversal sandbox escapes."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["path_traversal"]))
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "CAPABILITY_LAUNDERING"

def test_prefix_clipping_evasion_blocked(adversarial_payloads):
    """TC-04: Blocks partial text-prefix clipping evasion techniques targeting boundary path definitions."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["prefix_evasion"]))
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "CAPABILITY_LAUNDERING"

def test_nested_schema_mutation_quarantined(adversarial_payloads):
    """TC-05: Captures and contains structural modifications engineered via indirect prompt injections (IDPI)."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["nested_schema_mutation"]))
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "ANOMALOUS_STRUCTURE_ATTEMPT"

def test_type_confusion_arrays_fail_closed(adversarial_payloads):
    """TC-06: Enforces a fail-closed status when input parameter types violate expected primitive types."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["type_confusion_attack"]))
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "CAPABILITY_LAUNDERING"

def test_network_exfiltration_quarantined(adversarial_payloads):
    """TC-06b: Intercepts unauthorized outbound network data exfiltration traffic strings (EchoLeak)."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["network_exfiltration"]))
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "NETWORK_EXFILTRATION_ATTEMPT"

def test_missing_parameter_fail_closed(adversarial_payloads):
    """TC-07: Defensively enforces a fail-closed status when mandatory contract arguments are completely omitted."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["missing_mandatory_parameter"]))
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "ANOMALOUS_STRUCTURE_ATTEMPT"

def test_malformed_root_layout_blocked(adversarial_payloads):
    """TC-08: Dispatches an immediate fail-closed quarantine verdict if the root element is not a structured dictionary object."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["malformed_root"]))
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "ANOMALOUS_STRUCTURE_ATTEMPT"

def test_unauthorized_tool_execution_blocked(adversarial_payloads):
    """TC-09: Verifies zero-trust boundary isolation against unregistered capability keys or missing tool configurations."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["unauthorized_tool"]))
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "PRIVILEGE_OVER_STEP"

def test_hot_patching_policy_revocation(adversarial_payloads):
    """TC-10: Verifies runtime hot-patching reconfigurations. 
    If SecOps dynamically revokes a capability key from the active matrix, 
    subsequent agential invocations must be rejected immediately."""
    
    # Compliant payload that nominally resolves to ALLOW state parameters (git_add within ./data/exports)
    payload = adversarial_payloads["legitimate"]
    
    # Construct a highly restrictive runtime hot-patched policy surface that purges 'git_add' permissions
    restrictive_policy = json.dumps([
        {"tool_name": "brightdata_ingress", "expected_argument_key": "endpoint_api", "physical_effect": "NETWORK", "boundary_constraint": ["api.brightdata.com"]}
    ])
    
    # Evaluate the proposal payload against the injected dynamic restriction model
    result = json.loads(evaluate_agent_proposal(payload, restrictive_policy))
    
    # Assert that the deterministic WASM checkpoint catches the revocation pattern instantly
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "PRIVILEGE_OVER_STEP"    

def test_html_parser_disallowed_extension_quarantined():
    """
    TC-11: Validates that the html_parser engine blocks unauthorized execution formats (such as .sh)
    even when located inside compliant target directory path structures.
    """
    # Create a malicious payload pointing to a shell execution script inside the allowed suffix folder
    malicious_payload = json.dumps({
        "tool_name": "html_parser",
        "arguments": {"path": "./data/exports/reverse_shell.sh"}
    })
    
    # Process the suspicious intent sequence against the core decision checkpoint
    result = json.loads(evaluate_agent_proposal(malicious_payload))
    
    # Require an immediate transition into the secure isolated quarantine buffer
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "ANOMALOUS_STRUCTURE_ATTEMPT"

def test_null_byte_injection_quarantined(adversarial_payloads):
    """TC-12: Captures and isolates runtime null byte injections within string path arguments to prevent pointer manipulation."""
    result = json.loads(evaluate_agent_proposal(adversarial_payloads["null_byte_attack"]))
    
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "ANOMALOUS_STRUCTURE_ATTEMPT"

def test_html_parser_uppercase_disallowed_extension_quarantined():
    """TC-14: Assures case-insensitive verification algorithms block restricted extensions using alternative casing (.SH)."""
    malicious_payload = json.dumps({
        "tool_name": "html_parser",
        "arguments": {"path": "./data/exports/reverse_shell.SH"} # Casing bypass testing vector
    })
    
    result = json.loads(evaluate_agent_proposal(malicious_payload))
    
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "ANOMALOUS_STRUCTURE_ATTEMPT"

def test_network_homoglyph_attack_quarantined():
    """TC-15: Blocks structural network spoofing and egress attempts engineered via IDN Unicode homoglyph attacks."""
    # Data exfiltration using a Cyrillic 'а' (\u0430) char substitute instead of standard Latin 'a'
    homoglyph_url = "https://аpi.brightdata.com/v1/exfiltrate"
    
    malicious_payload = json.dumps({
        "tool_name": "brightdata_ingress",
        "arguments": {"endpoint_api": homoglyph_url}
    })
    
    result = json.loads(evaluate_agent_proposal(malicious_payload))
    
    # Verify the network exfiltration vector triggers quarantine under Punycode translation parsing
    assert result["verdict"] == "QUARANTINE"
    assert result["violation_code"] == "NETWORK_EXFILTRATION_ATTEMPT"