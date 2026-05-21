"""Move new unique images to static/images/ and fix DB paths to match existing convention."""
import os, sys, shutil, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from base.models import Product

MEDIA_IMAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "images")
STATIC_IMAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "images")

os.makedirs(STATIC_IMAGES, exist_ok=True)

# Products with images/ prefix need to be moved to static/images/
fixed = 0
for p in Product.objects.all():
    img = str(p.image)
    if img.startswith("images/"):
        filename = img.replace("images/", "")
        src = os.path.join(MEDIA_IMAGES, filename)
        dst = os.path.join(STATIC_IMAGES, filename)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"COPIED {filename} → static/images/")
        
        # Update DB to just the filename (matching existing convention)
        p.image = filename
        p.save()
        print(f"FIXED  {p.name}: '{img}' → '{filename}'")
        fixed += 1

print(f"\nDone! Fixed {fixed} products.")
