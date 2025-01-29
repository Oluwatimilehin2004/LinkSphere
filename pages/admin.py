from django.contrib import admin
from .models import Posts, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at',)

admin.site.register(Posts, PostAdmin)
admin.site.register(Comment)
