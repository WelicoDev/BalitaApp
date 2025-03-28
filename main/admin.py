from django.contrib import admin
from .models import Category, Tags, Post, About, Contact, Comment
from django.utils.html import mark_safe

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_display_links = ('id', 'name')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
    search_fields = ('tag',)
    list_display_links = ('id', 'tag')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_published', 'view_count', 'created_at', 'image_preview')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content', 'description', 'category__name', 'tags__tag')
    list_filter = ('is_published', 'category', 'tags')
    list_display_links = ('id', 'title', 'view_count')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'user', 'category', 'tags', 'description', 'is_published')
        }),
        ('Image Information', {
            'fields': ('picture',)
        }),
        ('SEO', {
            'fields': ('view_count',)
        }),
    )
    def image_preview(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture.url}" width="120" height="90"/>')
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', "full_name", "image_preview")
    def image_preview(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture.url}" width="120" height="90"/>')
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message')  # Qaysi maydonlar ro'yxatda ko'rsatiladi
    search_fields = ('name', 'email')  # Qidiruv maydonlari
    list_filter = ('name', 'email')  # Filtrlar

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','is_public', 'created_at']
    list_display_links = ('id', 'user')