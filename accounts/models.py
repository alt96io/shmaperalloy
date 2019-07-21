from django.core.files.storage import FileSystemStorage
from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
)
from PIL import Image

fs = FileSystemStorage()

class MemberManager(BaseUserManager):
    use_in_migrations = True

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
        return member

#create member that can create documents
    def create_staffuser(self, email, password=None):
        member = self.create_user(
            email,
            password=password,
            is_staff=True,
        )
        return  member

#create member with admin rights
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
    ## USERNAME_FIELD AND PASSWORD ARE REQUIRED BY DEFAULT
    REQUIRED_FIELDS = []

 #   objects = models.Manager()
 #   objects_active = MemberManager()
    objects = MemberManager()

    def __str__(self):
        return self.email

    def full_name(self):
        fullname = self.profile.first_name + " " + self.profile.last_name
        return fullname
    
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

#class Role(models.Model):
#    ROLE_CHOICES = (
#        ('O', 'Owner'),
#        ('C', 'Contributor'),
#        ('V', 'Viewer'),
#    )
#    assigned_role        = models.CharField(max_length=1, choices=ROLE_CHOICES, null=True)
#    member      = models.ManyToManyField(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='member_role')
#    doc         = models.ManyToManyField(Docname, on_delete=models.SET_NULL, null=True, blank=True, related_name='doc_role')

#    @classmethod
#    def assign_contributor(cls, selected_role, current_document, selected_member):
#        role, created = cls.objects.get_or_create(
#            selected_role = 'C'
#        )
#        role.member.add(selected_member)
#        role.doc.add(current_document)

class Profile(models.Model):
    member      = models.OneToOneField(Member, on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=255, blank=True)
    last_name   = models.CharField(max_length=255, blank=True)
    address     = models.CharField(max_length=255, blank=True)
    cell_phone  = models.CharField(max_length=15, blank=True)
    home_phone  = models.CharField(max_length=15, blank=True)
    work_phone  = models.CharField(max_length=15, blank=True)
    job_title   = models.CharField(max_length=255, blank=True)
    photo       = models.ImageField(default='report/chewbaccaheadshot.jpeg', upload_to='profilePics/')

    def __str__(self):
        return f'{self.first_name} {self.last_name} Profile' 
#
##TO CONTROL SIZE OF IMAGE FILE
#    def save(self):
#        super().save()
#
#        img = Image.open(self.photo.path)
#
#        if img.height > 300 or img.width > 300:
#            output_size = (300, 300)
#            img.thumbnail(output_size)
#            img.save()