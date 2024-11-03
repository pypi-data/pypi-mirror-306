from silverriver.client.endpoint import Endpoint
from silverriver.interfaces.data_models import LogsRequestModel


class TestsEndpoints:
    PREFIX = "/api/v1/tests"

    UPLOAD_TEST_PW_TRACE = Endpoint(prefix=PREFIX, path="/upload", method="POST",
                                    response_model=bool,
                                    request_model=LogsRequestModel)
