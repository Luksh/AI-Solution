from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from autoslug import AutoSlugField

# Create your models here.

class SoftwareSolution(models.Model):
    """Model for software solutions offered by AI-Solution"""
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False, max_length=200, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='solutions/', blank=True, null=True)
    features = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
  

class CaseStudy(models.Model):
    """Model for past solutions/case studies"""
    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    challenge = models.TextField()
    solution = models.TextField()
    results = models.TextField()
    image = models.ImageField(upload_to='case_studies/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.client_name}"

class Testimonial(models.Model):
    """Model for customer testimonials with ratings"""
    customer_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    testimonial = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.customer_name} - {self.company}"

class BlogPost(models.Model):
    """Model for blog posts/articles"""
    CATEGORY_CHOICES = [
        ('ai_technology', 'AI Technology'),
        ('machine_learning', 'Machine Learning'),
        ('data_science', 'Data Science'),
        ('business_intelligence', 'Business Intelligence'),
        ('industry_insights', 'Industry Insights'),
        ('case_studies', 'Case Studies'),
        ('company_news', 'Company News'),
    ]
    
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=200, null=True, blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='ai_technology')
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
        
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

class GalleryImage(models.Model):
    """Model for photo gallery images"""
    CATEGORY_CHOICES = [
        ('events', 'Events'),
        ('team', 'Team'),
        ('office', 'Office'),
        ('products', 'Products'),
        ('clients', 'Clients'),
        ('awards', 'Awards'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='events')
    event_name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.title

class Event(models.Model):
    """Model for upcoming events"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    registration_link = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Automatically set is_upcoming based on date
        self.is_upcoming = self.date > timezone.now()
        super().save(*args, **kwargs)

class ContactInquiry(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    job_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.company_name}"
    
    class Meta:
        verbose_name_plural = "Contact Inquiries"
    
class EventRegistration(models.Model):
    """Model for event registrations"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.event.title}"
