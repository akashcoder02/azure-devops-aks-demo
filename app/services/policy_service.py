from security.policies.policy_engine import (
    policy_engine
)

from services.devsecops import (
    devsecops_service
)


class PolicyService:

    def evaluate(self):

        results = (
            devsecops_service
            .get_application_security()
        )

        return policy_engine.evaluate(
            results
        )


policy_service = PolicyService()