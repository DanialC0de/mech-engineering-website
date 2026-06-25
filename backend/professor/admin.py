from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ProfessorProfile,
    EventInvitation,
    ProfessorArticle,
    EventProposal
)

from events.models import Event


@admin.register(ProfessorProfile)
class ProfessorProfileAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'employee_id',
        'academic_rank',
        'department',
        'created_at'
    ]

    list_filter = [
        'academic_rank',
        'department',
        'created_at'
    ]

    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'employee_id',
        'field_of_study'
    ]

    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    ordering = ['-created_at']

    fieldsets = (
        (
            'اطلاعات کاربر',
            {
                'fields': ('user',)
            }
        ),
        (
            'اطلاعات شغلی',
            {
                'fields': (
                    'employee_id',
                    'department',
                    'academic_rank',
                    'field_of_study',
                    'office_number'
                )
            }
        ),
        (
            'اطلاعات پژوهشی',
            {
                'fields': (
                    'research_interests',
                    'publications',
                    'bio'
                )
            }
        ),
        (
            'عکس پروفایل',
            {
                'fields': ('avatar',)
            }
        ),
        (
            'تنظیمات',
            {
                'fields': ('receive_notifications',)
            }
        ),
        (
            'تاریخ‌ها',
            {
                'fields': (
                    'created_at',
                    'updated_at'
                ),
                'classes': ('collapse',)
            }
        ),
    )


@admin.register(EventInvitation)
class EventInvitationAdmin(admin.ModelAdmin):

    list_display = [
        'professor',
        'event',
        'role',
        'status',
        'created_at'
    ]

    list_filter = [
        'status',
        'role',
        'event',
        'created_at'
    ]

    search_fields = [
        'professor__username',
        'professor__first_name',
        'professor__last_name',
        'event__title'
    ]

    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    ordering = ['-created_at']

    list_editable = ['status']

    autocomplete_fields = [
        'professor',
        'event'
    ]

    fieldsets = (
        (
            'اطلاعات اصلی',
            {
                'fields': (
                    'event',
                    'professor',
                    'role',
                    'status'
                )
            }
        ),
        (
            'پیام',
            {
                'fields': ('message',)
            }
        ),
        (
            'تاریخ‌ها',
            {
                'fields': (
                    'created_at',
                    'updated_at'
                ),
                'classes': ('collapse',)
            }
        ),
    )

    actions = [
        'accept_invitations',
        'decline_invitations'
    ]

    def accept_invitations(self, request, queryset):

        count = queryset.update(
            status='accepted'
        )

        self.message_user(
            request,
            f"{count} دعوتنامه پذیرفته شد."
        )

    accept_invitations.short_description = (
        "پذیرفتن دعوتنامه‌های انتخاب شده"
    )

    def decline_invitations(self, request, queryset):

        count = queryset.update(
            status='declined'
        )

        self.message_user(
            request,
            f"{count} دعوتنامه رد شد."
        )

    decline_invitations.short_description = (
        "رد کردن دعوتنامه‌های انتخاب شده"
    )


@admin.register(ProfessorArticle)
class ProfessorArticleAdmin(admin.ModelAdmin):

    list_display = [
        'title',
        'professor',
        'status',
        'created_at'
    ]

    list_filter = [
        'status',
        'created_at'
    ]

    search_fields = [
        'title',
        'professor__username',
        'professor__first_name',
        'professor__last_name',
        'abstract'
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
        'article_file_link'
    ]

    ordering = ['-created_at']

    fieldsets = (
        (
            'اطلاعات مقاله',
            {
                'fields': (
                    'title',
                    'abstract',
                    'file',
                    'article_file_link',
                    'status',
                    'admin_feedback'
                )
            }
        ),
        (
            'استاد',
            {
                'fields': ('professor',)
            }
        ),
        (
            'تاریخ‌ها',
            {
                'fields': (
                    'created_at',
                    'updated_at'
                ),
                'classes': ('collapse',)
            }
        ),
    )

    actions = [
        'approve_articles',
        'reject_articles'
    ]

    def article_file_link(self, obj):

        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">دانلود فایل مقاله</a>',
                obj.file.url
            )

        return "-"

    article_file_link.short_description = "فایل مقاله"

    def approve_articles(self, request, queryset):

        count = queryset.update(
            status='approved'
        )

        self.message_user(
            request,
            f"{count} مقاله تایید شد."
        )

    approve_articles.short_description = (
        "تایید مقالات انتخاب شده"
    )

    def reject_articles(self, request, queryset):

        count = queryset.update(
            status='rejected'
        )

        self.message_user(
            request,
            f"{count} مقاله رد شد."
        )

    reject_articles.short_description = (
        "رد مقالات انتخاب شده"
    )


@admin.register(EventProposal)
class EventProposalAdmin(admin.ModelAdmin):

    list_display = [
        'title',
        'professor',
        'event_type',
        'proposed_date',
        'status',
        'created_at'
    ]

    list_filter = [
        'status',
        'event_type',
        'created_at'
    ]

    search_fields = [
        'title',
        'professor__username',
        'professor__first_name',
        'professor__last_name',
        'description'
    ]

    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    ordering = ['-created_at']

    fieldsets = (
        (
            'اطلاعات پیشنهاد',
            {
                'fields': (
                    'title',
                    'description',
                    'proposed_date',
                    'event_type',
                    'status',
                    'admin_feedback'
                )
            }
        ),
        (
            'استاد',
            {
                'fields': ('professor',)
            }
        ),
        (
            'تاریخ‌ها',
            {
                'fields': (
                    'created_at',
                    'updated_at'
                ),
                'classes': ('collapse',)
            }
        ),
    )

    actions = [
        'approve_proposals',
        'reject_proposals'
    ]

    def approve_proposals(self, request, queryset):

        approved_count = 0

        for proposal in queryset:

            if proposal.status == 'approved':
                continue

            Event.objects.create(
                title=proposal.title,
                short_description=proposal.description,
                full_description=proposal.description,
                syllabus='',
                instructor_name=proposal.professor.get_full_name(),
                instructor_title='استاد',
                jalali_date=proposal.proposed_date,
                time='تعیین نشده',
                status='upcoming',
                capacity=0,
                created_by=proposal.professor
            )

            proposal.status = 'approved'
            proposal.save()

            approved_count += 1

        self.message_user(
            request,
            f"{approved_count} پیشنهاد تایید و به رویداد تبدیل شد."
        )

    approve_proposals.short_description = (
        "تایید و ایجاد رویداد"
    )

    def reject_proposals(self, request, queryset):

        count = queryset.update(
            status='rejected'
        )

        self.message_user(
            request,
            f"{count} پیشنهاد رویداد رد شد."
        )

    reject_proposals.short_description = (
        "رد پیشنهادات انتخاب شده"
    )