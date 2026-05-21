"""Populate English translations for all 24 products."""
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
from base.models import Product

# Map Ukrainian name substring → (English name, English description, English category)
TRANSLATIONS = {
    'Масляний фільтр Bosch': (
        'Bosch Oil Filter F 026 407 157',
        'Original Bosch oil filter for VAG group 1.6-2.0 TDI engines. Synthetic fiber filter element ensures 99.7% cleaning efficiency. Anti-drain valve prevents oil starvation during cold starts.',
        'Engine',
    ),
    'Ремінь ГРМ Gates': (
        'Gates PowerGrip Timing Belt T10476',
        'Gates timing belt for VW/Audi/Skoda with 1.9-2.0 TDI engines. Reinforced construction with polyamide cord and RPP profile teeth. Lifespan up to 120,000 km.',
        'Engine',
    ),
    'Свічки запалювання NGK': (
        'NGK Iridium IX Spark Plugs BKR6EIX',
        'NGK iridium spark plugs with 0.6mm center electrode. Improved cold start, stable spark under high loads. Lifespan up to 60,000 km.',
        'Engine',
    ),
    'Водяна помпа Hepu': (
        'Hepu Water Pump P657 for Toyota 1.6/1.8',
        'Hepu water pump with cast aluminum housing and ceramic seal for Toyota ZZ series engines. 15% improved cooling performance compared to OEM.',
        'Engine',
    ),
    'Комплект зчеплення Valeo': (
        'Valeo Clutch Kit 826317',
        'Complete Valeo clutch kit (228mm disc + pressure plate + bearing) for Renault/Dacia 1.5 dCi. Organic lining ensures smooth engagement and durability up to 150,000 km.',
        'Transmission',
    ),
    'Піввісь приводна SKF': (
        'SKF CV Drive Shaft VKJC 1198',
        'SKF front axle drive shaft for VW Golf VI/VII. Includes inner/outer CV joints and boots. Meets OE specification. 2-year warranty.',
        'Transmission',
    ),
    'Масло трансмісійне Motul': (
        'Motul Gear 300 Transmission Oil 75W-90 1L',
        'Fully synthetic Motul Gear 300 transmission oil for manual gearboxes and differentials. GL-4/GL-5 standards. Ensures smooth shifting even at temperatures down to -40°C.',
        'Transmission',
    ),
    'Підшипник вижимний INA': (
        'INA Clutch Release Bearing 500 0440 20',
        'INA clutch release bearing for Ford Focus II/III 1.6 TDCi. Hydraulic actuator, integrated cylinder. Concentricity accuracy ±0.1mm.',
        'Transmission',
    ),
    'Амортизатор KYB': (
        'KYB Excel-G Front Shock Absorber 339766',
        'KYB Excel-G gas-oil shock absorber for Toyota Camry XV50 front axle. Twin-tube technology with nitrogen charge. Restores factory suspension characteristics.',
        'Suspension',
    ),
    'Сайлентблок важеля Lemförder': (
        'Lemförder Control Arm Bushing 37964 01',
        'Lemförder front lower control arm bushing for BMW 3 (E90/F30). Natural rubber with vulcanized sleeve. OEM supplier for BMW Group.',
        'Suspension',
    ),
    'Пружина підвіски Lesjöfors': (
        'Lesjöfors Rear Suspension Spring 4072944',
        'Lesjöfors rear suspension spring for Skoda Octavia A7. Steel with anti-corrosion epoxy coating. Precise match to factory stiffness parameters.',
        'Suspension',
    ),
    'Стійка стабілізатора TRW': (
        'TRW Front Stabilizer Link JTS7515',
        'TRW front stabilizer link for Hyundai Tucson / Kia Sportage. Ball joint with polyurethane boot. Lifespan up to 80,000 km in urban conditions.',
        'Suspension',
    ),
    'Гальмівні колодки Brembo': (
        'Brembo Front Brake Pads P 85 020',
        'Brembo front brake pads for VW/Audi/Skoda MQB platform. NAO ceramic compound ensures low noise and dust levels. ECE R90 certified.',
        'Brakes',
    ),
    'Гальмівний диск TRW': (
        'TRW Ventilated Brake Disc DF6143',
        'TRW ventilated front brake disc for Toyota RAV4 / Camry. Diameter 296mm, thickness 26mm. EPB anti-corrosion coating provides protection up to 5 years.',
        'Brakes',
    ),
    'Супорт гальмівний ATE': (
        'ATE Brake Caliper 13.2381-8039.2',
        'ATE front brake caliper with single piston for Opel Astra J / Chevrolet Cruze. Factory remanufactured with new seals and guides. 1-year warranty.',
        'Brakes',
    ),
    'Гальмівна рідина DOT 4': (
        'Bosch Brake Fluid DOT 4 ENV6 1L',
        'Bosch ENV6 DOT 4 brake fluid with 265°C dry boiling point. Compatible with ABS/ESP/TCS systems. Recommended replacement interval — every 2 years.',
        'Brakes',
    ),
    'Бампер передній Hyundai': (
        'Hyundai Tucson NX4 2021+ Front Bumper',
        'Original front bumper for Hyundai Tucson NX4. Unpainted, with parking sensor and headlight washer openings. PP+EPDM material, UV resistant.',
        'Body',
    ),
    'Фара передня ліва Depo': (
        'Depo Left Front Headlight for VW Polo VI',
        'Depo left front headlight for VW Polo VI (AW) 2018+. Halogen, with LED daytime running lights. E4 certified. Analog OE 2G1 941 031.',
        'Body',
    ),
    'Дзеркало бокове ліве BLIC': (
        'BLIC Left Side Mirror for VW Passat B8',
        'Side mirror with electric adjustment, heating and turn signal indicator for VW Passat B8. Housing for painting. Aspherical anti-glare glass.',
        'Body',
    ),
    'Капот Kia Cerato': (
        'Kia Cerato BD 2019+ Steel Hood',
        'Original steel hood for Kia Cerato IV generation. Supplied with sound insulation and mounting hardware. Electrophoretic primer protection.',
        'Body',
    ),
    'Рульова рейка Koyo': (
        'Koyo Steering Rack for Toyota Corolla E210',
        'Koyo steering rack with electric power steering for Toyota Corolla 2019+. Factory remanufactured with all seals and bearings replaced. 1-year warranty.',
        'Steering',
    ),
    'Кермова тяга Moog': (
        'Moog Tie Rod RE-AX-7271',
        'Moog tie rod with end for Renault Megane III. Reinforced ball joint with grease fitting. Service life up to 80,000 km. TÜV certified.',
        'Steering',
    ),
    'Наконечник рульової тяги CTR': (
        'CTR Tie Rod End CEKH-48R',
        'CTR right tie rod end for Honda Civic X. Forged heat-treated components. Protective boot made of frost-resistant chloroprene rubber.',
        'Steering',
    ),
    'Насос ГПК Bosch': (
        'Bosch Power Steering Pump K S01 000 654',
        'Bosch power steering pump for Mercedes-Benz W211/W220. Vane-type, pressure up to 120 bar. New, not remanufactured. 2-year manufacturer warranty.',
        'Steering',
    ),
}

updated = 0
for product in Product.objects.all():
    for uk_substr, (en_name, en_desc, en_cat) in TRANSLATIONS.items():
        if uk_substr in product.name:
            product.name_en = en_name
            product.description_en = en_desc
            product.category_en = en_cat
            product.save()
            updated += 1
            print(f"OK {product.name} → {en_name}")
            break
    else:
        print(f"SKIP {product.name}")

print(f"\nDone! Updated {updated} products.")
