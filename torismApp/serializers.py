from rest_framework import serializers 
from rest_framework.authtoken.models import Token 
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
from .models import Post 

# ALL Post SERIALIZER 
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# CREATE AND UPDATE Post SERIALIZER 
class CreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

        def CreateUpadate(self, validated_data):
            title = self.validated_data['title']
            content = self.validated_data['content']
            created_by = self.request.user
            
            data = Post.objects.create_user(title,content,created_by)
            data.save()
            
            return data

# SERIALIZER FOR ACTIVE USER 
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('id','username','email')

# USER REGISTRATION SERIALIZER 
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('username', 'email', 'password')
        extra_kwargs = {'username':{'min_length':4, 'max_length':25},
                        'email':{'max_length':20,
                        "validators":[
                            UniqueValidator(
                                queryset=User.objects.all(),
                                message="Email already exists!"
                            )
                        ]},
                        'password': {'write_only':True}
                        }
        # GETTING AND RETURNING VALIDATED DATA 
        def create_user(self, validated_data):
            username = validated_data['username']
            email = validated_data['email']
            password = validated_data['password']
            
            user = User.objects.create_user(username,email,password)
            user.save()
            
            return user

# LOGIN SERIALIZER
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(label="Password",
                style={'input_type':'password'}, write_only=True,trim_whitespace=True)


    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user 
        raise serializers.ValidationError("incorrect username or password")