document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("id_category");
    const subcategorySelect = document.getElementById("id_subcategory");

    if (!categorySelect || !subcategorySelect) {
        return;
    }

    // Save the original options, including data-category
    const originalOptions = Array.from(
        subcategorySelect.options
    ).map(function (option) {
        return {
            value: option.value,
            text: option.textContent,
            category: option.getAttribute("data-category"),
        };
    });

    function filterSubcategories() {
        const selectedCategory = categorySelect.value;
        const oldSubcategory = subcategorySelect.value;

        // Remove all existing options
        subcategorySelect.innerHTML = "";

        // Add empty option
        const emptyOption = new Option(
            "---------",
            "",
            false,
            false
        );

        subcategorySelect.appendChild(emptyOption);

        // Add only subcategories belonging to selected category
        originalOptions.forEach(function (optionData) {
            if (
                optionData.value &&
                optionData.category === selectedCategory
            ) {
                const option = new Option(
                    optionData.text,
                    optionData.value,
                    false,
                    optionData.value === oldSubcategory
                );

                option.setAttribute(
                    "data-category",
                    optionData.category
                );

                subcategorySelect.appendChild(option);
            }
        });

        // Clear old selection if it does not belong to selected category
        const exists = Array.from(
            subcategorySelect.options
        ).some(function (option) {
            return option.value === oldSubcategory;
        });

        if (!exists) {
            subcategorySelect.value = "";
        }

        // Update Jazzmin Select2
        if (window.jQuery) {
            window.jQuery(subcategorySelect).trigger("change");
        }
    }

    // Normal Django change event
    categorySelect.addEventListener(
        "change",
        filterSubcategories
    );

    // Jazzmin/Select2 change event
    if (window.jQuery) {
        window.jQuery(categorySelect).on(
            "change",
            filterSubcategories
        );
    }

    // Filter when the page first loads
    filterSubcategories();
});
