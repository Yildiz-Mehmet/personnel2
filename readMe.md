# first installation stage

- python -m venv env
- source env/bin/activate
- pip install djangorestframework
- pip freeze > requirements.txt

# project need to be build for be setting

# we builded a project called main

- django-admin startproject main .

- settings => Installed_apps => + 'rest_framework'

# to make it work server

- python manage.py runserver

# migrate send django default tables to db.sqlite3 database

- python manage.py migrate

- python manage.py createsuperuser

# before you send githup build .gitignore

# install python-decouple and build .env

- pip install django-decouple

- settings => SECRET_KEY = config("SECRET_KEY")

- from decouple import config

# create the app

- python manage.py startapp personnel

- add installed_apps => + 'personnel',

# create model

- models.py =>

```py
from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name=models.CharField(max_length=32)
    user_id=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created=models.DateTimeField(auto_now_add= True)
    updated=models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name

class Personnel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    GENDER = (
        ('F','Female'),
        ('M','Male'),
        ('N','Prefer not to say'),
    )
    gender = models.CharField(max_length=1,choices=GENDER)
    TITLE =(
        ('S','Senior'),
        ('M','Med-Senior'),
        ('J','Junior'),
    )
    title = models.CharField(max_length=1,choices=TITLE)
    salary = models.IntegerField()
    started = models.DateField()
    department_id = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name='personnel')
    user_id = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created=models.DateTimeField(auto_now_add= True)
    updated=models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.first_name +'-'+self.last_name

```

# after create models

- python manage.py makemigrations

- python manage.py migrate

# for see in admin

```py
from .models import Department, Personnel

admin.site.register(Department)
admin.site.register(Personnel)


```

# create serializers.py =>

```py
from rest_framework import serializers
from .models import Department,Personnel

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'

class PersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personnel
        fields = '__all__'


```

# now there is a views.py => we have to make a decision that what will be in view

```py

from django.shortcuts import render
from .serializers import DepartmentSerializer,PersonnelSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Department,Personnel

class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer



class PersonnelListCreateView(ListCreateAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer


class PersonnelRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer



class DepartmentRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


```

# now there is urls.py => create personnel.urls

```py

from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('personnel.urls')),
]



```

# personnel urls.py =>

```py

from django.urls import path
from .views import DepartmentListCreateView,DepartmentRUDView,PersonnelListCreateView,PersonnelRUDView,DepartmentPersonnelView

urlpatterns = [
    path('departments/',DepartmentListCreateView.as_view()),
    path('departments/<int:pk>/',DepartmentRUDView.as_view()),
    path('personnels/',PersonnelListCreateView.as_view()),
    path('personnels/<int:pk>/',PersonnelRUDView.as_view()),
    # path('department-personnels/',DepartmentPersonnelView.as_view()),
    path('department<str:department>/',DepartmentPersonnelView.as_view()),
]

```

# nested serializers => personnel will lined up under department

# serializers.py =>

```py
class DepartmentPersonnelSerializer(serializers.ModelSerializer):

    personnel = PersonnelSerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = '__all__'

```

# views.py =>

```py
class DepartmentPersonnelView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentPersonnelSerializer


    def get_queryset(self):

        department = self.kwargs['department']
        return Department.objects.filter(name__iexact=department)
```

# models use related name => python manage.py makemigrations => python manage.py migrate

```py

department_id = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name='personnel')

```

##############################

# we will write custom permission

# build permissions.py

```py
from rest_framework.permissions import IsAdminUser,SAFE_METHODS

class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):


        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
```

# add this you want all views

```py
    permission_classes = (
        IsAuthenticated,
        IsAdminOrReadOnly,
    )
```

# others

```py
permission_classes =[IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:

            return self.update(request, *args, **kwargs)
        data = {
            'message':'You are not authorized to update!'
        }
        return Response(data,status=status.HTTP_401_UNAUTHORİZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance)
        if self.request.user.is_superuser:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'message':'You are not authorized to delete!'
        }
        return Response(data,status=status.HTTP_401_UNAUTHORİZED)


```

# build users for authentication with token

- python manage.py startapp users
- add to ınstalled_apps

```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

# dj-rest-auth add ınstalled_apps

```py
INSTALLED_APPS = (
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    ...,
    'dj_rest_auth'
)
```

- pip install dj-rest-auth
- python manage.py migrate

# urlpattern add

# main urls.py

```py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('personnel.urls')),
    path('users/',include('users.urls')),
]

```

# users urls.py

```py
from django.urls import path,include
urlpatterns = [

    path('auth/', include('dj_rest_auth.urls'))
]

```

## users => models.py =>

```py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    image = models.ImageField(upload_to="images",default="avatar")
    about = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


```

## Since we builted somethings in database,run makemigrations

- python manage.py makemigrations
- pip freeze > requirements.txt
- python manage.py migrate

# users => admin.py =>

```py
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)

```

## main => urls.py =>

```py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

# settings.py =>

```py
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

```

## create users => serializers.py =>

```py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required = True,
        validators = [
            UniqueValidator(queryset=User.objects.all())
        ],
    )

    password = serializers.CharField(
        write_only = True,  # GET methods can not return the password
        required = True,
        validators = [
            validate_password
        ],
        style = {
            'input_type':'password',
        }
    )

    password2 = serializers.CharField(
        write_only = True,
        required = True,
        style = {
            'input_type':'password',
        }
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'password2',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            data = {
                "password": "Password fields does not match!!!"
            }
            raise serializers.ValidationError(data)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )


class CustomTokenSerializer(TokenSerializer):

    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = (
            'key',
            'user',
            )

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Profile
        fields = (
            'id',
            'image',
            'about',
            'user'
        )
```

# users => views.py =>

```py
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from serializers import RegisterSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


```

# urls.py =>

```py

from django.urls import path,include
from .views import RegisterView

urlpatterns = [

    path('auth/', include('dj_rest_auth.urls')),
    path('register/', RegisterView.as_view()),

]
```

# create users => signals.py

```py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Profile


@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)

```

## apps.py =>

```py
 def ready(self):
        import users.signals

```

## views.py =>

```py
from django.shortcuts import render
from rest_framework.generics import ( CreateAPIView,
                                     RetrieveUpdateAPIView)
from django.contrib.auth.models import User
from .serializers import (RegisterSerializer,
                          ProfileSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Profile
from rest_framework.decorators import api_view

from rest_framework.permissions import IsAuthenticated



class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['token'] = 'No token created for this user!!!'

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)



class ProfileUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrStaff)


@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    data = {
        'message':'Logged out succesfully!'
    }
    return Response(data, status=status.HTTP_200_OK)



```

## urls.py =>

```py
 path('profile/<int:pk>', ProfileUpdateView.as_view()),

```

## for logout

```py
  path('auth/logout/', logout)

```
