import requests

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class GoogleAuthToTokenView(APIView):
    def post(self, request):
        code = request.data.get('code')
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        client_secret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
        redirect_uri = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI

        token_url = settings.SOCIAL_AUTH_GOOGLE_AUTHCODE_TOKEN_URL
        token_data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        if access_token:
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to obtain Google access token"}, status=status.HTTP_400_BAD_REQUEST)
