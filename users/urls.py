from django.urls import include,path
from .views import Register

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('register/', Register.as_view()),
]