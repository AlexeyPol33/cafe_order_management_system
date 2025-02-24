from django.db import models


class Meal(models.Choices):
    class Meta:
        verbose_name='Меню'
        indexes = [models.Index(fields=['id'])]
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True)
    description = models.TextField(
        blank=True,
        null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоймость',
        )


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PEND', 'в ожидании'
        INPROGRESS = 'INPR', 'в процессе'
        COMPLETED = 'COMP', 'завершен'
        CANCELED = 'CANC', 'отменен'

    class Meta:
        ordering = ['-status']
        indexes = [models.Index(fields=['-id'])]

    table_number = models.IntegerField()
    items = models.ManyToManyField(
        to=Meal,
        related_name='orders',
        through='order_meal')
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status)

    @property
    def total_price(self):
        prices = [item.price for item in self.items.all()]
        return  sum(prices)
