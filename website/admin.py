from django.contrib import admin
from .models import (
    SoftwareSolution, 
    CaseStudy, 
    Testimonial, 
    BlogPost, 
    GalleryImage, 
    Event, 
    ContactInquiry,
    EventRegistration
)

# Register your models here.

@admin.register(SoftwareSolution)
class SoftwareSolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'features', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'industry', 'created_at')
    search_fields = ('title', 'client_name', 'industry')
    list_filter = ('industry', 'created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'client_name', 'industry', 'image')
        }),
        ('Case Details', {
            'fields': ('challenge', 'solution', 'results')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'company', 'position', 'rating', 'date')
    search_fields = ('customer_name', 'company', 'testimonial')
    list_filter = ('rating', 'date')
    list_editable = ('rating',)
    fieldsets = (
        (None, {
            'fields': ('customer_name', 'company', 'position', 'image')
        }),
        ('Testimonial Details', {
            'fields': ('testimonial', 'rating', 'date')
        }),
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    search_fields = ('title', 'content', 'author')
    list_filter = ('is_published', 'created_at')
    list_editable = ('is_published',)
    readonly_fields = ('created_at', 'updated_at', 'slug')  # Added slug to readonly_fields
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'featured_image')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Categorization', {
            'fields': ('category', 'tags'),
        }),
        ('Publication', {
            'fields': ('is_published', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_name', 'date')
    search_fields = ('title', 'description', 'event_name')
    list_filter = ('category', 'date', 'event_name')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image')
        }),
        ('Categorization', {
            'fields': ('category',)
        }),
        ('Event Details', {
            'fields': ('event_name', 'date')
        }),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_featured', 'is_upcoming')
    list_filter = ('is_featured', 'is_upcoming')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    list_editable = ('is_featured',)
    readonly_fields = ('is_upcoming',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image')
        }),
        ('Event Details', {
            'fields': ('date', 'location', 'registration_link', 'is_featured')
        }),
        ('Status', {
            'fields': ('is_upcoming',),
            'classes': ('collapse',)
        }),
    )

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'email', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'company_name', 'job_details')
    list_filter = ('is_read', 'created_at', 'country')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company_name', 'country', 'job_title')
        }),
        ('Inquiry Details', {
            'fields': ('job_details', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent adding contact inquiries directly from admin
        # They should only be created through the contact form
        return False


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event', 'email', 'phone', 'company', 'registered_at')
    list_filter = ('event', 'registered_at')
    search_fields = ('full_name', 'email', 'phone', 'company')
    date_hierarchy = 'registered_at'
    readonly_fields = ('registered_at',)
