import json
import uuid
from typing import TYPE_CHECKING

from asgiref.sync import sync_to_async

from django.apps import apps
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncWebsocketConsumer

from .openaichat import stream_response, SYSTEM_MESSAGE

if TYPE_CHECKING:
    from wschat.models import UserChat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await self._get_user_from_token(
            self.scope["cookies"].get("access_token")
        )
        if user is None:
            await self.accept()
            await self.close(code=1008, reason="User is not authenticated")
        else:
            self.scope["user"] = user
            self.scope["max_chat_messages"] = await self._get_max_chat_messages()
            self.scope["session_id"] = str(uuid.uuid4())
            await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        userchat = await self._get_user_chat()
        if not await self._allowed_to_chat(userchat.count):
            return
        userchat.count += 1
        await sync_to_async(userchat.save)()

        messages = cache.get(self.scope["session_id"], [])
        if not messages:
            messages = [SYSTEM_MESSAGE]
        messages.append({"role": "user", "content": text_data})

        try:
            response = await self._send_stream_response(messages)
            await self._send_end_stream()
        except Exception as e:
            await self._send_exception(e)
        else:
            messages.append({"role": "assistant", "content": response})

        cache.set(self.scope["session_id"], messages, timeout=60 * 60)  # 1 hour

    # ------------------ Helper methods -------------------
    # -----------------------------------------------------
    # -----------------------------------------------------
    # -----------------------------------------------------

    async def _send_exception(self, e: Exception) -> None:
        await self.send(
            text_data=json.dumps(
                {
                    "type": "data",
                    "payload": "",
                    "error": str(e),
                }
            )
        )

    async def _send_end_stream(self) -> None:
        await self.send(
            text_data=json.dumps(
                {
                    "type": "endStream",
                    "payload": "",
                }
            )
        )

    async def _send_stream_response(self, messages: list[dict[str, str]]) -> str:
        response = ""
        async for chunk in stream_response(messages):
            response += chunk["content"]
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "stream",
                        "payload": chunk["content"],
                        "chatID": chunk["chat_id"],
                    }
                )
            )
        return response

    async def _allowed_to_chat(self, count: int) -> bool:
        if count >= self.scope["max_chat_messages"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "data",
                        "payload": "",
                        "error": "You have reached the daily chat limit",
                    }
                )
            )
            return False
        return True

    async def _get_user_chat(self) -> "UserChat":
        UserChat = apps.get_model("wschat", "UserChat")
        user = self.scope["user"]
        userchat, _ = await sync_to_async(UserChat.objects.get_or_create)(user_id=user)
        return userchat  # type: ignore

    async def _get_max_chat_messages(self) -> int:
        UserLimits = apps.get_model("core", "UserLimits")
        default_limits = await sync_to_async(UserLimits.objects.get)(name="default")
        return default_limits.max_chat_messages  # type: ignore

    async def _get_user_from_token(self, token) -> int | None:
        if token is None:
            return None

        # Needs to be here to let app load
        from oauth2_provider.models import AccessToken

        # Only used to catch "DoesNotExist" exception properly
        UserModel = await sync_to_async(get_user_model())()

        try:
            valid_token = await sync_to_async(AccessToken.objects.get)(
                token=token,
                expires__gt=timezone.now(),
            )
            return valid_token.user_id  # type: ignore
        except (AccessToken.DoesNotExist, UserModel.DoesNotExist, KeyError):
            return None
