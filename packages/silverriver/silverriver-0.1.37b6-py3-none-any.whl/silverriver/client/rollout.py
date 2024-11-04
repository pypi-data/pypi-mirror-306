from silverriver.client.endpoint import Endpoint
from silverriver.interfaces.rollout import RolloutRequest, RolloutResult


class RolloutEndpoints:
    RUN_AGENT = Endpoint(
        path="/run_agent",
        method="POST",
        request_model=RolloutRequest,
        response_model=dict[str, RolloutResult],
    )
