"""
Management command to migrate products from old SQLite database
and assign appropriate images to all products.
"""

import sqlite3
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from base.models import Product


# Map seeded products to existing image files
IMAGE_MAP = {
    "Engine": "engine.jpg",
    "Transmission": "gearbox.jpg",
    "Suspension": "wheel.jpg",
    "Brakes": "crankshaft.jpg",
    "Body": "headlights.jpg",
    "Steering": "powersteering.jpg",
}


class Command(BaseCommand):
    help = "Migrate products from old SQLite DB and assign images."

    def handle(self, *args, **options):
        sqlite_path = settings.BASE_DIR.parent / "backend" / "db.sqlite3"

        # ── Step 1: Import old SQLite products ──────────────────
        if sqlite_path.exists():
            self.stdout.write(f"Found SQLite DB at {sqlite_path}")
            try:
                conn = sqlite3.connect(str(sqlite_path))
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute(
                    "SELECT name, image, brand, category, description, "
                    "price, countInStock, rating, numReviews "
                    "FROM base_product"
                )
                rows = cur.fetchall()
                conn.close()

                user = User.objects.first()
                imported = 0
                for row in rows:
                    _, created = Product.objects.get_or_create(
                        name=row["name"],
                        defaults={
                            "user": user,
                            "image": row["image"] or "",
                            "brand": row["brand"] or "",
                            "category": row["category"] or "",
                            "description": row["description"] or "",
                            "price": row["price"],
                            "countInStock": row["countInStock"] or 0,
                            "rating": row["rating"],
                            "numReviews": row["numReviews"] or 0,
                        },
                    )
                    if created:
                        imported += 1

                self.stdout.write(self.style.SUCCESS(
                    f"✅ Imported {imported} products from SQLite ({len(rows)} total in old DB)."
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ SQLite import error: {e}"))
        else:
            self.stdout.write(self.style.WARNING(
                f"No SQLite DB found at {sqlite_path}, skipping import."
            ))

        # ── Step 2: Assign images to seeded products that have none ─
        products_without_images = Product.objects.filter(
            image=""
        ) | Product.objects.filter(image__isnull=True)

        updated = 0
        for product in products_without_images:
            cat = product.category or ""
            img = IMAGE_MAP.get(cat, "engine.jpg")
            product.image = img
            product.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Assigned images to {updated} products without images."
        ))

        # Summary
        total = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"\n📦 Total products in PostgreSQL: {total}"
        ))
