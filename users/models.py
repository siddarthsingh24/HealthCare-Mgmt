from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can access admin site.')
    profile_picture = models.ImageField(upload_to='profile_pictures', max_length=255)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

CATEGORY_CHOICES = [
    ('Mental Health', 'Mental Health'),
    ('Heart Disease', 'Heart Disease'),
    ('Covid19', 'Covid19'),
    ('Immunization', 'Immunization'),
]

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary = models.TextField(max_length=500)
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
