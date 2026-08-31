from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import bot


class AsyncMessages:
    def __init__(self, messages):
        self._messages = messages

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._messages:
            raise StopAsyncIteration
        return self._messages.pop(0)


@pytest.mark.asyncio
async def test_delete_old_messages_skips_bot_and_redacts_content():
    own_message = SimpleNamespace(author=bot.bot.user, delete=AsyncMock(), id=1)
    other_message = SimpleNamespace(
        author=object(), delete=AsyncMock(), id=2, content="must-not-be-logged"
    )
    channel = SimpleNamespace(
        id=10,
        history=lambda **_: AsyncMessages([own_message, other_message]),
    )

    with patch.object(bot.asyncio, "sleep", new=AsyncMock()):
        deleted = await bot.delete_old_messages_in_channel(channel)

    assert deleted == 1
    own_message.delete.assert_not_awaited()
    other_message.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_old_messages_handles_forbidden():
    response = SimpleNamespace(status=403, reason="Forbidden")
    forbidden = bot.discord.Forbidden(response, "denied")
    message = SimpleNamespace(
        author=object(), delete=AsyncMock(side_effect=forbidden), id=2
    )
    channel = SimpleNamespace(id=10, history=lambda **_: AsyncMessages([message]))

    assert await bot.delete_old_messages_in_channel(channel) == 0


def test_main_requires_token(monkeypatch):
    monkeypatch.delenv("DISCORD_TOKEN", raising=False)
    with pytest.raises(SystemExit, match="DISCORD_TOKEN is required"):
        bot.main()
