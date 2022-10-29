from rest_framework.views import APIView
from django.contrib import auth 
from knox.models import AuthToken 
from rest_framework import generics, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404 
from django.contrib.auth import authenticate 
from .models import Post 
from .serializers import (PostSerializer,CreateUserSerializer,LoginSerializer,
                        UsersSerializer,CreateUpdateSerializer)


# OWNER OR READ ONLY PERMISSION 
class OwnerOrReadOnly(permissions.BasePermission):
    def got_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return obj.author == request.user 

# VIEW TO LIST ALL POST 
class PostApiList(APIView): 
    def get(self, request):
        post = Post.objects.filter(hidden=False)
        data = PostSerializer(post, many=True).data 
        return Response(data)

# SHOW POST BY ID PROVIDED
class PostApiDetails(APIView):
    permission_classes =[
        permissions.IsAuthenticated
    ]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        data = PostSerializer(post).data 
        return Response(data)

# CREATE NEW POST 
class PostApiCreate(APIView):
    permission_classes =[
        permissions.IsAuthenticated,
    ]
    @api_view(["POST"])
    def create(request):
        serializer = CreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            title = get_
            serializer.save()
        return Response(serializer.data)

# UPDATE POST ONLY BY OWNER 
class PostApiUpdate(APIView):
    permission_classes =[
        permissions.IsAuthenticated,
        OwnerOrReadOnly
    ]
    @api_view(["POST"])
    def update(request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CreateUpdateSerializer(instance=post, data=request.data)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

# DELETE NEW ONLY BY OWNER 
class PostApiDelete(APIView):
    permission_classes =[
        permissions.IsAuthenticated,
        OwnerOrReadOnly
    ]
    @api_view(["POST"])
    def delete(request, pk):
        post = get_object_or_404(pk=pk)
        post.delete()
        return Response("Post Deleted")


# REGISTER USER VIEW 
class CreateApiUser(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

# PERFORM PROVIDED VALIDATION AND ADD TOKEN TO REGISTERED USERS 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        
        # RETURN USER'S' USERNAME , EMAIL AND TOKEN ON REGISTRATION
        return Response({
            "users":CreateUserSerializer(user, context=self.get_serializer_context()).data,
            "token":token[1]})


# LOGIN VIEW 
class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data 
        return Response({
            "user":UsersSerializer(user, context=self.get_serializer_context()).data,
            "token":Authtoken.objects.create(user)[1]
        })
    
# RETURN THE LOGGED IN USER 
class ActiveApiUser(generics.RetrieveAPIView):
   
#    USER MUST BE LOGGED IN TO GET DATA 
    permission_classes =[
        permissions.IsAuthenticated
    ]

    serializer_class = UsersSerializer

    def get_object(self):
        return self.request.user 
