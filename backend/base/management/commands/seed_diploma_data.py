"""
Management command to seed the PostgreSQL database with realistic
auto-parts data across all 6 RAG categories for diploma demonstration.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from base.models import Product


SEED_PRODUCTS = [
    # ── Engine ───────────────────────────────────────────────
    {
        "name": "Масляний фільтр Bosch F 026 407 157",
        "brand": "Bosch",
        "category": "Engine",
        "description": "Оригінальний масляний фільтр Bosch для двигунів 1.6–2.0 TDI. "
                       "Високоякісний фільтруючий елемент забезпечує ефективне очищення оливи.",
        "price": 285.00,
        "countInStock": 25,
        "rating": 4.8,
        "numReviews": 12,
    },
    {
        "name": "Ремінь ГРМ Gates PowerGrip T10476",
        "brand": "Gates",
        "category": "Engine",
        "description": "Ремінь газорозподільного механізму Gates для VW/Audi/Skoda 1.9–2.0 TDI. "
                       "Посилена конструкція з поліамідним кордом.",
        "price": 920.00,
        "countInStock": 10,
        "rating": 4.9,
        "numReviews": 8,
    },
    {
        "name": "Свічки запалювання NGK BKR6E",
        "brand": "NGK",
        "category": "Engine",
        "description": "Нікелеві свічки запалювання NGK для бензинових двигунів. "
                       "Стабільна іскра, довгий термін служби до 30 000 км.",
        "price": 135.00,
        "countInStock": 50,
        "rating": 4.7,
        "numReviews": 20,
    },
    # ── Transmission ─────────────────────────────────────────
    {
        "name": "Комплект зчеплення LUK 624 3934 09",
        "brand": "LUK",
        "category": "Transmission",
        "description": "Повний комплект зчеплення LUK (диск + кошик + підшипник) "
                       "для VW Golf VII 1.6 TDI. Оригінальна якість OEM.",
        "price": 4850.00,
        "countInStock": 5,
        "rating": 4.9,
        "numReviews": 6,
    },
    {
        "name": "Піввісь приводна SKF VKJC 1198",
        "brand": "SKF",
        "category": "Transmission",
        "description": "Приводна піввісь SKF для переднього мосту. "
                       "Комплект із ШРУС та пильниками. Гарантія 2 роки.",
        "price": 3200.00,
        "countInStock": 3,
        "rating": 4.6,
        "numReviews": 4,
    },
    # ── Suspension ───────────────────────────────────────────
    {
        "name": "Амортизатор Kayaba Excel-G 339766",
        "brand": "Kayaba",
        "category": "Suspension",
        "description": "Газомасляний амортизатор Kayaba Excel-G передній для Toyota Camry. "
                       "Технологія гідравлічного відбою для комфортної їзди.",
        "price": 2100.00,
        "countInStock": 8,
        "rating": 4.8,
        "numReviews": 15,
    },
    {
        "name": "Сайлентблок важеля Lemförder 37964 01",
        "brand": "Lemförder",
        "category": "Suspension",
        "description": "Сайлентблок переднього нижнього важеля Lemförder для BMW 3 (E90). "
                       "OEM-якість, натуральний каучук.",
        "price": 680.00,
        "countInStock": 12,
        "rating": 4.5,
        "numReviews": 7,
    },
    # ── Brakes ───────────────────────────────────────────────
    {
        "name": "Гальмівні колодки Brembo P 85 020",
        "brand": "Brembo",
        "category": "Brakes",
        "description": "Передні гальмівні колодки Brembo для VW/Audi/Skoda. "
                       "Керамічна суміш NAO, низький рівень шуму та пилу.",
        "price": 1450.00,
        "countInStock": 20,
        "rating": 4.9,
        "numReviews": 25,
    },
    {
        "name": "Гальмівний диск TRW DF6143",
        "brand": "TRW",
        "category": "Brakes",
        "description": "Вентильований гальмівний диск TRW для Toyota RAV4. "
                       "Антикорозійне покриття, діаметр 296 мм.",
        "price": 1200.00,
        "countInStock": 10,
        "rating": 4.7,
        "numReviews": 11,
    },
    # ── Body ─────────────────────────────────────────────────
    {
        "name": "Бампер передній Hyundai Tucson 2021+",
        "brand": "Hyundai OEM",
        "category": "Body",
        "description": "Оригінальний передній бампер для Hyundai Tucson NX4. "
                       "Незафарбований, з отворами під парктроніки.",
        "price": 7500.00,
        "countInStock": 2,
        "rating": 5.0,
        "numReviews": 3,
    },
    {
        "name": "Дзеркало бокове ліве VW Passat B8",
        "brand": "BLIC",
        "category": "Body",
        "description": "Бокове дзеркало з електрорегулюванням та обігрівом для VW Passat B8. "
                       "Корпус під фарбування.",
        "price": 2800.00,
        "countInStock": 4,
        "rating": 4.4,
        "numReviews": 5,
    },
    # ── Steering ─────────────────────────────────────────────
    {
        "name": "Рульова рейка Koyo для Toyota Corolla E210",
        "brand": "Koyo",
        "category": "Steering",
        "description": "Рульова рейка Koyo з електропідсилювачем для Toyota Corolla 2019+. "
                       "Відновлена на заводі, гарантія 1 рік.",
        "price": 12500.00,
        "countInStock": 2,
        "rating": 4.6,
        "numReviews": 3,
    },
    {
        "name": "Кермова тяга Moog RE-AX-7271",
        "brand": "Moog",
        "category": "Steering",
        "description": "Кермова тяга Moog з наконечником для Renault Megane III. "
                       "Посилений шарнір, термін служби до 80 000 км.",
        "price": 850.00,
        "countInStock": 15,
        "rating": 4.7,
        "numReviews": 9,
    },
]


class Command(BaseCommand):
    help = "Seed DB with 13 realistic auto-parts across 6 categories for diploma demo."

    def handle(self, *args, **options):
        # Use the first superuser (or first user) as the product owner
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.first()
        if not user:
            self.stdout.write(self.style.WARNING(
                "No users found. Creating a default admin user (admin / admin1234)."
            ))
            user = User.objects.create_superuser(
                username="admin",
                email="admin@apexpress.local",
                password="admin1234",
            )

        created_count = 0
        for item in SEED_PRODUCTS:
            _, created = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    "user": user,
                    "brand": item["brand"],
                    "category": item["category"],
                    "description": item["description"],
                    "price": item["price"],
                    "countInStock": item["countInStock"],
                    "rating": item["rating"],
                    "numReviews": item["numReviews"],
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Seeded {created_count} new products ({len(SEED_PRODUCTS)} total defined)."
        ))
