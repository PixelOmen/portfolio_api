from django.conf import settings

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import email


class EmailTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = email.send_welcome_email(request, html=False)
        if result:
            return Response({'details': 'Email sent successfully'})
        else:
            return Response({'details': 'Email failed to send'}, status=500)


def display_email_template(request):
    context = {'user': request.user,
               'portfolio_link': settings.EMAIL_PORTFOLIO_LINK,
               'email_logo_url': settings.EMAIL_LOGO_URL}
    return render(request, 'email_template.html', context)
