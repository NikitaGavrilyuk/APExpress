"""
Copy generated unique images to media/images/ and update the Product model.
"""
import os, sys, shutil, django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from base.models import Product

ARTIFACT_DIR = r"C:\Users\gavri\.gemini\antigravity\brain\d0b94ceb-221e-4291-8fd9-caa8ac72bdf8"
MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "images")

# Map: substring in product name → generated image filename
IMAGE_MAP = {
    "Фара":        "headlight_depo_1772387590444.png",
    "Дзеркало":    "side_mirror_blic_1772387546397.png",
    "Капот":       "hood_kia_cerato_1772387564385.png",
    "Рульова рейка": "steering_rack_koyo_1772387607011.png",
    "Кермова тяга":  "tie_rod_moog_1772387624260.png",
    "Наконечник":    "tie_rod_end_ctr_1772387663880.png",
    "Насос ГПК":     "power_steering_pump_1772387679064.png",
}

os.makedirs(MEDIA_DIR, exist_ok=True)

updated = 0
for keyword, img_file in IMAGE_MAP.items():
    src = os.path.join(ARTIFACT_DIR, img_file)
    if not os.path.exists(src):
        print(f"SKIP {keyword}: {img_file} not found")
        continue

    # Copy to media/images/
    dst = os.path.join(MEDIA_DIR, img_file)
    shutil.copy2(src, dst)

    # Update product in DB
    products = Product.objects.filter(name__icontains=keyword)
    for p in products:
        p.image = f"images/{img_file}"
        p.save()
        print(f"OK {p.name} → {img_file}")
        updated += 1

print(f"\nDone! Updated {updated} products.")
