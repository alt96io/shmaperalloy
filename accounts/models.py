from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

fs = FileSystemStorage()

class MemberManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email:
            raise ValueError("Members must have an email address")
        if not password:
            raise ValueError("Members must have a password")
        member = self.model(
            email = self.normalize_email(email)
        )
        member.set_password(password) # change member password
        member.staff = is_staff
        member.admin = is_admin
        member.active = is_active
        member.save(using=self._db)
        return  member

    def create_staffuser(self, email, password=None):
        member = self.create_user(
            email,
            password=password,
            is_staff=True,
        )
        return  member

    def create_superuser(self, email, password=None):
        member = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return  member

# class User(AbstractBaseUser, PermissionsMixin):
class Member(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    active      = models.BooleanField(default=True) # can login
    staff       = models.BooleanField(default=False) # can create documents
    admin       = models.BooleanField(default=False) # can create/modify    member accounts
    confirm     = models.BooleanField(default=False)  # confirmed email

    USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []

    objects = MemberManager()

    def __str__(self):
        return self.email

#    def get_full_name(self):
#        full_name = self.first_name + " " + self.last_name
#        return full_name
    
#    def get_short_name(self):
#        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

    @property
    def confirmed_email(self):
        return self.confirm

class Profile(models.Model):
    member      = models.OneToOneField(Member, on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=255, blank=True)
    last_name   = models.CharField(max_length=255, blank=True)
    address     = models.CharField(max_length=255, blank=True)
    cell_phone  = models.CharField(max_length=15, blank=True)
    home_phone  = models.CharField(max_length=15, blank=True)
    work_phone  = models.CharField(max_length=15, blank=True)
    photo       = models.ImageField(default='report/chewbaccaheadshot.jpeg', upload_to='profilePics/')

    def __str__(self):
        return f'{self.first_name} {self.last_name} Profile'
