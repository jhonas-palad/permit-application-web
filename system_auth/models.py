from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager as UM
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

    


class UserManager(UM):

    def get_by_natural_key(self, email_user):
        
        if '@' in email_user and '.' in email_user:
            
            return self.get(email = email_user)
        else:
            
            return self.get(username = email_user)



class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length = 128)
    last_name = models.CharField(max_length = 128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add = True)



    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return f'User %s %s' %(self.first_name, self.last_name)

    def clean(self):
        super().clean()
        setattr(self, self.EMAIL_FIELD, type(self).objects.normalize_email(self.email))

    

    def get_full_name():
        pass
    
    def get_first_name():
        pass
    def send_email():
        pass




class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    GOVERNMENT_ID = (
        (1, "Driver's License"),
        (2, "Passpord"),
        (3, "Senior Citizen"),
        (4, "SSS ID"),
        (5, "COMELEC"),
        (6, "PhilID"),
        (7, "NBI Clearance"),
        (8, "Firearms License"),
        (9, "Pag-ibig"),
        (10, "PWD"),
        (11, "Barangay ID"),
        (12, "Phil-health ID"),
        (13, "Philippine Postal ID"),
        (14, "Other valid government-issued IDs"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(_('Phone Number'), max_length = 12, )
    gender = models.CharField(_('Gender'), max_length=2, choices = GENDER)
    gov_id_type = models.CharField(_('Government ID type'), max_length = 1, choices=GOVERNMENT_ID)
    id_ref = models.CharField(_('ID ref no.'), max_length = 128)
    id_img = models.ImageField(_('ID image'),upload_to = 'gov_ids')


