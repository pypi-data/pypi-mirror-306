from mindcontrol_types import PromptV1
from typing import List, Optional
from ..client import MindControl
from ..types import TemplateVars
from .types import Adapter, ProviderKeys, Version, VersionVariant
from .error import MissingAdapter


class MindControlWrapper:
    """Mind Control wrapper class."""

    adapters: List[Adapter]
    """List of active adapters."""
    keys: ProviderKeys
    """Provider keys."""
    client: MindControl
    """Mind Control client instance."""
    collection_id: str
    """Collection id."""
    payload: str
    """The payload JSON."""
    major: int
    """Major version number."""
    minor: int
    """Minor version number."""
    version: VersionVariant
    """Version variant."""
    direct: bool
    """If to use the direct API. If omitted, the default value will be used."""

    def __init__(
        self,
        adapters: List[Adapter],
        keys: ProviderKeys,
        token: str,
        collection_id: str,
        payload: str,
        major: int,
        minor: int,
        version: VersionVariant = "published",
        direct: bool = False,
    ):
        """Wrapper constructor.

        :param adapters: List of active adapters.
        :param keys: Provider keys.
        :param token: Mind Control API token.
        :param collection_id: Collection id.
        :param payload: The payload JSON.
        :param major: Major version number.
        :param minor: Minor version number.
        :param version: Version variant.
        :param direct: If to use the direct API. If omitted, the default value
        will be used."""

        self.adapters = adapters
        self.keys = keys
        self.client = MindControl(token)
        self.collection_id = collection_id
        self.payload = payload
        self.major = major
        self.minor = minor
        self.version = version
        self.direct = direct

    async def exec(
        self,
        name: str,
        vars: Optional[TemplateVars] = None,
        version: Optional[VersionVariant] = None,
        direct: Optional[bool] = None,
    ) -> str:
        """Executes the given prompt or chain using one of the active
        adapters

        :param name: Prompt or chain name to execute.
        :param vars: Variables to use in the prompt or chain.
        :param version: Version variant (tag or "exact").
        :param direct: If to use the direct API. If omitted, the default value
        will be used.

        :returns: Result of the prompt execution."""

        collection = self.client.collection(
            self.collection_id,
            **self.resolve_version(version, direct),
        )

        async def interop(prompt: PromptV1) -> str:
            for adapter in self.adapters:
                response = await adapter(self.keys, prompt)
                if response is not None:
                    return response

            raise MissingAdapter("No adapter matched the prompt.")

        return await collection.exec(name, interop=interop, vars=vars)

    def resolve_version(
        self,
        version: Optional[VersionVariant] = None,
        direct: Optional[bool] = None,
    ) -> Version:
        """Resolves the version variant.

        :param version: Version variant (tag or "exact").
        :param direct: If to use the direct API. If omitted, the default value
        will be used.

        :returns: Version dict."""

        version = version or self.version
        direct = direct if direct is not None else self.direct

        match version:
            case "published":
                return Version(
                    major=self.major, minor=None, tag="published", direct=direct
                )

            case "any":
                return Version(major=self.major, minor=None, tag="any", direct=direct)

            case "exact":
                return Version(
                    major=self.major, minor=self.minor, tag=None, direct=direct
                )
