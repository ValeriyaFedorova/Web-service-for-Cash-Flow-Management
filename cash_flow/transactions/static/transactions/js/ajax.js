// AJAX функции для динамической загрузки категорий и подкатегорий
document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.getElementById('id_type');
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    // Загрузка категорий при изменении типа
    if (typeSelect && categorySelect) {
        typeSelect.addEventListener('change', function() {
            const typeId = this.value;
            if (typeId) {
                loadCategories(typeId);
            } else {
                categorySelect.innerHTML = '<option value="">---------</option>';
                subcategorySelect.innerHTML = '<option value="">---------</option>';
            }
        });
    }

    // Загрузка подкатегорий при изменении категории
    if (categorySelect && subcategorySelect) {
        categorySelect.addEventListener('change', function() {
            const categoryId = this.value;
            if (categoryId) {
                loadSubcategories(categoryId);
            } else {
                subcategorySelect.innerHTML = '<option value="">---------</option>';
            }
        });
    }

    function loadCategories(typeId) {
        fetch(`/ajax/load-categories/?type_id=${typeId}`)
            .then(response => response.json())
            .then(data => {
                categorySelect.innerHTML = '<option value="">---------</option>';
                data.forEach(function(category) {
                    const option = document.createElement('option');
                    option.value = category.id;
                    option.textContent = category.name;
                    categorySelect.appendChild(option);
                });
                
                // Сброс подкатегорий
                subcategorySelect.innerHTML = '<option value="">---------</option>';
            })
            .catch(error => console.error('Error loading categories:', error));
    }

    function loadSubcategories(categoryId) {
        fetch(`/ajax/load-subcategories/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {
                subcategorySelect.innerHTML = '<option value="">---------</option>';
                data.forEach(function(subcategory) {
                    const option = document.createElement('option');
                    option.value = subcategory.id;
                    option.textContent = subcategory.name;
                    subcategorySelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error loading subcategories:', error));
    }
});