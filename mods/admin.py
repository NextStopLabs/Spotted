from django.contrib import admin
from .models import Mod, ModVersion, Comment

# --- Inline for ModVersion (shows all versions on Mod page) ---
class ModVersionInline(admin.TabularInline):
    model = ModVersion
    extra = 1  # show 1 empty row by default
    fields = ('version_number', 'zip_file')
    show_change_link = True
    verbose_name = "Version"
    verbose_name_plural = "Versions"

# --- Inline for Comment (shows all comments on Mod page) ---
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'comment', 'created_at', 'updated_at')
    can_delete = True
    verbose_name = "Comment"
    verbose_name_plural = "Comments"

# --- Main Mod Admin ---
@admin.register(Mod)
class ModAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'latest_version', 'version_count', 'comment_count', 'views')
    search_fields = ('name', 'description')
    inlines = [ModVersionInline, CommentInline]

    def latest_version(self, obj):
        latest = obj.modversion_set.order_by('-id').first()
        return latest.version_number if latest else "—"
    latest_version.short_description = "Latest Version"

    def version_count(self, obj):
        return obj.modversion_set.count()
    version_count.short_description = "Total Versions"

    def comment_count(self, obj):
        return obj.comment_set.count()
    comment_count.short_description = "Comments"

# --- ModVersion Admin ---
@admin.register(ModVersion)
class ModVersionAdmin(admin.ModelAdmin):
    list_display = ('mod', 'version_number', 'zip_file', 'downloads')
    search_fields = ('mod__name', 'version_number')
    list_filter = ('mod',)

# --- Comment Admin ---
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('mod', 'author', 'short_comment', 'created_at')
    search_fields = ('mod__name', 'author__username', 'comment')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def short_comment(self, obj):
        return (obj.comment[:75] + '...') if len(obj.comment) > 75 else obj.comment
    short_comment.short_description = "Comment"
