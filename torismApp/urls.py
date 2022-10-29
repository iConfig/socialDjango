from django.urls import path ,include
from .apiviews import (PostApiList, PostApiDetails, CreateApiUser,LoginApi,
                    ActiveApiUser, PostApiCreate,PostApiUpdate,
                    PostApiDelete)
from .views import (HomeView,signupView,loginView,logoutView,PostDetails,LikePostView,
                    PostUpdate,PostDelete,PostCreate,ProfileView,profileupdateView,
                    CommentView)
from knox import views as knox_views 
from django.conf import settings 
from django.conf.urls.static import static 



urlpatterns = [
    path('', HomeView, name="home"),
    path('profile', ProfileView, name="profile"),
    path('profile/edit', profileupdateView, name="edit_profile"),
    path('posts/details/<int:pk>', PostDetails, name="post_details"),
    path('posts/new', PostCreate, name="post_create"),
    path('posts/update/<int:id>', PostUpdate, name="post_update"),
    path('posts/delete<int:id>', PostDelete, name="post_delete"),
    path('posts/like', LikePostView, name="post_likes"),
    path('posts/details/comment', CommentView, name="post_comment"),
    path('join/register', signupView, name="register"),
    path('join/login', loginView, name="login"),
    path('join/logout', logoutView, name="logout"),
    path("posts/api", PostApiList.as_view(), name="posts_list"),
    path("posts/api/<int:post_id>", PostApiDetails.as_view(), name="posts_api_details"),
    path("posts/api/create/", PostApiCreate.as_view(), name="create_api_posts"),
    path("posts/api/update/", PostApiUpdate.as_view(), name="update_api_posts"),
    path("posts/api/delete/", PostApiDelete.as_view(), name="delete_api_posts"),
    path('auth/api/', include('knox.urls')),
    path('auth/api/user/', ActiveApiUser.as_view(), name="users"),
    path("auth/api/signup/", CreateApiUser.as_view(), name="create_user"),
    path("auth/api/login/", LoginApi.as_view(), name="login_user"),
    path("auth/api/logout/", knox_views.LogoutView.as_view(), name="logout_user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)