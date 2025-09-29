from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import (
    SoftwareSolution, 
    CaseStudy, 
    Testimonial, 
    BlogPost, 
    GalleryImage, 
    Event, 
    ContactInquiry
)
from .forms import ContactForm, LoginForm
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse

from .gemini_chat import chat_with_gemini

import logging

# Configure logging
logger = logging.getLogger(__name__)

def chat(request):
    user_input = request.GET.get('message', '')
    if not user_input:
        return JsonResponse({'response': 'Please provide a message.'}, status=400)
    
    try:
        response = chat_with_gemini(user_input)
        if not response:
            response = "Sorry, I couldn't generate a response. Please try again."
        return JsonResponse({'response': response})
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return JsonResponse({'response': 'An error occurred while processing your request. Please try again later.'}, status=500)


class CustomAdminLoginView(LoginView):
    template_name = 'dashboard/login.html'
    form_class = AdminAuthenticationForm
    
    def get_success_url(self):
        # Check if there's a next parameter
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('admin:index')
        
def home(request):
    """View for the homepage"""
    # Get featured content for the homepage
    solutions = SoftwareSolution.objects.all()[:3]
    testimonials = Testimonial.objects.all().order_by('-date')[:3]
    case_studies = CaseStudy.objects.all()[:2]
    featured_events = Event.objects.filter(is_featured=True).order_by('date')[:2]
    
    context = {
        'solutions': solutions,
        'testimonials': testimonials,
        'case_studies': case_studies,
        'featured_events': featured_events,
    }
    return render(request, 'website/home.html', context)

def solutions(request):
    """View for software solutions page"""
    solutions = SoftwareSolution.objects.all()
    return render(request, 'website/solutions.html', {'solutions': solutions})

def solution_detail(request, slug):
    """View for individual solution detail page"""
    solution = get_object_or_404(SoftwareSolution, slug=slug)
    # Get other solutions for the "Other Solutions" section
    other_solutions = SoftwareSolution.objects.exclude(id=solution.id)[:3]
    
    context = {
        'solution': solution,
        'other_solutions': other_solutions,
    }
    return render(request, 'website/solution_detail.html', context)

def case_studies(request):
    """View for case studies/past solutions page"""
    case_studies = CaseStudy.objects.all()
    testimonials = Testimonial.objects.all().order_by('-date')[:3]
    return render(request, 'website/case_studies.html', {
        'case_studies': case_studies,
        'testimonials': testimonials
    })

def case_study_detail(request, id):
    """View for individual case study detail page"""
    case_study = get_object_or_404(CaseStudy, id=id)
    # Get other case studies for the "Related Case Studies" section
    related_case_studies = CaseStudy.objects.exclude(id=case_study.id)[:3]
    
    context = {
        'case_study': case_study,
        'related_case_studies': related_case_studies,
    }
    return render(request, 'website/case_study_detail.html', context)

def testimonials(request):
    """View for testimonials page"""
    testimonials = Testimonial.objects.all().order_by('-date')
    return render(request, 'website/testimonials.html', {'testimonials': testimonials})

def blog(request):
    """View for blog page"""
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    search = request.GET.get('search')
    
    all_posts = BlogPost.objects.filter(is_published=True)
    posts = all_posts.order_by('-created_at')
    
    # Apply filters if provided
    if category:
        posts = posts.filter(category=category)
    
    if tag:
        posts = posts.filter(tags__icontains=tag)
    
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search) |
            Q(author__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    # Get all categories and tags for the sidebar
    all_categories = dict(BlogPost.CATEGORY_CHOICES)
    
    # Get category counts
    category_counts = {}
    for cat_key, _ in BlogPost.CATEGORY_CHOICES:
        category_counts[cat_key] = all_posts.filter(category=cat_key).count()
    
    # Get all unique tags
    all_tags = []
    for post in all_posts:
        tags = post.get_tags_list()
        all_tags.extend(tags)
    all_tags = list(set(all_tags))
    
    # Get recent posts for sidebar
    recent_posts = all_posts.order_by('-created_at')[:5]
    
    context = {
        'posts': posts,
        'all_categories': all_categories,
        'category_counts': category_counts,
        'all_tags': all_tags,
        'recent_posts': recent_posts,
        'selected_category': category,
        'selected_tag': tag,
        'search_query': search,
        'total_posts': all_posts.count()
    }
    
    return render(request, 'website/blog.html', context)

def blog_post_detail(request, slug):
    """View for individual blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Get all categories and tags for the sidebar
    all_categories = dict(BlogPost.CATEGORY_CHOICES)
    
    # Get all unique tags
    all_tags = []
    for blog_post in BlogPost.objects.filter(is_published=True):
        tags = blog_post.get_tags_list()
        all_tags.extend(tags)
    all_tags = list(set(all_tags))
    
    # Get recent posts for sidebar
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id).order_by('-created_at')[:5]
    
    # Get related posts (same category or tags)
    post_tags = post.get_tags_list()
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(
        id=post.id
    ).filter(
        Q(category=post.category) | 
        Q(tags__icontains=','.join(post_tags)) if post_tags else Q()
    ).distinct()[:3]
    
    context = {
        'post': post,
        'all_categories': all_categories,
        'all_tags': all_tags,
        'recent_posts': recent_posts,
        'related_posts': related_posts,
        'post_tags': post_tags
    }
    
    return render(request, 'website/blog_post_detail.html', context)

def gallery(request):
    """View for photo gallery page"""
    # Get filter parameters from request
    category = request.GET.get('category')
    event = request.GET.get('event')
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    # Start with all images
    images = GalleryImage.objects.all()
    
    # Apply filters if provided
    if category and category != 'all':
        images = images.filter(category=category)
    
    if event:
        images = images.filter(event_name__icontains=event)
    
    if year:
        images = images.filter(date__year=year)
    
    if month:
        images = images.filter(date__month=month)
    
    # Order by date (newest first)
    images = images.order_by('-date')
    
    # Get all categories for the filter
    categories = dict(GalleryImage.CATEGORY_CHOICES)
    
    # Get all unique event names
    events = GalleryImage.objects.values_list('event_name', flat=True).distinct()
    events = [event for event in events if event]  # Remove None/empty values
    
    # Get years and months with images
    years = GalleryImage.objects.dates('date', 'year', order='DESC')
    months = GalleryImage.objects.dates('date', 'month', order='DESC')
    
    context = {
        'images': images,
        'categories': categories,
        'events': events,
        'years': years,
        'months': months,
        'selected_category': category,
        'selected_event': event,
        'selected_year': year,
        'selected_month': month
    }
    
    return render(request, 'website/gallery.html', context)

def events(request):
    """View for events page"""
    # This line gets events with dates in the future
    upcoming_events = Event.objects.filter(date__gt=timezone.now()).order_by('date')
    past_events = Event.objects.filter(date__lte=timezone.now()).order_by('-date')
    return render(request, 'website/events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    })

def contact(request):
    """View for contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been submitted successfully. We will contact you soon!')
            return redirect('website:contact')
    else:
        form = ContactForm()
    
    return render(request, 'website/contact.html', {'form': form})

def admin_login(request):
    """View for admin login"""
    if request.user.is_authenticated:
        return redirect('website:admin_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('website:admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions')
    else:
        form = LoginForm()
    
    return render(request, 'website/admin_login.html', {'form': form})

@login_required
def admin_logout(request):
    """View for admin logout"""
    logout(request)
    return redirect('website:admin_login')

@login_required
def admin_dashboard(request):
    """View for admin dashboard to track customer inquiries"""
    # Only staff/admin users can access this page
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page')
        return redirect('website:home')
    
    # Get all inquiries
    inquiries = ContactInquiry.objects.all().order_by('-created_at')
    
    # Get counts for dashboard stats
    total_inquiries = inquiries.count()
    unread_inquiries = inquiries.filter(is_read=False).count()
    read_inquiries = total_inquiries - unread_inquiries
    
    # Get inquiries by country for chart
    countries = ContactInquiry.objects.values('country').annotate(count=Count('country')).order_by('-count')
    
    context = {
        'inquiries': inquiries,
        'total_inquiries': total_inquiries,
        'unread_inquiries': unread_inquiries,
        'read_inquiries': read_inquiries,
        'countries': countries,
    }
    
    return render(request, 'website/admin_dashboard.html', context)

def test_logo(request):
    """Test view to check if the logo is accessible"""
    return render(request, 'website/test_logo.html')


from .models import Event, EventRegistration

def event_register(request):
    """Handle event registration form submission"""
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        job_title = request.POST.get('job_title')
        
        try:
            event = Event.objects.get(id=event_id)
            
            # Create registration record
            registration = EventRegistration(
                event=event,
                full_name=full_name,
                email=email,
                phone=phone,
                company=company,
                job_title=job_title
            )
            registration.save()
            
            # Send confirmation email (you can implement this later)
            
            messages.success(request, f"You have successfully registered for {event.title}. A confirmation email has been sent to your email address.")
            
        except Event.DoesNotExist:
            messages.error(request, "Event not found. Please try again.")
        
        return redirect('website:events')
    
    # If not POST, redirect to events page
    return redirect('website:events')


from django.shortcuts import get_object_or_404
from .models import Event

# Add this new view function
def event_detail(request, event_id):
    """View for individual event details"""
    event = get_object_or_404(Event, id=event_id)
    
    # Get related events (upcoming events in the same location)
    related_events = Event.objects.filter(
        is_upcoming=True, 
        location=event.location
    ).exclude(id=event.id)[:3]
    
    context = {
        'event': event,
        'related_events': related_events,
    }
    return render(request, 'website/event_detail.html', context)
