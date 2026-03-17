from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import AccessibleAuthenticationForm
from .views import BlogDetailView, BlogListView, CaseStudyDetailView, ServiceDetailView


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", ServiceDetailView.as_view(), name="service_detail"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="core/login.html", authentication_form=AccessibleAuthenticationForm),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("blog/", BlogListView.as_view(), name="blog_list"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/<slug:slug>/", CaseStudyDetailView.as_view(), name="portfolio_detail"),
    path("analytics/", views.analytics, name="analytics"),
    path("visualizations/", views.visualizations, name="visualizations"),
    path("tutorials/", views.tutorials, name="tutorials"),
    path("tutorials/beginners/bar/", views.tutorial_beginners_bar, name="tutorial_beginners_bar"),
    path("tutorials/beginners/line/", views.tutorial_beginners_line, name="tutorial_beginners_line"),
    path("tutorials/intermediate/histogram/", views.tutorial_intermediate_histogram, name="tutorial_intermediate_histogram"),
    path("tutorials/intermediate/scatter/", views.tutorial_intermediate_scatter, name="tutorial_intermediate_scatter"),
    path("tutorials/advanced/network/", views.tutorial_advanced_network, name="tutorial_advanced_network"),
    path("tutorials/advanced/3d/", views.tutorial_advanced_3d, name="tutorial_advanced_3d"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





