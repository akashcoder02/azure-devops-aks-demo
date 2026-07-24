class SecurityScore:

    def calculate(self, dashboard):

        score = 100

        scanners = [

            dashboard["application"].get("gitleaks", {}),
            dashboard["application"].get("semgrep", {}),
            dashboard["application"].get("pip-audit", {}),
            dashboard["application"].get("trivy", {}),
            dashboard["application"].get("kubernetes", {}),

            dashboard["platform"].get("checkov", {}),
            dashboard["platform"].get("aks", {})

        ]

        for scanner in scanners:

            critical = scanner.get("critical", 0)
            findings = scanner.get("findings", 0)

            score -= critical * 10
            score -= findings

        score = max(score, 0)

        return {

            "score": score,

            "grade": self.grade(score)

        }

    def grade(self, score):

        if score >= 95:
            return "A+"

        elif score >= 90:
            return "A"

        elif score >= 80:
            return "B"

        elif score >= 70:
            return "C"

        return "D"


security_score = SecurityScore()