from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg", blank=True, null=True)

    def __str__(self):
        return self.user.username


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def excerpt(self):
        words = self.content.split()
        preview = " ".join(words[:30])
        if len(words) > 30:
            return f"{preview}..."
        return preview


class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=120)
    accent = models.CharField(max_length=120, blank=True)
    client_name = models.CharField(max_length=160, blank=True)
    industry = models.CharField(max_length=120, blank=True)
    summary = models.TextField()
    client_context = models.TextField()
    challenge = models.TextField()
    approach = models.TextField()
    solution = models.TextField()
    tools_used = models.TextField(help_text="Comma-separated tools or capabilities used on the project.")
    result = models.TextField()
    featured_on_homepage = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    featured_order = models.PositiveSmallIntegerField(default=0)
    hero_image = models.ImageField(upload_to="case-studies/", blank=True, null=True)
    hero_image_path = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["featured_order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("portfolio_detail", kwargs={"slug": self.slug})

    @property
    def tools_list(self):
        return [tool.strip() for tool in self.tools_used.split(",") if tool.strip()]


class CaseStudyMetric(models.Model):
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name="metrics")
    label = models.CharField(max_length=120)
    value = models.CharField(max_length=120)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.case_study.title}: {self.label}"


class CaseStudyScreenshot(models.Model):
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name="screenshots")
    title = models.CharField(max_length=160)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to="case-studies/", blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.case_study.title}: {self.title}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=80, default="fas fa-chart-line")
    short_description = models.TextField(help_text="Short summary used on cards, previews, and SEO-heavy sections.")
    hero_headline = models.CharField(max_length=220, blank=True)
    overview = models.TextField()
    ideal_client = models.TextField()
    business_value = models.TextField()
    process_summary = models.TextField()
    inquiry_subject = models.CharField(max_length=160, blank=True)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    featured_on_homepage = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    featured_order = models.PositiveSmallIntegerField(default=0)
    hero_image = models.ImageField(upload_to="services/", blank=True, null=True)
    hero_image_path = models.CharField(max_length=255, blank=True)
    case_studies = models.ManyToManyField(CaseStudy, related_name="related_services", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["featured_order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"slug": self.slug})

    @property
    def contact_subject(self):
        return self.inquiry_subject or f"Inquiry about {self.title}"

    @property
    def display_headline(self):
        return self.hero_headline or self.title

    @property
    def meta_title(self):
        return self.seo_title or f"{self.title} Services | Mimalodi Visual Data Space"

    @property
    def meta_description(self):
        return self.seo_description or self.short_description


class ServiceDeliverable(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="deliverables")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.service.title}: {self.title}"


