"""Fix remaining 3 products with unique images from working URLs."""
import os, django, requests
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
from base.models import Product

IMG_DIR = 'static/images'

# Alternative URLs - these are verified working
FIXES = {
    'Дзеркало бокове': 'https://images.unsplash.com/photo-1489824904134-891ab64532f1?w=600&q=80',
    'Кермова тяга': 'https://images.unsplash.com/photo-1486006920555-c77dcf18193c?w=600&q=80',
    'Наконечник рульової': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&q=80',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for product in Product.objects.all():
    matched = None
    for sub in FIXES:
        if sub in product.name:
            matched = sub
            break
    if not matched:
        continue

    url = FIXES[matched]
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

print("Done!")
