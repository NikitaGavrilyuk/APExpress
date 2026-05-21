"""
Download unique product images for 7 products that were sharing images.
Run from backend dir: python download_unique_images.py
"""
import os, django, requests, shutil
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
from base.models import Product

IMG_DIR = 'static/images'

# Real product image URLs for each specific product
PRODUCT_IMAGES = {
    'Фара передня': 'https://images.unsplash.com/photo-1552642762-f55d06580015?w=600&q=80',
    'Дзеркало бокове': 'https://images.unsplash.com/photo-1609073120766-9cfb0c79ac5b?w=600&q=80',
    'Капот': 'https://images.unsplash.com/photo-1606577924006-27d39b132ae2?w=600&q=80',
    'Рульова рейка': 'https://images.unsplash.com/photo-1600712242805-5f78671b24da?w=600&q=80',
    'Кермова тяга': 'https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&q=80',
    'Наконечник рульової': 'https://images.unsplash.com/photo-1449130255830-c55ed5f5e5e5?w=600&q=80',
    'Насос ГПК': 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=600&q=80',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for product in Product.objects.all():
    matched_key = None
    for substring in PRODUCT_IMAGES:
        if substring in product.name:
            matched_key = substring
            break

    if not matched_key:
        continue

    url = PRODUCT_IMAGES[matched_key]
    fname = f"unique_{product._id}.jpg"
    fpath = os.path.join(IMG_DIR, fname)

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        with open(fpath, 'wb') as f:
            f.write(resp.content)
        product.image = fname
        product.save()
        print(f"OK {product.name} → {fname} ({len(resp.content)} bytes)")
    except Exception as e:
        print(f"FAIL {product.name}: {e}")

print("\nDone!")
