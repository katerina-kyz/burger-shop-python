from django.core.management.base import BaseCommand
from main.models import BurgerCategory, Burger, PickupPoint

class Command(BaseCommand):
    help = 'Initialize database with initial data'

    def handle(self, *args, **options):
        # Создаем категории
        categories = [
            {'name': 'Классические', 'description': 'Традиционные бургеры с говядиной'},
            {'name': 'Острые', 'description': 'Для любителей погорячее'},
            {'name': 'Вегетарианские', 'description': 'Без мяса, но очень вкусные'},
            {'name': 'Куриные', 'description': 'Нежные бургеры с курицей'},
        ]
        
        for cat_data in categories:
            cat, created = BurgerCategory.objects.get_or_create(name=cat_data['name'])
            if created:
                cat.description = cat_data['description']
                cat.save()
                self.stdout.write(self.style.SUCCESS(f'Создана категория: {cat.name}'))
        
        # Получаем категории
        classic = BurgerCategory.objects.get(name='Классические')
        spicy = BurgerCategory.objects.get(name='Острые')
        vegetarian = BurgerCategory.objects.get(name='Вегетарианские')
        chicken = BurgerCategory.objects.get(name='Куриные')
        
        # Создаем бургеры с URL изображений
        burgers = [
            {
                'name': 'Чизбургер Классический',
                'category': classic,
                'description': 'Сочная говяжья котлета, расплавленный сыр чеддер, свежие овощи и фирменный соус',
                'composition': 'Говяжья котлета, сыр чеддер, салат, помидоры, лук, соус',
                'price': 250,
                'calories': 520,
                'image_url': 'https://i.postimg.cc/8PVrrbmX/burger.png'
            },
            {
                'name': 'Двойной Гурман',
                'category': classic,
                'description': 'Две сочные котлеты, двойная порция сыра, бекон и специальный соус',
                'composition': '2 говяжьи котлеты, сыр чеддер, бекон, салат, помидоры, соус',
                'price': 380,
                'calories': 780,
                'image_url': 'https://avatars.mds.yandex.net/get-shedevrum/14550299/img_65229b487ff811efb254c6c9289df30b/orig'
            },
            {
                'name': 'Острый Техасский',
                'category': spicy,
                'description': 'Пикантная котлета с халапеньо, острый соус и сыр с перцем',
                'composition': 'Говяжья котлета с перцем, сыр с халапеньо, салат, острый соус',
                'price': 320,
                'calories': 590,
                'image_url': 'https://static.tildacdn.com/tild3437-6138-4261-b463-376166363534/_____24.png'
            },
            {
                'name': 'Вегетарианский Гарден',
                'category': vegetarian,
                'description': 'Нутовая котлета, свежие овощи, авокадо и веганский соус',
                'composition': 'Нутовая котлета, авокадо, салат, помидоры, огурцы, веганский соус',
                'price': 290,
                'calories': 430,
                'image_url': 'https://img.povar.ru/mobile/c9/41/7b/34/vegetarianskii_burger_master-klass-510146.JPG'
            },
            {
                'name': 'Куриный Кранч',
                'category': chicken,
                'description': 'Хрустящая куриная котлета в панировке, сыр и соус ранч',
                'composition': 'Куриная котлета, сыр, салат, помидоры, соус ранч',
                'price': 270,
                'calories': 480,
                'image_url': 'https://avatars.mds.yandex.net/i?id=e9a7f97565fe9dc1e2230a3b0ca9c475_l-5176811-images-thumbs&n=13'
            },
            {
                'name': 'BBQ Бургер',
                'category': classic,
                'description': 'Котлета из мраморной говядины, карамелизованный лук, бекон и BBQ соус',
                'composition': 'Мраморная говядина, бекон, сыр, карамелизованный лук, BBQ соус',
                'price': 350,
                'calories': 650,
                'image_url': 'https://avatars.mds.yandex.net/get-eda/3808326/8ff58a9276f22ae11de4258561bed4fd/1200x1200nocrop'
            },
        ]
        
        for burger_data in burgers:
            burger, created = Burger.objects.get_or_create(
                name=burger_data['name'],
                defaults={
                    'category': burger_data['category'],
                    'description': burger_data['description'],
                    'composition': burger_data['composition'],
                    'price': burger_data['price'],
                    'calories': burger_data['calories'],
                    'image_url': burger_data['image_url'],
                    'is_available': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан бургер: {burger.name}'))
            else:
                # Если бургер уже существует, обновляем URL изображения
                burger.image_url = burger_data['image_url']
                burger.save()
                self.stdout.write(self.style.WARNING(f'Обновлён бургер: {burger.name}'))
        
        # Создаем точки выдачи
        points = [
            {
                'name': 'ТЦ "Звёздный"',
                'address': 'Коммунистическая ул., 7, Сыктывкар',
                'latitude': 61.6643,
                'longitude': 50.835,
                'working_hours': '10:00 - 21:00',
                'phone': '+7 (904) 271-16-05'
            },
            {
                'name': 'ТЦ "Июнь"',
                'address': 'Октябрьский пр., 133, Сыктывкар',
                'latitude': 61.6489,
                'longitude': 50.8094,
                'working_hours': '09:00 - 22:00',
                'phone': '+7 (8212) 28-88-88'
            },
            {
                'name': 'ТЦ "Парма"',
                'address': 'Коммунистическая ул., 50, Сыктывкар',
                'latitude': 61.6684,
                'longitude': 50.8359,
                'working_hours': '10:00 - 21:00',
                'phone': '+7 (8212) 46-86-03'
            },
        ]
        
        for point_data in points:
            point, created = PickupPoint.objects.get_or_create(
                name=point_data['name'],
                defaults={
                    'address': point_data['address'],
                    'latitude': point_data['latitude'],
                    'longitude': point_data['longitude'],
                    'working_hours': point_data['working_hours'],
                    'phone': point_data['phone']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана точка выдачи: {point.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ База данных успешно заполнена!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Статистика:'))
        self.stdout.write(self.style.SUCCESS(f'   - Категорий: {BurgerCategory.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Бургеров: {Burger.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Точек выдачи: {PickupPoint.objects.count()}'))