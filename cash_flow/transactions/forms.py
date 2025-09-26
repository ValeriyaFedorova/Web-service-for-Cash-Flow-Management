from django import forms
from .models import Transaction, Status, Type, Category, Subcategory

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['created_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'comment': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Введите комментарий (необязательно)',
                'maxlength': '500'
            }),
            'amount': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0.01',
                'class': 'form-control',
                'required': 'required',
                'placeholder': '0.00'
            }),
        }
        labels = {
            'created_date': 'Дата операции *',
            'status': 'Статус *',
            'type': 'Тип операции *',
            'category': 'Категория *',
            'subcategory': 'Подкатегория *',
            'amount': 'Сумма (руб) *',
            'comment': 'Комментарий',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Добавляем классы Bootstrap ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'comment':  # comment уже настроен
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
            if field.required:
                field.widget.attrs['required'] = 'required'
        
        # Устанавливаем пустой label для обязательных полей
        self.fields['status'].empty_label = "Выберите статус"
        self.fields['type'].empty_label = "Выберите тип операции"
        self.fields['category'].empty_label = "Сначала выберите тип"
        self.fields['subcategory'].empty_label = "Сначала выберите категорию"
        
        # Для новой записи устанавливаем текущую дату по умолчанию
        if not self.instance.pk:  # Если это создание новой записи
            from django.utils import timezone
            self.fields['created_date'].initial = timezone.now().date()
        
        # Динамическая загрузка категорий и подкатегорий
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                self.fields['category'].queryset = Category.objects.none()
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.type.category_set.all()
        else:
            self.fields['category'].queryset = Category.objects.none()
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = Subcategory.objects.none()
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сумма должна быть больше нуля")
        return amount

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название статуса',
                'maxlength': '100'
            }),
        }
        labels = {
            'name': 'Название статуса',
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название типа операции',
                'maxlength': '100'
            }),
        }
        labels = {
            'name': 'Название типа',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название категории',
                'maxlength': '100'
            }),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название категории',
            'type': 'Тип операции',
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название подкатегории',
                'maxlength': '100'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название подкатегории',
            'category': 'Категория',
        }