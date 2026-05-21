"""
Seed the PostgreSQL database with 24 realistic auto parts (4 per category)
with real product images downloaded from the internet.
"""

import os
import requests
from io import BytesIO

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from base.models import Product


# ── Real part images from Unsplash / Wikimedia ──────────────────────
# Each category has a pool of image URLs to rotate through
CATEGORY_IMAGES = {
    "Engine": [
        "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=600&q=80",
        "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&q=80",
        "https://images.unsplash.com/photo-1580894894513-541e068a3e2b?w=600&q=80",
        "https://images.unsplash.com/photo-1600712242805-5f78671b24da?w=600&q=80",
    ],
    "Transmission": [
        "https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?w=600&q=80",
        "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&q=80",
        "https://images.unsplash.com/photo-1530046339160-ce3e530c7d2f?w=600&q=80",
        "https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=600&q=80",
    ],
    "Suspension": [
        "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&q=80",
        "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&q=80",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=600&q=80",
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&q=80",
    ],
    "Brakes": [
        "https://images.unsplash.com/photo-1486006920555-c77dcf18193c?w=600&q=80",
        "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&q=80",
        "https://images.unsplash.com/photo-1449130255830-c55ed5f5e5e5?w=600&q=80",
        "https://images.unsplash.com/photo-1562911791-c7a97b729ec5?w=600&q=80",
    ],
    "Body": [
        "https://images.unsplash.com/photo-1520340356584-f9917d1eea6f?w=600&q=80",
        "https://images.unsplash.com/photo-1542362567-b07e54358753?w=600&q=80",
        "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=600&q=80",
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=600&q=80",
    ],
    "Steering": [
        "https://images.unsplash.com/photo-1449130255830-c55ed5f5e5e5?w=600&q=80",
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&q=80",
        "https://images.unsplash.com/photo-1542362567-b07e54358753?w=600&q=80",
        "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=600&q=80",
    ],
}


PRODUCTS = [
    # ═══════════════════ ENGINE (4) ═══════════════════
    {
        "name": "Масляний фільтр Bosch F 026 407 157",
        "brand": "Bosch",
        "category": "Engine",
        "description": (
            "Оригінальний масляний фільтр Bosch для двигунів 1.6–2.0 TDI "
            "групи VAG. Фільтруючий елемент з синтетичного волокна забезпечує "
            "ефективність очищення 99.7%. Антидренажний клапан запобігає "
            "масляному голодуванню при холодному пуску."
        ),
        "price": 285.00,
        "countInStock": 45,
        "rating": 4.8,
        "numReviews": 34,
    },
    {
        "name": "Ремінь ГРМ Gates PowerGrip T10476",
        "brand": "Gates",
        "category": "Engine",
        "description": (
            "Ремінь газорозподільного механізму Gates для VW/Audi/Skoda "
            "з двигунами 1.9–2.0 TDI. Посилена конструкція з поліамідним "
            "кордом та зубцями профілю RPP. Ресурс до 120 000 км."
        ),
        "price": 920.00,
        "countInStock": 18,
        "rating": 4.9,
        "numReviews": 22,
    },
    {
        "name": "Свічки запалювання NGK Iridium IX BKR6EIX",
        "brand": "NGK",
        "category": "Engine",
        "description": (
            "Іридієві свічки запалювання NGK з центральним електродом "
            "діаметром 0.6 мм. Покращений холодний пуск, стабільна іскра "
            "при високих навантаженнях. Ресурс до 60 000 км."
        ),
        "price": 245.00,
        "countInStock": 80,
        "rating": 4.7,
        "numReviews": 51,
    },
    {
        "name": "Водяна помпа Hepu P657 для Toyota 1.6/1.8",
        "brand": "Hepu",
        "category": "Engine",
        "description": (
            "Водяна помпа Hepu з литим алюмінієвим корпусом та "
            "керамічним ущільненням для двигунів Toyota серії ZZ. "
            "Підвищена продуктивність охолодження на 15% порівняно з OEM."
        ),
        "price": 1_350.00,
        "countInStock": 12,
        "rating": 4.6,
        "numReviews": 14,
    },

    # ═══════════════════ TRANSMISSION (4) ═══════════════════
    {
        "name": "Комплект зчеплення Valeo 826317",
        "brand": "Valeo",
        "category": "Transmission",
        "description": (
            "Повний комплект зчеплення Valeo (диск 228 мм + кошик + "
            "підшипник) для Renault/Dacia 1.5 dCi. Органічна накладка "
            "забезпечує плавне змикання та довговічність до 150 000 км."
        ),
        "price": 4_200.00,
        "countInStock": 7,
        "rating": 4.8,
        "numReviews": 16,
    },
    {
        "name": "Піввісь приводна SKF VKJC 1198",
        "brand": "SKF",
        "category": "Transmission",
        "description": (
            "Приводна піввісь SKF для переднього мосту VW Golf VI/VII. "
            "У комплекті ШРУС внутрішній/зовнішній та пильники. "
            "Відповідає специфікації OE. Гарантія 2 роки."
        ),
        "price": 3_450.00,
        "countInStock": 5,
        "rating": 4.6,
        "numReviews": 9,
    },
    {
        "name": "Масло трансмісійне Motul Gear 300 75W-90 1L",
        "brand": "Motul",
        "category": "Transmission",
        "description": (
            "Повністю синтетичне трансмісійне мастило Motul Gear 300 "
            "для механічних КПП та диференціалів. Стандарти GL-4/GL-5. "
            "Забезпечує чітке перемикання передач навіть при низьких "
            "температурах до -40°C."
        ),
        "price": 720.00,
        "countInStock": 30,
        "rating": 4.9,
        "numReviews": 28,
    },
    {
        "name": "Підшипник вижимний INA 500 0440 20",
        "brand": "INA",
        "category": "Transmission",
        "description": (
            "Вижимний підшипник зчеплення INA для Ford Focus II/III "
            "1.6 TDCi. Гідравлічний привод, інтегрований циліндр. "
            "Точність концентричності ±0.1 мм."
        ),
        "price": 1_850.00,
        "countInStock": 6,
        "rating": 4.5,
        "numReviews": 11,
    },

    # ═══════════════════ SUSPENSION (4) ═══════════════════
    {
        "name": "Амортизатор KYB Excel-G 339766 передній",
        "brand": "KYB",
        "category": "Suspension",
        "description": (
            "Газомасляний амортизатор KYB Excel-G для передньої осі "
            "Toyota Camry XV50. Twin-tube технологія з азотним "
            "підпором. Відновлює заводські характеристики підвіски."
        ),
        "price": 2_100.00,
        "countInStock": 14,
        "rating": 4.8,
        "numReviews": 38,
    },
    {
        "name": "Сайлентблок важеля Lemförder 37964 01",
        "brand": "Lemförder",
        "category": "Suspension",
        "description": (
            "Сайлентблок переднього нижнього важеля Lemförder для "
            "BMW 3 (E90/F30). Натуральний каучук з вулканізованою "
            "втулкою. OEM-постачальник для BMW Group."
        ),
        "price": 680.00,
        "countInStock": 22,
        "rating": 4.5,
        "numReviews": 15,
    },
    {
        "name": "Пружина підвіски Lesjöfors 4072944 задня",
        "brand": "Lesjöfors",
        "category": "Suspension",
        "description": (
            "Задня пружина підвіски Lesjöfors для Skoda Octavia A7. "
            "Сталь з антикорозійним епоксидним покриттям. Точна "
            "відповідність жорсткості заводських параметрів."
        ),
        "price": 950.00,
        "countInStock": 10,
        "rating": 4.4,
        "numReviews": 8,
    },
    {
        "name": "Стійка стабілізатора TRW JTS7515",
        "brand": "TRW",
        "category": "Suspension",
        "description": (
            "Передня стійка стабілізатора TRW для Hyundai Tucson / "
            "Kia Sportage. Шарнір з поліуретановим пильником. "
            "Ресурс до 80 000 км у міських умовах."
        ),
        "price": 420.00,
        "countInStock": 35,
        "rating": 4.3,
        "numReviews": 19,
    },

    # ═══════════════════ BRAKES (4) ═══════════════════
    {
        "name": "Гальмівні колодки Brembo P 85 020 передні",
        "brand": "Brembo",
        "category": "Brakes",
        "description": (
            "Передні гальмівні колодки Brembo для VW/Audi/Skoda "
            "платформи MQB. Керамічна суміш NAO забезпечує низький "
            "рівень шуму та пилоутворення. Сертифікація ECE R90."
        ),
        "price": 1_450.00,
        "countInStock": 25,
        "rating": 4.9,
        "numReviews": 42,
    },
    {
        "name": "Гальмівний диск TRW DF6143 вентильований",
        "brand": "TRW",
        "category": "Brakes",
        "description": (
            "Вентильований передній гальмівний диск TRW для Toyota "
            "RAV4 / Camry. Діаметр 296 мм, товщина 26 мм. "
            "Антикорозійне покриття EPB забезпечує захист до 5 років."
        ),
        "price": 1_200.00,
        "countInStock": 16,
        "rating": 4.7,
        "numReviews": 23,
    },
    {
        "name": "Супорт гальмівний ATE 13.2381-8039.2",
        "brand": "ATE",
        "category": "Brakes",
        "description": (
            "Передній гальмівний супорт ATE з одним поршнем для "
            "Opel Astra J / Chevrolet Cruze. Відновлений на заводі "
            "з новими манжетами та спрямовуючими. Гарантія 1 рік."
        ),
        "price": 2_800.00,
        "countInStock": 4,
        "rating": 4.6,
        "numReviews": 7,
    },
    {
        "name": "Гальмівна рідина DOT 4 Bosch ENV6 1L",
        "brand": "Bosch",
        "category": "Brakes",
        "description": (
            "Гальмівна рідина Bosch ENV6 класу DOT 4 із температурою "
            "кипіння 265°C (суха). Сумісна з ABS/ESP/TCS системами. "
            "Рекомендований інтервал заміни — кожні 2 роки."
        ),
        "price": 380.00,
        "countInStock": 40,
        "rating": 4.8,
        "numReviews": 31,
    },

    # ═══════════════════ BODY (4) ═══════════════════
    {
        "name": "Бампер передній Hyundai Tucson NX4 2021+",
        "brand": "Hyundai OEM",
        "category": "Body",
        "description": (
            "Оригінальний передній бампер для Hyundai Tucson NX4. "
            "Незафарбований, з отворами під парктроніки та омивач фар. "
            "Матеріал PP+EPDM, стійкий до ультрафіолету."
        ),
        "price": 7_500.00,
        "countInStock": 3,
        "rating": 5.0,
        "numReviews": 4,
    },
    {
        "name": "Фара передня ліва Depo для VW Polo VI",
        "brand": "Depo",
        "category": "Body",
        "description": (
            "Передня ліва фара Depo для VW Polo VI (AW) 2018+. "
            "Галогенна, з денними ходовими вогнями LED. "
            "Сертифікація E4. Аналог OE 2G1 941 031."
        ),
        "price": 4_200.00,
        "countInStock": 6,
        "rating": 4.3,
        "numReviews": 12,
    },
    {
        "name": "Дзеркало бокове ліве BLIC для Passat B8",
        "brand": "BLIC",
        "category": "Body",
        "description": (
            "Бокове дзеркало з електрорегулюванням, обігрівом та "
            "повторювачем повороту для VW Passat B8. Корпус під "
            "фарбування. Скло асферичне з антибліковим покриттям."
        ),
        "price": 2_800.00,
        "countInStock": 8,
        "rating": 4.4,
        "numReviews": 9,
    },
    {
        "name": "Капот Kia Cerato BD 2019+ (сталевий)",
        "brand": "Kia OEM",
        "category": "Body",
        "description": (
            "Оригінальний сталевий капот для Kia Cerato IV покоління. "
            "Поставляється з шумоізоляцією та кріпленнями. "
            "Захисне електрофорезне ґрунтування."
        ),
        "price": 6_800.00,
        "countInStock": 2,
        "rating": 4.7,
        "numReviews": 3,
    },

    # ═══════════════════ STEERING (4) ═══════════════════
    {
        "name": "Рульова рейка Koyo для Toyota Corolla E210",
        "brand": "Koyo",
        "category": "Steering",
        "description": (
            "Рульова рейка Koyo з електропідсилювачем для Toyota "
            "Corolla 2019+. Відновлена на заводі з заміною всіх "
            "ущільнень та підшипників. Гарантія 1 рік."
        ),
        "price": 12_500.00,
        "countInStock": 3,
        "rating": 4.6,
        "numReviews": 6,
    },
    {
        "name": "Кермова тяга Moog RE-AX-7271",
        "brand": "Moog",
        "category": "Steering",
        "description": (
            "Кермова тяга Moog з наконечником для Renault Megane III. "
            "Посилений кульовий шарнір з прес-масльонкою. "
            "Термін служби до 80 000 км. Сертифікація TÜV."
        ),
        "price": 850.00,
        "countInStock": 20,
        "rating": 4.7,
        "numReviews": 15,
    },
    {
        "name": "Наконечник рульової тяги CTR CEKH-48R",
        "brand": "CTR",
        "category": "Steering",
        "description": (
            "Правий рульовий наконечник CTR для Honda Civic X. "
            "Ковані комплектуючі з термообробкою. Захисний "
            "пильник із морозостійкого хлоропренового каучуку."
        ),
        "price": 520.00,
        "countInStock": 18,
        "rating": 4.5,
        "numReviews": 10,
    },
    {
        "name": "Насос ГПК Bosch K S01 000 654",
        "brand": "Bosch",
        "category": "Steering",
        "description": (
            "Насос гідропідсилювача керма Bosch для Mercedes-Benz "
            "W211/W220. Лопатево-пластинчастий тип, тиск до 120 бар. "
            "Новий, не відновлений. Гарантія виробника 2 роки."
        ),
        "price": 8_900.00,
        "countInStock": 2,
        "rating": 4.8,
        "numReviews": 5,
    },
]


def download_image(url, timeout=15):
    """Download an image from URL and return bytes + filename."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=timeout, stream=True)
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "image/jpeg")
        ext = "jpg"
        if "png" in content_type:
            ext = "png"
        elif "webp" in content_type:
            ext = "webp"

        return resp.content, ext
    except Exception as e:
        return None, str(e)


class Command(BaseCommand):
    help = "Seed DB with 24 realistic auto parts with real photos."

    def handle(self, *args, **options):
        # Get or create admin user
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.first()
        if not user:
            user = User.objects.create_superuser(
                "admin", "admin@apexpress.local", "admin1234"
            )

        # Clear old products
        old_count = Product.objects.count()
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING(
            f"🗑️  Deleted {old_count} old products."
        ))

        created = 0
        for i, item in enumerate(PRODUCTS):
            self.stdout.write(
                f"  [{i+1}/{len(PRODUCTS)}] {item['name']}...", ending=""
            )

            product = Product(
                user=user,
                name=item["name"],
                brand=item["brand"],
                category=item["category"],
                description=item["description"],
                price=item["price"],
                countInStock=item["countInStock"],
                rating=item["rating"],
                numReviews=item["numReviews"],
            )

            # Download and attach image
            cat = item["category"]
            img_urls = CATEGORY_IMAGES.get(cat, [])
            img_index = created % len(img_urls) if img_urls else 0

            if img_urls:
                img_data, ext = download_image(img_urls[img_index])
                if img_data:
                    filename = (
                        f"{cat.lower()}_{item['brand'].lower()}"
                        f"_{created+1}.{ext}"
                    )
                    product.image.save(
                        filename,
                        ContentFile(img_data),
                        save=False,
                    )
                    self.stdout.write(self.style.SUCCESS(" ✅ (image OK)"))
                else:
                    self.stdout.write(self.style.WARNING(f" ⚠️ (no image: {ext})"))
            else:
                self.stdout.write(self.style.WARNING(" ⚠️ (no URL)"))

            product.save()
            created += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"✅ Seeded {created} products with images across 6 categories!"
        ))
        self.stdout.write(
            f"📦 Total in DB: {Product.objects.count()}"
        )
