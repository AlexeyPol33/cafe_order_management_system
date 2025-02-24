from django.db import models


class Meal(models.Model):
    class Meta:
        verbose_name='Меню'
        indexes = [models.Index(fields=['id'])]
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')
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
        through='OrderMeal')
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status)

    @property
    def total_price(self):
        prices = [item.price for item in self.items.all()]
        return sum(prices)


class OrderMeal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)