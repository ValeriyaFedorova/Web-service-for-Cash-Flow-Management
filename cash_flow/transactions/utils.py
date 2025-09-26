def initialize_default_data():
    """Функция для инициализации начальных данных"""
    from .models import Status, Type, Category, Subcategory
    
    # Создание статусов по умолчанию
    default_statuses = ['Бизнес', 'Личное', 'Налог']
    for status_name in default_statuses:
        Status.objects.get_or_create(name=status_name)
    
    # Создание типов по умолчанию
    default_types = ['Пополнение', 'Списание']
    for type_name in default_types:
        Type.objects.get_or_create(name=type_name)
    
    print("Default data initialized successfully!")