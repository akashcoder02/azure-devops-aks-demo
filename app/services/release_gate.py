from services.policy_service import (
    policy_service
)


class ReleaseGate:

    def evaluate(self):

        policy = policy_service.evaluate()

        if policy["blocked"]:

            return {

                "success": False,

                "message": "Deployment blocked.",

                "policy": policy

            }

        return {

            "success": True,

            "message": "Deployment approved.",

            "policy": policy

        }


release_gate = ReleaseGate()