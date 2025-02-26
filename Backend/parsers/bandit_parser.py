import json

def parse_bandit(report):
    findings = []
    for issue in report.get("results", []):
        findings.append({
            "tool": "Bandit",
            "filename": issue["filename"],
            "line": issue["line_number"],
            "severity": issue["issue_severity"],
            "description": issue["issue_text"],
            "test_name": issue["test_name"],
            "cwe_id": issue.get("issue_cwe", {}).get("id"),
        })
    return findings
