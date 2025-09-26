from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from .models import Transaction, Status, Type, Category, Subcategory
from .forms import TransactionForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm

def transaction_list(request):
    # Получаем все транзакции с предзагрузкой связанных данных
    transactions = Transaction.objects.all().select_related(
        'status', 'type', 'category', 'subcategory'
    ).order_by('-created_date', '-id')
    
    # Инициализируем фильтры
    filters = Q()
    filter_applied = False
    filter_params = {}
    
    # Обработка параметров фильтрации
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    status_id = request.GET.get('status', '')
    type_id = request.GET.get('type', '')
    category_id = request.GET.get('category', '')
    subcategory_id = request.GET.get('subcategory', '')
    
    # Сохраняем параметры фильтрации
    filter_params = {
        'date_from': date_from,
        'date_to': date_to,
        'status': status_id,
        'type': type_id,
        'category': category_id,
        'subcategory': subcategory_id,
    }
    
    # Применяем фильтры
    if date_from:
        filters &= Q(created_date__gte=date_from)
        filter_applied = True
    if date_to:
        filters &= Q(created_date__lte=date_to)
        filter_applied = True
    if status_id:
        filters &= Q(status_id=status_id)
        filter_applied = True
    if type_id:
        filters &= Q(type_id=type_id)
        filter_applied = True
    if category_id:
        filters &= Q(category_id=category_id)
        filter_applied = True
    if subcategory_id:
        filters &= Q(subcategory_id=subcategory_id)
        filter_applied = True
    
    # Применяем фильтры к queryset
    if filter_applied:
        transactions = transactions.filter(filters)
    
    # Пагинация
    paginator = Paginator(transactions, 25)  # 25 записей на страницу
    page = request.GET.get('page')
    
    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)
    
    # Расчет статистики
    total_count = Transaction.objects.count()
    filtered_count = transactions.count()
    
    # Общая статистика
    overall_stats = Transaction.objects.aggregate(
        total_income=Sum('amount', filter=Q(type__name='Пополнение')),
        total_expense=Sum('amount', filter=Q(type__name='Списание')),
    )
    
    overall_income = overall_stats['total_income'] or 0
    overall_expense = overall_stats['total_expense'] or 0
    overall_balance = overall_income - overall_expense
    
    # Статистика по фильтрованным данным
    filtered_stats = transactions.aggregate(
        total_income=Sum('amount', filter=Q(type__name='Пополнение')),
        total_expense=Sum('amount', filter=Q(type__name='Списание')),
    )
    
    filtered_income = filtered_stats['total_income'] or 0
    filtered_expense = filtered_stats['total_expense'] or 0
    filtered_balance = filtered_income - filtered_expense
    
    # Статистика по категориям
    category_stats = transactions.values(
        'category__name', 'type__name'
    ).annotate(
        total_amount=Sum('amount'),
        count=Count('id')
    ).order_by('-total_amount')[:10]
    
    # Получаем данные для фильтров
    statuses = Status.objects.all().order_by('name')
    types = Type.objects.all().order_by('name')
    categories = Category.objects.all().select_related('type').order_by('type__name', 'name')
    subcategories = Subcategory.objects.all().select_related('category').order_by('category__name', 'name')
    
    context = {
        'transactions': transactions_page,
        'page_obj': transactions_page,
        'is_paginated': paginator.num_pages > 1,
        
        'filter_params': filter_params,
        'filter_applied': filter_applied,
        
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
        
        # Статистика
        'total_count': total_count,
        'filtered_count': filtered_count,
        'overall_income': overall_income,
        'overall_expense': overall_expense,
        'overall_balance': overall_balance,
        'filtered_income': filtered_income,
        'filtered_expense': filtered_expense,
        'filtered_balance': filtered_balance,
        'category_stats': category_stats,
    }
    
    return render(request, 'transactions/transaction_list.html', context)

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            messages.success(request, f'Запись успешно создана!')
            return redirect('transaction_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TransactionForm()
    
    context = {
        'form': form,
        'title': 'Создание новой записи о движении денежных средств',
        'submit_text': 'Создать запись',
    }
    return render(request, 'transactions/transaction_form.html', context)

def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, f'Запись успешно обновлена!')
            return redirect('transaction_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TransactionForm(instance=transaction)
    
    context = {
        'form': form,
        'title': f'Редактирование записи',
        'submit_text': 'Сохранить изменения',
        'transaction': transaction,
    }
    return render(request, 'transactions/transaction_form.html', context)

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    
    if request.method == 'POST':
        transaction_id = transaction.id
        transaction.delete()
        messages.success(request, f'Запись успешно удалена!')
        return redirect('transaction_list')
    
    context = {
        'transaction': transaction,
        'back_url': request.META.get('HTTP_REFERER', '/'),
    }
    return render(request, 'transactions/transaction_confirm_delete.html', context)

def dictionary_management(request):
    # Обработка добавления новых элементов
    if request.method == 'POST':
        model_type = request.POST.get('model_type')
        form = None
        
        if model_type == 'status':
            form = StatusForm(request.POST)
        elif model_type == 'type':
            form = TypeForm(request.POST)
        elif model_type == 'category':
            form = CategoryForm(request.POST)
        elif model_type == 'subcategory':
            form = SubcategoryForm(request.POST)
        
        if form and form.is_valid():
            item = form.save()
            messages.success(request, f'Элемент "{item.name}" успешно добавлен в справочник!')
            return redirect('dictionary_management')
        else:
            messages.error(request, 'Ошибка при добавлении элемента. Проверьте данные.')
    
    context = {
        'statuses': Status.objects.all().order_by('name'),
        'types': Type.objects.all().order_by('name'),
        'categories': Category.objects.all().select_related('type').order_by('type__name', 'name'),
        'subcategories': Subcategory.objects.all().select_related('category').order_by('category__name', 'name'),
        
        'status_form': StatusForm(),
        'type_form': TypeForm(),
        'category_form': CategoryForm(),
        'subcategory_form': SubcategoryForm(),
    }
    return render(request, 'transactions/dictionary_management.html', context)

def edit_dictionary_item(request, model_type, pk):
    models_map = {
        'status': (Status, StatusForm),
        'type': (Type, TypeForm),
        'category': (Category, CategoryForm),
        'subcategory': (Subcategory, SubcategoryForm),
    }
    
    if model_type not in models_map:
        messages.error(request, 'Неверный тип справочника')
        return redirect('dictionary_management')
    
    model_class, form_class = models_map[model_type]
    item = get_object_or_404(model_class, pk=pk)
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Элемент "{item.name}" успешно обновлен!')
            return redirect('dictionary_management')
        else:
            messages.error(request, 'Ошибка при обновлении элемента.')
    else:
        form = form_class(instance=item)
    
    context = {
        'form': form,
        'item': item,
        'model_type': model_type,
        'title': f'Редактирование: {item.name}',
    }
    return render(request, 'transactions/dictionary_edit.html', context)

@require_http_methods(["POST"])
def delete_dictionary_item(request, model_type, pk):
    models_map = {
        'status': Status,
        'type': Type,
        'category': Category,
        'subcategory': Subcategory,
    }
    
    if model_type not in models_map:
        messages.error(request, 'Неверный тип справочника')
        return redirect('dictionary_management')
    
    model_class = models_map[model_type]
    item = get_object_or_404(model_class, pk=pk)
    item_name = item.name
    
    # Проверка на использование в транзакциях
    if model_type == 'status' and Transaction.objects.filter(status=item).exists():
        messages.error(request, f'Нельзя удалить статус "{item_name}", так как он используется в транзакциях!')
    elif model_type == 'type' and (Category.objects.filter(type=item).exists() or 
                                  Transaction.objects.filter(type=item).exists()):
        messages.error(request, f'Нельзя удалить тип "{item_name}", так как он используется в категориях или транзакциях!')
    elif model_type == 'category' and (Subcategory.objects.filter(category=item).exists() or 
                                     Transaction.objects.filter(category=item).exists()):
        messages.error(request, f'Нельзя удалить категорию "{item_name}", так как она используется в подкатегориях или транзакциях!')
    elif model_type == 'subcategory' and Transaction.objects.filter(subcategory=item).exists():
        messages.error(request, f'Нельзя удалить подкатегорию "{item_name}", так как она используется в транзакциях!')
    else:
        item.delete()
        messages.success(request, f'Элемент "{item_name}" успешно удален из справочника!')
    
    return redirect('dictionary_management')

# AJAX views
def load_categories(request):
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(type_id=type_id).order_by('name')
        categories_data = [{'id': cat.id, 'name': cat.name} for cat in categories]
    else:
        categories_data = []
    return JsonResponse(categories_data, safe=False)

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
        subcategories_data = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
    else:
        subcategories_data = []
    return JsonResponse(subcategories_data, safe=False)