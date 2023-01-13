from rest_framework import permissions
# ! permissions'lar True yada False döner
class IsStafforReadOnly(permissions.IsAdminUser):
    # IsAdminUser'dan miras aldık
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
            # SAFE_METHODS --> data'da değişiklik yapmayan metodlar.get gibi
            # eğer GET metodu ise True dön,değilse diğer metodlar için adminse True dön 
        return bool(request.user and request.user.is_staff)
    
