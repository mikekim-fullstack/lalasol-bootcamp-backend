from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

class UserRole(models.Model):
    ROLE_TYPE=[
        (0, 'STUDENT'),
        (1, 'TEACHER'),
        (2, 'ADMIN'),

    ]
    role_type = models.SmallIntegerField(choices=ROLE_TYPE, default=ROLE_TYPE[0][0])
    def __str__(self):
        return self.ROLE_TYPE[self.role_type][1]
    def get_types(self):
        return self.ROLE_TYPE
    def get_index_by_name(self, name):
        role_num = -1
        for num in self.ROLE_TYPE:
            if name==self.ROLE_TYPE[num][1]:
                role_num = num
        return num
    def get_mytype(self):
        return self.ROLE_TYPE[self.role_type][1]


class UserAccountManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        print('----------- create user account -----------')
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password, **extra_fields):
        # extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_staffuser(self, email, password, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email, password, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class UserAccount(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=56, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = PhoneNumberField(blank=True, null=True)
    role = models.ManyToManyField(UserRole, related_name='role_user')
    is_active = models.BooleanField(default=True)
    
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True, null=True)
    # is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def get_full_name(self):
        return self.first_name+' '+ self.first_name
        # return u'{self.first_name}, {self.first_name}'

    def get_short_name(self):
        return u'{self.first_name}'
    def __str__(self):
        return self.email
    def getRole(self):
        # print(self.role)
        return self.role
    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    @property
    def is_staff(self):
        '''
        Removing is_staff field.
        '''
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    
