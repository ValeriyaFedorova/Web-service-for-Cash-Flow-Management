from django.urls import path
from . import views

urlpatterns = [
    # Основные маршруты для транзакций
    path('', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),
    path('delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
    
    # Управление справочниками
    path('dictionaries/', views.dictionary_management, name='dictionary_management'),
    path('dictionaries/edit/<str:model_type>/<int:pk>/', 
         views.edit_dictionary_item, name='edit_dictionary_item'),
    path('dictionaries/delete/<str:model_type>/<int:pk>/', 
         views.delete_dictionary_item, name='delete_dictionary_item'),
    
    # AJAX endpoints
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]