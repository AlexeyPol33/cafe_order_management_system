from django.core.management.base import BaseCommand
import yaml
from orders.models import Meal


class Command(BaseCommand):
    help = 'Loads meal data from a YAML file into a database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to YAML file for data loading',
        )

    def handle(self, *args, **options):
        yaml_file_path = options['file']
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        for meal_data in data.get('meals',[]):
            try:
                meal = Meal.objects.create(
                    name = meal_data.get('name', None),
                    description = meal_data.get('description', ""),
                    price = meal_data.get('price', None)
                )
            except:
                pass
        self.stdout.write(self.style.SUCCESS('SUCCESS load'))
    
