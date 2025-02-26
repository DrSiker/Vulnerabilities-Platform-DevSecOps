def parse_gitleaks(report):
    findings = []
    for leak in report.get("Leaks", []):
        findings.append({
            "tool": "Gitleaks",
            "description": leak["Rule"],
            "severity": "CRITICAL",
            "file": leak["File"],
        })
    return findings
