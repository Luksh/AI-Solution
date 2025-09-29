import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_solution.settings')
django.setup()

from website.models import BlogPost
from django.utils.text import slugify

def update_blog_slugs():
    """Update all blog posts with missing slugs"""
    blog_posts = BlogPost.objects.all()
    updated_count = 0
    
    for post in blog_posts:
        if not post.slug:
            # Generate a slug from the title
            base_slug = slugify(post.title)
            
            # Check if the slug already exists
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(id=post.id).exists():
                # If slug exists, append a number
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Update the post with the new slug
            post.slug = slug
            post.save()
            updated_count += 1
            print(f"Updated post '{post.title}' with slug '{post.slug}'")
    
    print(f"\nCompleted! Updated {updated_count} blog posts with slugs.")

if __name__ == "__main__":
    update_blog_slugs()
