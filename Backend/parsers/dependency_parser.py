def parse_dependency_check(report):
    findings = []
    for dependency in report.get("dependencies", []):
        for vuln in dependency.get("vulnerabilities", []):
            findings.append({
                "tool": "Dependency-Check",
                "package": dependency.get("package"),
                "severity": vuln["Severity"],
                "description": vuln["Description"],
                "cve_id": vuln["VulnerabilityID"],
            })
    return findings
