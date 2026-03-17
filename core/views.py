from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.conf import settings
from django.views.generic import DetailView, ListView

from .forms import AccessibleUserCreationForm, ContactForm, ProfileUpdateForm, UserUpdateForm
from .models import BlogPost, CaseStudy, ContactSubmission, Profile, Service, Tutorial


def home(request):
    context = {
        "posts": BlogPost.objects.all()[:3],
        "tutorials": Tutorial.objects.all()[:3],
        "featured_case_studies": CaseStudy.objects.filter(is_published=True, featured_on_homepage=True)[:3],
        "featured_services": _published_services().filter(featured_on_homepage=True)[:3],
    }
    return render(request, "core/home.html", context)


def about(request):
    return render(request, "core/about.html", {"featured_services": _published_services().filter(featured_on_homepage=True)[:3]})


def services(request):
    services_catalog = _published_services()
    context = {
        "services": services_catalog,
        "service_metrics": [
            {"label": "Core service areas", "value": services_catalog.count()},
            {"label": "Published case studies", "value": CaseStudy.objects.filter(is_published=True).count()},
            {"label": "Main outcome", "value": "Clearer decisions from better data"},
        ],
    }
    return render(request, "core/services.html", context)


class ServiceDetailView(DetailView):
    model = Service
    template_name = "core/service_detail.html"
    context_object_name = "service"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Service.objects.filter(is_published=True).prefetch_related(
            "deliverables",
            "case_studies__metrics",
            "case_studies__screenshots",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        linked_case_studies = self.object.case_studies.filter(is_published=True).prefetch_related("metrics", "screenshots")
        if not linked_case_studies.exists():
            linked_case_studies = CaseStudy.objects.filter(is_published=True, featured_on_homepage=True)[:2]

        context["service_case_studies"] = linked_case_studies
        context["related_services"] = Service.objects.filter(is_published=True).exclude(pk=self.object.pk)[:2]
        context["service_proof_points"] = [
            {"label": "Deliverables", "value": self.object.deliverables.count()},
            {"label": "Linked case studies", "value": linked_case_studies.count() if hasattr(linked_case_studies, "count") else len(linked_case_studies)},
            {"label": "Best fit", "value": "Teams that need clearer reporting"},
        ]
        return context


def contact(request):
    selected_service = None
    initial = {}
    service_slug = request.GET.get("service", "").strip()
    requested_subject = request.GET.get("subject", "").strip()

    if service_slug:
        selected_service = Service.objects.filter(is_published=True, slug=service_slug).first()
        if selected_service and request.method != "POST":
            initial["subject"] = selected_service.contact_subject

    if requested_subject and request.method != "POST":
        initial["subject"] = requested_subject

    form = ContactForm(request.POST or None, initial=initial)

    if request.method == "POST":
        if form.is_valid():
            submission = form.save()
            _send_contact_notification(submission)
            messages.success(
                request,
                "Thanks for reaching out. Your inquiry has been received and I typically respond within 1 to 2 business days.",
            )
            return redirect("contact")

        messages.error(request, "Please review the form and correct the highlighted fields.")

    return render(request, "core/contact.html", {"form": form, "selected_service": selected_service})


def signup(request):
    if request.method == "POST":
        form = AccessibleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("profile")
    else:
        form = AccessibleUserCreationForm()
    return render(request, "core/signup.html", {"form": form})


@login_required
def profile(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    context = {
        "profile_record": user_profile,
        "profile_completion": _profile_completion_score(request.user, user_profile),
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "core/profile.html", context)


class BlogListView(ListView):
    model = BlogPost
    template_name = "core/blog_list.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_services"] = _published_services()[:2]
        context["featured_case_studies"] = CaseStudy.objects.filter(is_published=True, featured_on_homepage=True)[:2]
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "core/blog_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_posts"] = BlogPost.objects.exclude(pk=self.object.pk)[:2]
        context["featured_services"] = _published_services()[:2]
        return context


def analytics(request):
    context = {
        "metrics": [
            {"label": "Published articles", "value": BlogPost.objects.count()},
            {"label": "Tutorials available", "value": Tutorial.objects.count()},
            {"label": "Service landing pages", "value": Service.objects.filter(is_published=True).count()},
            {"label": "Case studies", "value": CaseStudy.objects.filter(is_published=True).count()},
        ],
        "analytics_highlights": [
            {
                "title": "Reporting systems over vanity dashboards",
                "description": "The site now frames analytics as a repeatable business workflow: cleaner data, clearer reporting, and stronger stakeholder communication.",
            },
            {
                "title": "Portfolio-backed services",
                "description": "Service pages can now point to linked case studies, which creates a more convincing path from offer to proof.",
            },
            {
                "title": "Simple, production-minded delivery",
                "description": "The stack remains plain Django so the experience stays reliable on inexpensive hosting without relying on fragile prototype infrastructure.",
            },
        ],
        "featured_services": _published_services()[:3],
        "featured_case_studies": CaseStudy.objects.filter(is_published=True, featured_on_homepage=True)[:2],
    }
    return render(request, "core/analytics.html", context)


def portfolio(request):
    case_studies = CaseStudy.objects.filter(is_published=True).prefetch_related("metrics", "screenshots")
    context = {
        "case_studies": case_studies,
        "portfolio_metrics": [
            {"label": "Case studies", "value": len(case_studies)},
            {"label": "Core offer", "value": "Dashboards and reporting"},
            {"label": "Audience", "value": "Clients and employers"},
        ],
    }
    return render(request, "core/portfolio.html", context)


class CaseStudyDetailView(DetailView):
    model = CaseStudy
    template_name = "core/portfolio_detail.html"
    context_object_name = "case_study"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return CaseStudy.objects.filter(is_published=True).prefetch_related("metrics", "screenshots")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_case_studies"] = (
            CaseStudy.objects.filter(is_published=True)
            .exclude(pk=self.object.pk)
            .order_by("featured_order", "title")[:2]
        )
        return context


def visualizations(request):
    visualization_case_studies = CaseStudy.objects.filter(is_published=True).prefetch_related("metrics")[:3]
    context = {
        "dataset_title": "World Happiness Report",
        "dataset_overview": "A sample portfolio dataset showing how business questions can be turned into clear visual narratives.",
        "static_visual": "core/images/example_static_chart.png",
        "insights": "Reusable visuals, concise annotations, and a clear narrative are more production-friendly than a prototype dashboard stack.",
        "visualization_case_studies": visualization_case_studies,
    }
    return render(request, "core/visualizations.html", context)


def tutorials(request):
    return render(
        request,
        "core/tutorials.html",
        {
            "tutorials": Tutorial.objects.all(),
            "featured_services": _published_services()[:2],
        },
    )


def tutorial_beginners_bar(request):
    return render(request, "core/tutorials/beginners_bar.html")


def tutorial_beginners_line(request):
    return render(request, "core/tutorials/beginners_line.html")


def tutorial_intermediate_histogram(request):
    return render(request, "core/tutorials/intermediate_histogram.html")


def tutorial_intermediate_scatter(request):
    return render(request, "core/tutorials/intermediate_scatter.html")


def tutorial_advanced_network(request):
    return render(request, "core/tutorials/advanced_network.html")


def tutorial_advanced_3d(request):
    return render(request, "core/tutorials/advanced_3d.html")


def _published_services():
    return Service.objects.filter(is_published=True).prefetch_related("deliverables", "case_studies__metrics")


def _profile_completion_score(user, profile):
    fields = [
        user.first_name,
        user.last_name,
        user.email,
        profile.bio,
        profile.location,
    ]
    completed_fields = sum(bool(field) for field in fields)
    return int((completed_fields / len(fields)) * 100)


def _send_contact_notification(submission: ContactSubmission) -> None:
    recipient = getattr(settings, "CONTACT_NOTIFICATION_EMAIL", "") or getattr(settings, "DEFAULT_FROM_EMAIL", "")
    default_from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "")

    if not recipient or not default_from_email:
        return

    send_mail(
        subject=f"New contact inquiry: {submission.subject}",
        message=(
            f"Name: {submission.name}\n"
            f"Email: {submission.email}\n\n"
            f"Message:\n{submission.message}"
        ),
        from_email=default_from_email,
        recipient_list=[recipient],
        fail_silently=True,
    )