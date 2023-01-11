from django.contrib.auth.models import User
# register olduğumuzda User tablosunda kayıt ediliyor
from django.db.models.signals import post_save
# kayıt edildikten sonra sinyali gönder (post_save --> kayıt sonrası)
from django.dispatch import receiver
# sinyali yakala (receiver)
from rest_framework.authtoken.models import Token
# üretilen token'ların tutulduğu token tablosu

@receiver(post_save, sender=User)
def create_Token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


