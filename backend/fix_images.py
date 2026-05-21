import os, shutil, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
from base.models import Product

IMAGE_DIR = 'static/images'
IMGS = {
    'Engine': 'engine.jpg',
    'Transmission': 'gearbox.jpg',
    'Suspension': 'wheel.jpg',
    'Brakes': 'crankshaft.jpg',
    'Body': 'headlights.jpg',
    'Steering': 'powersteering.jpg',
}

for p in Product.objects.all():
    src = IMGS.get(p.category)
    if not src:
        print(f'SKIP {p.name}')
        continue
    fname = f'{p.category.lower()}_{p._id}.jpg'
    src_path = os.path.join(IMAGE_DIR, src)
    dst_path = os.path.join(IMAGE_DIR, fname)
    if os.path.exists(src_path) and not os.path.exists(dst_path):
        shutil.copy2(src_path, dst_path)
    p.image = fname
    p.save()
    print(f'OK {p.name} -> {fname}')

print('Done!')
