from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import AccessibleAuthenticationForm
from .views import (
    BlogDetailView,
    BlogListView,
    CaseStudyDetailView,
    ServiceDetailView,
    about,
    analytics,
    contact,
    home,
    portfolio,
    profile,
    services,
    signup,
    tutorial_advanced_3d,
    tutorial_advanced_network,
    tutorial_beginners_bar,
    tutorial_beginners_line,
    tutorial_intermediate_histogram,
    tutorial_intermediate_scatter,
    tutorials,
    visualizations,
)


urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("services/", services, name="services"),
    path("services/<slug:slug>/", ServiceDetailView.as_view(), name="service_detail"),
    path("portfolio/", portfolio, name="portfolio"),
    path("portfolio/<slug:slug>/", CaseStudyDetailView.as_view(), name="portfolio_detail"),
    path("contact/", contact, name="contact"),
    path("analytics/", analytics, name="analytics"),
    path("blog/", BlogListView.as_view(), name="blog_list"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    path("tutorials/", tutorials, name="tutorials"),
    path("tutorials/beginners/bar/", tutorial_beginners_bar, name="tutorial_beginners_bar"),
    path("tutorials/beginners/line/", tutorial_beginners_line, name="tutorial_beginners_line"),
    path("tutorials/intermediate/histogram/", tutorial_intermediate_histogram, name="tutorial_intermediate_histogram"),
    path("tutorials/intermediate/scatter/", tutorial_intermediate_scatter, name="tutorial_intermediate_scatter"),
    path("tutorials/advanced/network/", tutorial_advanced_network, name="tutorial_advanced_network"),
    path("tutorials/advanced/3d/", tutorial_advanced_3d, name="tutorial_advanced_3d"),
    path("visualizations/", visualizations, name="visualizations"),
    path("signup/", signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="core/login.html",
            authentication_form=AccessibleAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
]





