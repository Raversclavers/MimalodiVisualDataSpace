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


class CaseStudyMetricInline(admin.TabularInline):
    model = CaseStudyMetric
    extra = 1


class CaseStudyScreenshotInline(admin.TabularInline):
    model = CaseStudyScreenshot
    extra = 1


class ServiceDeliverableInline(admin.TabularInline):
    model = ServiceDeliverable
    extra = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "content")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location")
    search_fields = ("user__username", "user__email", "location")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured_order", "is_published", "featured_on_homepage")
    list_filter = ("is_published", "featured_on_homepage", "category")
    list_editable = ("featured_order", "is_published", "featured_on_homepage")
    search_fields = ("title", "category", "summary", "client_name", "industry")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CaseStudyMetricInline, CaseStudyScreenshotInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "featured_order", "is_published", "featured_on_homepage")
    list_filter = ("is_published", "featured_on_homepage")
    list_editable = ("featured_order", "is_published", "featured_on_homepage")
    search_fields = ("title", "short_description", "overview", "ideal_client")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("case_studies",)
    inlines = [ServiceDeliverableInline]
