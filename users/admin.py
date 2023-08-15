from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.sessions.models import Session

from .models import Post, Category, Comment

# Register your models here.

admin.site.register(Category)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_date')
    # fieldsets = ((None,{'fields':('title',)}),)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'comment_date')


class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)
