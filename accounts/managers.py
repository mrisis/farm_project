from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self,mobile_number,password):
        if not mobile_number:
            raise ValueError('user must have be mobile number')


        user = self.model(mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self,mobile_number,password):
        user = self.create_user(mobile_number,password)
        user.is_admin=True
        user.is_superuser = True
        user.save(using=self._db)
        return user