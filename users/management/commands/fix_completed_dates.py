from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Исправляет даты завершения для завершенных заявок'

    def handle(self, *args, **options):
        self.stdout.write('Исправление дат завершения для завершенных заявок...')
        
        # Находим все завершенные заявки без completed_at
        completed_orders = Order.objects.filter(
            status='completed',
            completed_at__isnull=True
        )
        
        updated_count = 0
        
        for order in completed_orders:
            # Устанавливаем дату завершения через 1-5 дней после создания
            completed_delta = timedelta(
                days=random.randint(1, 5),
                hours=random.randint(1, 8)
            )
            order.completed_at = order.created_at + completed_delta
            order.save()
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Обновлено {updated_count} завершенных заявок'
            )
        )
