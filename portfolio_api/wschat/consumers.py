from asgiref.sync import sync_to_async

from django.utils import timezone
from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await self.get_user_from_token(self.scope["cookies"].get("access_token"))
        if user is None:
            await self.accept()
            await self.close(code=1008, reason="User is not authenticated")
        else:
            self.scope["user"] = user
            await self.accept()

    async def receive(self, text_data):
        pass

    async def send_message(self, text_data):
        await self.send(text_data)

    async def disconnect(self, close_code):
        pass

    async def get_user_from_token(self, token):
        # Needs to be here to let app load
        from oauth2_provider.models import AccessToken

        # Only used to catch "DoesNotExist" exception properly
        UserModel = await sync_to_async(get_user_model())()

        try:
            valid_token = await sync_to_async(AccessToken.objects.get)(
                token=token,
                expires__gt=timezone.now(),
            )

            # Can't user "Manager" (objects.get) from UserModel,
            # need to use `get_user_model` again
            user = await sync_to_async(get_user_model().objects.get)(
                id=valid_token.user_id  # type: ignore
            )

            return user
        except (AccessToken.DoesNotExist, UserModel.DoesNotExist, KeyError):
            return None
