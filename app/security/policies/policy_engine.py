from security.config_loader import (
    config_loader
)


class PolicyEngine:

    def __init__(self):

        self.config = config_loader.load()

    def evaluate(self, results):

        policy = self.config["policy"]

        critical = 0
        high = 0

        for scanner in results.values():

            if isinstance(scanner, dict):

                critical += scanner.get(
                    "critical",
                    0
                )

                high += scanner.get(
                    "high",
                    0
                )

        blocked = False
        reasons = []

        if (
            policy["block_on_critical"]
            and critical > 0
        ):

            blocked = True

            reasons.append(
                "Critical vulnerabilities detected."
            )

        if high > policy["high_threshold"]:

            reasons.append(
                "High vulnerability threshold exceeded."
            )

        return {

            "mode": policy["mode"],

            "blocked": blocked,

            "critical": critical,

            "high": high,

            "reasons": reasons

        }


policy_engine = PolicyEngine()

if __name__ == "__main__":

    from security.orchestrator import (
        devsecops_orchestrator
    )

    results = (
        devsecops_orchestrator
        .application_security()
    )

    policy = policy_engine.evaluate(
        results
    )

    print("=" * 50)
    print("DevSecOps Policy Evaluation")
    print("=" * 50)
    print(policy)
    print("=" * 50)

    import sys

    if policy["blocked"]:

        print("❌ Deployment Blocked")

        sys.exit(1)

    print("✅ Deployment Approved")

    sys.exit(0)