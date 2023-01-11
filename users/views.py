from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from django.contrib.auth.models import User

class Register(CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = RegisterSerializer