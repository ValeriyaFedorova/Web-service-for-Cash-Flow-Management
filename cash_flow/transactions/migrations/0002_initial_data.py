from django.db import migrations

def create_initial_data(apps, schema_editor):
    Status = apps.get_model('transactions', 'Status')
    Type = apps.get_model('transactions', 'Type')
    Category = apps.get_model('transactions', 'Category')
    Subcategory = apps.get_model('transactions', 'Subcategory')
    
    # Статусы
    statuses = ['Бизнес', 'Личное', 'Налог']
    for status_name in statuses:
        Status.objects.get_or_create(name=status_name)
    
    # Типы
    types = ['Пополнение', 'Списание']
    for type_name in types:
        Type.objects.get_or_create(name=type_name)
    
    # Категории и подкатегории
    type_income = Type.objects.get(name='Пополнение')
    type_expense = Type.objects.get(name='Списание')
    
    # Категории для пополнения
    income_categories = [
        ('Зарплата', ['Аванс', 'Премия']),
        ('Инвестиции', ['Акции', 'Облигации', 'Депозиты']),
        ('Фриланс', ['Разработка', 'Дизайн', 'Консультации']),
    ]
    
    # Категории для списания
    expense_categories = [
        ('Инфраструктура', ['VPS', 'Proxy', 'Хостинг', 'Домены']),
        ('Маркетинг', ['Farpost', 'Avito', 'Контекстная реклама', 'SMM']),
        ('Продукты', ['Супермаркет', 'Рынок', 'Доставка']),
        ('Транспорт', ['Бензин', 'Общественный транспорт', 'Такси']),
        ('Развлечения', ['Кино', 'Рестораны', 'Концерты']),
    ]
    
    for cat_name, subcats in income_categories:
        category, created = Category.objects.get_or_create(name=cat_name, type=type_income)
        for subcat_name in subcats:
            Subcategory.objects.get_or_create(name=subcat_name, category=category)
    
    for cat_name, subcats in expense_categories:
        category, created = Category.objects.get_or_create(name=cat_name, type=type_expense)
        for subcat_name in subcats:
            Subcategory.objects.get_or_create(name=subcat_name, category=category)

class Migration(migrations.Migration):
    dependencies = [
        ('transactions', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(create_initial_data),
    ]