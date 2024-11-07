"""Context class for keeping track of the conversation state in Redis."""

from typing import Any

from redis import asyncio as redis

from lego.lego_types import JSONDict, Messages
from lego.models import ReprEnum
from lego.settings import RedisConnection


class RedisContext:
    """Redis conversation context."""

    def __init__(self, conversation_id: str, connection: RedisConnection):
        self.redis = redis.from_url(connection.url())
        ## It may be a better option to use the following instead
        ## since no need to use urllib.parse.unquote_plus?
        # self.redis = redis.Redis(
        #     host=connection.host,
        #     port=connection.port,
        #     db=connection.db,
        #     password=connection.password,
        # )
        self.redon = self.redis.json()
        self.convid = conversation_id

    async def init(self) -> None:
        """Initialize the conversation context."""
        await self.redon.set(self.convid, "$", {}, nx=True)
        await self.redon.set(self.convid, "$.state", {}, nx=True)
        await self.redon.set(self.convid, "$.export", {}, nx=True)
        await self.redon.set(self.convid, "$.messages", [], nx=True)

    async def session_info(self) -> tuple[str, str, float] | None:
        """Return the session info."""
        ## FIXME: unpacking tuple needs too much caution.
        if not (session_id := await self.get("session_id")):
            return None

        if not (token := await self.get("access_token")):
            raise KeyError("Access token is missing.")

        return token, session_id, await self.redis.ttl(self.convid)

    async def set_session(
        self, access_token: str, session_id: str, expires_in: float
    ):
        """Set the session info."""
        await self.set_("session_id", session_id)
        await self.set_("access_token", access_token)
        await self.redis.expire(self.convid, int(expires_in))

    async def state(self) -> JSONDict:
        """Return info extracted during the conversation."""
        res = await self.redon.get(self.convid, "$.state")
        return res[0]

    async def export(self) -> JSONDict:
        """Return what was registered for export."""
        res = await self.redon.get(self.convid, "$.export")
        return res[0]

    async def messages(self) -> Messages:
        """Return the conversation history."""
        res = await self.redon.get(self.convid, "$.messages")
        return res[0]

    async def set_(
        self,
        key: str | ReprEnum,
        value: Any,  # type: ignore[misc]
        export: bool = False,
    ):
        """Set a key-value pair in the conversation state."""
        await self.redon.set(self.convid, f"$.state.{key}", value)
        if export:
            await self.redon.set(self.convid, f"$.export.{key}", value)

    async def count(self, key: str | ReprEnum) -> int:
        """Return the number of elements in a list."""
        if counter := await self.get(key):
            if not isinstance(counter, int):
                raise TypeError("Counter is not an integer.")
        else:
            await self.set_(key, 1)
        res = await self.redon.numincrby(self.convid, f"$.state.{key}", 1)  # type: ignore[no-untyped-call]
        return res[0]

    async def get(  # type: ignore[misc]
        self, key: str | ReprEnum, fallback_value: Any = None
    ) -> Any:
        """Get a key-value pair from the conversation state."""
        result = await self.redon.get(self.convid, f"$.state.{key}")
        return result[0] if result else fallback_value

    async def save_message(self, message: dict[str, str]):
        """Append a message to the conversation history list."""
        await self.redon.arrappend(self.convid, "$.messages", message)  # type: ignore[misc]

    async def last_message(self) -> dict[str, str]:
        """Return the last message in the conversation history."""
        if result := await self.redon.get(self.convid, "$.messages[-1]"):
            return result[0]
        raise IndexError("Empty message history.")
