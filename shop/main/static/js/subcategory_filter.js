document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.querySelector('#id_category');
    const subCategorySelect = document.querySelector('#id_subcategory');

    if (!categorySelect || !subCategorySelect) return;

    const originalOptions = Array.from(subCategorySelect.options).map(option => {
        const match = option.textContent.match(/\[Cat:(\d+)\]$/); // look at the END of text
        const categoryId = match ? match[1] : null;
        const label = match ? option.textContent.replace(/\s*\[Cat:\d+\]$/, '') : option.textContent;

        return {
            value: option.value,
            label: label,
            categoryId: categoryId,
        };
    });

    function updateSubCategories() {
        const selectedCategoryId = categorySelect.value;
        subCategorySelect.innerHTML = '';

        const filtered = originalOptions.filter(opt => {
            return opt.categoryId === selectedCategoryId || opt.categoryId === null;
        });

        filtered.forEach(opt => {
            const option = document.createElement('option');
            option.value = opt.value;
            option.textContent = opt.label;
            subCategorySelect.appendChild(option);
        });
    }

    categorySelect.addEventListener('change', updateSubCategories);
    updateSubCategories();
});