from django.contrib import admin

from .models import Gif, User, Comment

class GifAdmin(admin.ModelAdmin):
	list_display = ('gif_name', 'gif_url')

admin.site.register(Gif, GifAdmin)

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'password')

admin.site.register(User, UserAdmin)

class CommentAdmin(admin.ModelAdmin):
	#list_display = ('content')
	pass
admin.site.register(Comment, CommentAdmin)
