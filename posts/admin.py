from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, PostFiles, Friendship, UserProfile

class PostFilesInline(admin.TabularInline):
    """Inline for managing uploaded files related to a post."""
    model = PostFiles
    extra = 1
    fields = ('file', 'description', 'file_preview')
    readonly_fields = ('file_preview',)

    def file_preview(self, obj):
        """Show a preview if the uploaded file is image, video, or audio."""
        if not obj.file:
            return "No file"
        url = obj.file.url.lower()
        if url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            return mark_safe(f'<img src="{obj.file.url}" style="max-height:100px; border-radius:6px;" />')
        elif url.endswith(('.mp4', '.mov', '.webm', '.ogg', '.avi')):
            return mark_safe(f'<video src="{obj.file.url}" style="max-height:100px; border-radius:6px;" controls></video>')
        elif url.endswith(('.mp3', '.wav', '.ogg')):
            return mark_safe(f'<audio src="{obj.file.url}" controls></audio>')
        return "No preview available"
    file_preview.short_description = "Preview"


class CommentInline(admin.TabularInline):
    """Inline for viewing and editing comments on a post."""
    model = Comment
    extra = 0
    readonly_fields = ('author', 'comment', 'created_at', 'updated_at')
    fields = ('author', 'comment', 'likes', 'dislikes', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Main admin for posts."""
    list_display = ('title', 'author', 'slug', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'tags')
    search_fields = ('title', 'description', 'tags', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('likes', 'dislikes')

    inlines = [PostFilesInline, CommentInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'description', 'tags')
        }),
        ('Post Attributes', {
            'classes': ('collapse',),
            'fields': ('post_attributes',),
        }),
        ('Engagement', {
            'classes': ('collapse',),
            'fields': ('likes', 'dislikes'),
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Standalone admin for managing comments."""
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('comment', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('likes', 'dislikes')


@admin.register(PostFiles)
class PostFilesAdmin(admin.ModelAdmin):
    """Standalone admin for managing uploaded post files."""
    list_display = ('post', 'file', 'description')
    search_fields = ('post__title', 'description')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for managing user profiles."""
    list_display = ('user', 'bio',)
    search_fields = ('user__username', 'bio', 'location')
    readonly_fields = ('user',)

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    """Admin for managing user follow relationships."""
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """Optimize by prefetching related users."""
        qs = super().get_queryset(request)
        return qs.select_related('follower', 'following')
