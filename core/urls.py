from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import include
from .views import BlogDetailView, BlogListView  # Ensure BlogListView is imported

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('analytics/', views.analytics, name='analytics'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', BlogListView.as_view(), name='blog_list'),  # Blog listing page
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),  # Blog detail page
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('visualizations/', views.visualizations, name='visualizations'),
    path('django_plotly_dash/', include('django_plotly_dash.urls', namespace='the_django_plotly_dash')),
    path('tutorials/', views.tutorials, name='tutorials'),
    path('tutorials/beginners/bar/', views.tutorial_beginners_bar, name='tutorial_beginners_bar'),
    path('tutorials/beginners/line/', views.tutorial_beginners_line, name='tutorial_beginners_line'),
    path('tutorials/intermediate/histogram/', views.tutorial_intermediate_histogram, name='tutorial_intermediate_histogram'),
    path('tutorials/intermediate/scatter/', views.tutorial_intermediate_scatter, name='tutorial_intermediate_scatter'),
    path('tutorials/advanced/network/', views.tutorial_advanced_network, name='tutorial_advanced_network'),
    path('tutorials/advanced/3d/', views.tutorial_advanced_3d, name='tutorial_advanced_3d'),
    path('tutorials/', views.tutorials_home, name='tutorials_home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





