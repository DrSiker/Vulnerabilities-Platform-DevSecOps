def parse_snyk(report):
    findings = []
    for vuln in report.get("vulnerabilities", []):
        findings.append({
            "tool": "Snyk",
            "severity": vuln["severity"],
            "description": vuln["title"],
            "package": vuln.get("packageName"),
            "version": vuln.get("version"),
            "cwe_id": vuln.get("identifiers", {}).get("CWE", []),
            "cvss_score": vuln.get("cvssScore"),
        })
    return findings
