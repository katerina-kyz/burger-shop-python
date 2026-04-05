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
        
        # Создаем бургеры
        burgers = [
            {
                'name': 'Чизбургер Классический',
                'category': classic,
                'description': 'Сочная говяжья котлета, расплавленный сыр чеддер, свежие овощи и фирменный соус',
                'composition': 'Говяжья котлета, сыр чеддер, салат, помидоры, лук, соус',
                'price': 250,
                'calories': 520
            },
            {
                'name': 'Двойной Гурман',
                'category': classic,
                'description': 'Две сочные котлеты, двойная порция сыра, бекон и специальный соус',
                'composition': '2 говяжьи котлеты, сыр чеддер, бекон, салат, помидоры, соус',
                'price': 380,
                'calories': 780
            },
            {
                'name': 'Острый Техасский',
                'category': spicy,
                'description': 'Пикантная котлета с халапеньо, острый соус и сыр с перцем',
                'composition': 'Говяжья котлета с перцем, сыр с халапеньо, салат, острый соус',
                'price': 320,
                'calories': 590
            },
            {
                'name': 'Вегетарианский Гарден',
                'category': vegetarian,
                'description': 'Нутовая котлета, свежие овощи, авокадо и веганский соус',
                'composition': 'Нутовая котлета, авокадо, салат, помидоры, огурцы, веганский соус',
                'price': 290,
                'calories': 430
            },
            {
                'name': 'Куриный Кранч',
                'category': chicken,
                'description': 'Хрустящая куриная котлета в панировке, сыр и соус ранч',
                'composition': 'Куриная котлета, сыр, салат, помидоры, соус ранч',
                'price': 270,
                'calories': 480
            },
            {
                'name': 'BBQ Бургер',
                'category': classic,
                'description': 'Котлета из мраморной говядины, карамелизованный лук, бекон и BBQ соус',
                'composition': 'Мраморная говядина, бекон, сыр, карамелизованный лук, BBQ соус',
                'price': 350,
                'calories': 650
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
                    'is_available': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан бургер: {burger.name}'))
        
        # Создаем точки выдачи
        points = [
            {
                'name': 'ТРЦ "Галерея"',
                'address': 'ул. Ленина, 10, 1 этаж',
                'latitude': 55.7558,
                'longitude': 37.6176,
                'working_hours': '10:00 - 22:00',
                'phone': '+7 (999) 111-11-11'
            },
            {
                'name': 'Метро "Парк культуры"',
                'address': 'Зубовский бульвар, 15',
                'latitude': 55.7345,
                'longitude': 37.5900,
                'working_hours': '09:00 - 21:00',
                'phone': '+7 (999) 222-22-22'
            },
            {
                'name': 'БЦ "Москва-Сити"',
                'address': 'Пресненская наб., 8, -1 этаж',
                'latitude': 55.7475,
                'longitude': 37.5400,
                'working_hours': '11:00 - 23:00',
                'phone': '+7 (999) 333-33-33'
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