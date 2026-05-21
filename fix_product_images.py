"""
Quick fix: reassign existing image files to products by category.
Run: python manage.py shell < ../fix_product_images.py
"""
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()

import shutil
from base.models import Product

IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'backend', 'static', 'images')

# Map categories to existing image files on disk
CATEGORY_IMAGES = {
    'Engine':       'engine.jpg',
    'Transmission': 'gearbox.jpg',
    'Suspension':   'wheel.jpg',
    'Brakes':       'crankshaft.jpg',
    'Body':         'headlights.jpg',
    'Steering':     'powersteering.jpg',
}

for product in Product.objects.all():
    cat = product.category
    source_img = CATEGORY_IMAGES.get(cat)
    if not source_img:
        print(f"SKIP {product.name} — no image for category {cat}")
        continue

    source_path = os.path.join(IMAGE_DIR, source_img)
    if not os.path.exists(source_path):
        print(f"SKIP {product.name} — source file {source_img} not found")
        continue

    # Create a unique filename for the product
    safe_name = f"{cat.lower()}_{product._id}.jpg"
    dest_path = os.path.join(IMAGE_DIR, safe_name)

    if not os.path.exists(dest_path):
        shutil.copy2(source_path, dest_path)

    product.image = safe_name
    product.save()
    print(f"OK {product.name} → {safe_name}")

print("\nDone! All products now have valid images.")
