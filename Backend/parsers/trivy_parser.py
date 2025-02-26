def parse_trivy(report):
    findings = []
    for item in report:
        for vuln in item.get("Vulnerabilities", []):
            findings.append({
                "tool": "Trivy",
                "target": item["Target"],
                "package": vuln["PkgName"],
                "severity": vuln["Severity"],
                "description": vuln["Description"],
                "cve_id": vuln["VulnerabilityID"],
            })
    return findings
