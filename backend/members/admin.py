from django.contrib import admin
from .models import Committee, Member, MemberRequest, InternalResource, GalleryImage

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'student_id', 'role', 'committee', 'is_active')
    list_filter = ('role', 'committee', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'student_id')
    readonly_fields = ('joined_at',)
    list_editable = ('role', 'is_active')
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'student_id')
        }),
        ('عضویت', {
            'fields': ('role', 'committee', 'is_active')
        }),
        ('زمان', {
            'fields': ('joined_at',),
            'classes': ('collapse',),
        }),
    )

@admin.register(MemberRequest)
class MemberRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'committee', 'status', 'created_at')
    list_filter = ('status', 'committee')
    search_fields = ('user__first_name', 'user__last_name', 'student_id')
    readonly_fields = ('created_at',)
    list_editable = ('status',)

@admin.register(InternalResource)
class InternalResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)
    list_editable = ('category',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)