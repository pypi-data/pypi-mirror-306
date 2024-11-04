import logging

from openinference.instrumentation import TraceConfig
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.trace import get_tracer_provider

from silverriver.client.http_client import HTTPCruxClient
from silverriver.interfaces import AgentAction, NOOP_ACTION, SupportedModes, BrowserType
from silverriver.interfaces.browsergym_observation import BrowsergymObservation
from silverriver.interfaces.chat import AgentChatInterface
from silverriver.interfaces.data_models import BrowserObservation, Observation
from silverriver.utils.execution import execute_python_code

API_HOST = "crux.silverstream.ai"
API_PORT = 31337
API_SERVER_URL = f"https://{API_HOST}:{API_PORT}"

logger = logging.getLogger(__name__)

OpenAIInstrumentor().instrument(tracer_provider=get_tracer_provider(), config=TraceConfig())


class BrowserSession:
    """
    Represents a browser session in the cloud for the agent to interact with.

    This class manages interactions with a remote browser session,
    code execution, and observation retrieval.
    """

    def __init__(self, client: HTTPCruxClient, chat_module: AgentChatInterface, browser_type: BrowserType):
        self._client = client
        self.browser_type = browser_type
        self.remote_page = None
        self.chat_module = chat_module

    def _validate_obs(self, transition):
        if self.browser_type == BrowserType.SOTA:
            obs = Observation(
                **transition.obs,
                chat_messages=[],
                last_action_error="",
            )
        elif self.browser_type == BrowserType.BROWSERGYM:
            obs = BrowsergymObservation(**transition.obs)
        else:
            raise ValueError(f"Unknown browser type {self.browser_type}")
        return obs

    def reset(self, start_url: str) -> (BrowserObservation | BrowsergymObservation, dict):
        """
        Reset the browser session with a new starting URL.

        Args:
            start_url (str): The URL to start the session with.

        Returns:
            BrowserObservation: The observation after resetting the session.
            dict: Additional metadata.
        """
        setup = self._client.env_setup(start_url=start_url, browser_type=self.browser_type)
        self.remote_page = setup.exec_context["page"]

        transition = self._client.internal_step(NOOP_ACTION)
        obs = self._validate_obs(transition)
        return obs, transition.info

    def execute(self, code: str) -> BrowserObservation:
        """
        Execute Python code in the context of the browser session.

        This method runs the provided code, posts the action to the client,
        and returns the resulting browser observation.

        Args:
            code (str): The Python code to execute.

        Returns:
            BrowserObservation: The observation after executing the code.
        """
        if self.browser_type == BrowserType.SOTA:
            execute_python_code(
                code, execution_context={
                    "page": self.remote_page,
                    "chat": self.chat_module,
                })
        else:
            logger.warning(
                "BrowserGym does not support remote code execution, the action will be executed remotely.")
        action = AgentAction(code=code)
        ret = self._client.internal_step(action)
        return self._validate_obs(ret)


class Crux:
    """
    Main client for interacting with the Crux API.

    This class provides methods to create browser sessions and retrieve agent actions.
    """

    def __init__(self, api_key: str, base_url: str = API_SERVER_URL):
        self.client = HTTPCruxClient(api_key=api_key, base_url=base_url)

    def create_browser_session(self, start_url: str, chat, browser_type: BrowserType = BrowserType.SOTA) -> tuple[
        BrowserSession, Observation | BrowsergymObservation, dict]:
        """
        Create a new browser session.

        Args:
            start_url (str): The URL to start the session with.
            chat: The chat interface for agent-user communication.
            browser_type (BrowserType): The type of browser to use, either SOTA (default, performance) or BrowserGym (reproducibility).

        Returns:
            tuple: A tuple containing the BrowserSession, initial BrowserObservation, and additional info.
                session: is the BrowserSession to control the browser remotely, BrowserObservation contains all the
                relevant information for decision making, while info contains metadata which is likely not interesting
                to the agent.
        """
        session = BrowserSession(client=self.client, chat_module=chat, browser_type=browser_type)
        obs, info = session.reset(start_url=start_url)
        return session, obs, info

    def get_action(self, obs: Observation, mode: SupportedModes, interactive) -> AgentAction:
        """
        Get the next action from the agent based on the current observation.

        Args:
            obs (Observation): The current observation of the environment.
            mode (SupportedModes): The mode to use for generating the action. See SupportedModes for available options.
            interactive (bool): Whether the agent can interact with the user.

        Returns:
            str: The code representing the next action to take.
        """
        if isinstance(obs, BrowserObservation) and not isinstance(obs, Observation):
            raise ValueError("The agent needs to be informed of the chat messages, use Observation instead.")
        return self.client.agent_get_action(obs, mode, interactive)

    def upload_logs(self, prefix: str, blob: bytes):
        return self.client.upload_logs(prefix, blob)

    def close(self):
        self.client.env_close()
        self.client.agent_close()
