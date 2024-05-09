from django.contrib import admin
from .models import Post, Category, Comment, Rating

from mptt.admin import DraggableMPTTAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ панель для категорий
    """

    prepopulated_fields = {'slug' : ('title', )}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}


@admin.register(Comment)
class CommentAdminPage(DjangoMpttAdmin):
    """
    Админ-модель комментариев
    """
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass