"""
Assign AI-generated product images to DB products.
Run from backend dir: python assign_images.py
"""
import os, shutil, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()

from base.models import Product

BRAIN = r'C:\Users\gavri\.gemini\antigravity\brain\d0b94ceb-221e-4291-8fd9-caa8ac72bdf8'
IMG_DIR = 'static/images'

# Map: product name substring → generated image filename
IMAGE_MAP = {
    'Масляний фільтр': 'oil_filter',
    'Ремінь ГРМ': 'timing_belt',
    'Свічки запалювання': 'spark_plugs',
    'Водяна помпа': 'water_pump',
    'Комплект зчеплення': 'clutch_kit',
    'Піввісь приводна': 'drive_shaft',
    'Масло трансмісійне': 'transmission_oil',
    'Підшипник вижимний': 'clutch_bearing',
    'Амортизатор': 'shock_absorber',
    'Сайлентблок': 'silent_block',
    'Пружина підвіски': 'coil_spring',
    'Стійка стабілізатора': 'stabilizer_link',
    'Гальмівні колодки': 'brake_pads',
    'Гальмівний диск': 'brake_disc',
    'Супорт гальмівний': 'brake_caliper',
    'Гальмівна рідина': 'brake_fluid',
    'Бампер передній': 'car_bumper',
    'Фара передня': 'car_bumper',      # reuse bumper
    'Дзеркало бокове': 'car_bumper',    # reuse bumper
    'Капот': 'car_bumper',              # reuse bumper
    'Рульова рейка': 'drive_shaft',     # reuse drive shaft (similar shape)
    'Кермова тяга': 'stabilizer_link',  # reuse stabilizer (similar shape)
    'Наконечник рульової': 'clutch_bearing',  # reuse bearing
    'Насос ГПК': 'water_pump',          # reuse water pump (similar shape)
}

# Find all generated images in brain dir
generated = {}
for f in os.listdir(BRAIN):
    if f.endswith('.png'):
        base = f.rsplit('_', 1)[0]  # e.g. "oil_filter" from "oil_filter_123.png"
        generated[base] = os.path.join(BRAIN, f)

print(f"Found {len(generated)} generated images")

for product in Product.objects.all():
    matched_key = None
    for substring, img_key in IMAGE_MAP.items():
        if substring in product.name:
            matched_key = img_key
            break

    if not matched_key:
        print(f"SKIP {product.name} — no mapping")
        continue

    src = generated.get(matched_key)
    if not src:
        print(f"SKIP {product.name} — image '{matched_key}' not generated")
        continue

    dst_name = f"product_{product._id}.png"
    dst_path = os.path.join(IMG_DIR, dst_name)
    shutil.copy2(src, dst_path)
    product.image = dst_name
    product.save()
    print(f"OK {product.name} → {dst_name}")

print(f"\nDone! Updated {Product.objects.count()} products.")
