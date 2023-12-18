from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Chat
from rest_framework import status, viewsets
from django.http import Http404

class CustomPagination(PageNumberPagination):
    page_size = 10  # Define el número de mensajes por página
    page_size_query_param = 'page_size'
    max_page_size = 100

#8. Endpoint /api/canales/chats/
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

# 9. Endpoint /api/canales/mensajes/
class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all().order_by('id') 
    serializer_class = MensajeSerializer
    pagination_class = CustomPagination

# 10. Endpoint /api/chats/<chat_id>/mensajes/
class MensajePorChatView(APIView):
    def get(self, request, chat_id, format=None):
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        mensajes = Mensaje.objects.filter(chat=chat)
        serializer = MensajeSerializer(mensajes, many=True)
        return Response(serializer.data)
    
# 11. Endpoint /api/chats/<chat_id>/mensajes/<username>/
class MensajePorChatYUsuarioView(APIView):
    def get(self, request, chat_id, username, format=None):
        try:
            chat = Chat.objects.get(pk=chat_id)
            user = User.objects.get(username=username)
        except (Chat.DoesNotExist, User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        mensajes = Mensaje.objects.filter(chat=chat, user=user)
        serializer = MensajeSerializer(mensajes, many=True)
        return Response(serializer.data)
