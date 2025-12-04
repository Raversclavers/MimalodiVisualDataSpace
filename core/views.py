from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .models import BlogPost
from .models import BlogPost, Profile, Tutorial  # Add Tutorial to the import statement
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .visualization_utils import generate_static_visualizations
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .forms import ProfileUpdateForm
from .models import Profile



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
       
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'core/profile.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)  # Corrected this line to call the logout function properly
    return redirect('home')

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'core/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = BlogPost.objects.get(slug=slug)
    return render(request, 'core/blog_detail.html', {'post': post})

class BlogListView(ListView):
    model = BlogPost
    template_name = 'core/blog_list.html'  # Ensure this path is correct
    context_object_name = 'posts'

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'core/blog_detail.html'  # Ensure this path is correct
    context_object_name = 'post'

def visualizations(request):
    # Context for dashboard (modify with actual dataset details)
    context = {
        'dataset_title': 'World Happiness Report',
        'dataset_overview': 'This dataset explores the happiness scores of countries from 2015 to 2019.',
        'filters': ['Year', 'Region'],
        'graphs': {
            'interactive_chart': 'example_interactive_dashboard',
            'static_visual': 'example_static_chart',
        },
        'insights': 'Key insights from the dataset include trends in happiness scores over years and regional comparisons.',
    }
    return render(request, 'core/visualizations.html', context)

def home(request):
       posts = BlogPost.objects.all().order_by('-created_at')[:5]  # Get the latest 5 posts
       return render(request, 'core/home.html', {'posts': posts})

@login_required
def analytics(request):
    return render(request, 'core/analytics.html')

def blog_tutorials(request):
    blog_posts = BlogPost.objects.all()  # Fetch all blog posts
    return render(request, 'core/blog_tutorials.html', {'blog_posts': blog_posts})

def blog_and_tutorials(request):
    blog_posts = BlogPost.objects.all()  # Fetch all blog posts
    return render(request, 'core/blog_and_tutorials.html', {'blog_posts': blog_posts})

def tutorials(request):
    tutorials = Tutorial.objects.all()  # Fetch all tutorials
    return render(request, 'core/tutorials.html', {'tutorials': tutorials})

def tutorial_beginners_bar(request):
    # Render a template with the line graph tutorial content
    return render(request, 'core/tutorials/beginners_bar.html')

def tutorial_beginners_line(request):
    return render(request, 'core/tutorials/beginners_line.html')  # Create this template

def tutorial_intermediate_histogram(request):
    return render(request, 'core/tutorials/intermediate_histogram.html')  # Create this template

def tutorial_intermediate_scatter(request):
    return render(request, 'core/tutorials/intermediate_scatter.html')  # Create this template

def tutorial_advanced_network(request):
    return render(request, 'core/tutorials/advanced_network.html')  # Create this template

def tutorial_advanced_3d(request):
    return render(request, 'core/tutorials/advanced_3d.html')

def tutorials_home(request):
    return render(request, 'core/tutorials_home.html')