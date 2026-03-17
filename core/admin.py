from django.contrib import admin
from .models import (
    BlogPost,
    CaseStudy,
    CaseStudyMetric,
    CaseStudyScreenshot,
    ContactSubmission,
    Profile,
    Service,
    ServiceDeliverable,
    Tutorial,
)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location")
    search_fields = ("user__username", "user__email", "location")


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")


class CaseStudyMetricInline(admin.TabularInline):
    model = CaseStudyMetric
    extra = 1


class CaseStudyScreenshotInline(admin.TabularInline):
    model = CaseStudyScreenshot
    extra = 1


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "client_name", "featured_on_homepage", "is_published")
    list_filter = ("featured_on_homepage", "is_published", "category")
    search_fields = ("title", "client_name", "industry", "summary", "result")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CaseStudyMetricInline, CaseStudyScreenshotInline]


class ServiceDeliverableInline(admin.TabularInline):
    model = ServiceDeliverable
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "featured_on_homepage", "is_published")
    list_filter = ("featured_on_homepage", "is_published")
    search_fields = ("title", "short_description", "overview", "ideal_client", "business_value")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("case_studies",)
    inlines = [ServiceDeliverableInline]
