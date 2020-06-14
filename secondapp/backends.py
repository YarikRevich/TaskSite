from django.contrib.auth.models import User



class EmailAndPasswordBackend(object):

    def authenticate(self,username=None,password=None,**kwargs):
        try:
            User.objects.get(email=username,password=password) 
        except User.MultipleObjectsReturned:
            User.objects.filter(email=username,password=password).first() 
        except User.DoesNotExist:
            return None
        if getattr(User,"is_active") and User.check_password(password):
            return User
        return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)  
        except User.DoesNotExist:
            return None          