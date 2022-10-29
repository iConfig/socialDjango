from django.contrib import admin
from.models import Post,Profile,Like,Comment

# Register your models here.

class postAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'title', 'created_date']
    list_filter = ['created_by', 'created_date']
    search_fields = ['created_by', 'title','created_date']


admin.site.register(Post, postAdmin)

class profileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username','location']
    # list_filter = ['first_name', 'last_name','user','location']
    search_fields = ('first_name','last_name',)

admin.site.register(Profile, profileAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']

admin.site.register(Like, LikeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'post','comment']

admin.site.register(Comment, CommentAdmin)