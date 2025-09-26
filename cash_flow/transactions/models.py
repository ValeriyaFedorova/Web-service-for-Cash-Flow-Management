from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    
    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('name', 'type')
        ordering = ['type__name', 'name']
    
    def __str__(self):
        return f"{self.name}"

class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ('name', 'category')
        ordering = ['category__name', 'name']
    
    def __str__(self):
        return f"{self.name}"

class Transaction(models.Model):
    created_date = models.DateField(
        default=timezone.now, 
        verbose_name="Дата создания"
    )
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT, 
        verbose_name="Статус"
    )
    type = models.ForeignKey(
        Type, 
        on_delete=models.PROTECT, 
        verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.PROTECT, 
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Сумма (руб)"
    )
    comment = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Комментарий",
        max_length=500
    )
   
    
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-created_date', '-id']
    
    def __str__(self):
        return f"{self.created_date} - {self.amount}р. - {self.type} - {self.category}"
    
    def get_amount_display(self):
        return f"{self.amount:,.2f} р.".replace(',', ' ')
