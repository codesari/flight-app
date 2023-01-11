from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    # required=True,zorunlu alan
    # UniqueValidator,field'ın eşsiz olması için.
    password = serializers.CharField(
        write_only=True,
        # required = True,
        validators = [validate_password],
        style = {"input_type" : "password"}
        )
    # write_only,GET işlemi oldugu zaman password gözükmesin
    password2 = serializers.CharField(
        write_only=True,
        # required=True,
        validators = [validate_password],
        style = {"input_type" : "password"}
        )
    # required=True'yu password2'de yazıyorum.password zaten db'de zorunlu alan,o olmadan kullanıcı oluşturulmuyor,fakat,password2 db'de olmadığı için ona required=True dedik.
    # özet :
    # 2 tane field'ın özelligini degistirdim (email ve password)
    # 1 tane field ekledim (password2)

    class Meta:
        model=User
        fields=(
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2'
        )
        # içeriği değişmeyecek collections'ları tuple formatinda yazmak best-practice ve daha hızlı çalışır.
    
    
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Password fields did not match'}
            )
        return data

    # ! validated_data,yukarıda validation işleminden geçmiş data demek.

    def create(self,validated_data):
      
        validated_data.pop('password2')
         # password2'yi db'ye göndermiyoruz
        password=validated_data.pop('password')
        # ? pop fonksiyonunu değişkene atarsak,çıkarılan elemanı değişkene atar
        # password u daha sonra hash'leyip göndermek için değişkene atadık.
        # user olusturuyorum
        user=User.objects.create(**validated_data)
        # **validated_data alttaki kodu kısaltıyor (ilgili field'ları map ediyor)
        #  username=validate_data['username], email = va.......
        # password olusturup hash'liyorum
        user.set_password(password)
        # password ün encrypte olarak db ye kaydedilmesiniş sağlıyor.
        user.save()
        return user

