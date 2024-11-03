document.addEventListener('DOMContentLoaded', function () {
    const headers = document.querySelectorAll('.inline-related th');
    const urlParams = new URLSearchParams(window.location.search);
    let currentOrderBy = urlParams.get('order_by') ? urlParams.get('order_by').split(',') : [];
    let currentOrderDir = urlParams.get('order_dir') ? urlParams.get('order_dir').split(',') : [];
    const maxSortColumns = 5;

    headers.forEach(header => {
        const fieldName = header.innerText.trim().toLowerCase();

        if (fieldName === 'delete?') return;

        header.classList.add('sortable');
        header.dataset.sort = fieldName;
        header.style.cursor = 'pointer';

        const fieldIndex = currentOrderBy.indexOf(fieldName);
        if (fieldIndex > -1) {
            const icon = document.createElement('span');
            icon.classList.add('sort-icon');
            icon.innerText = currentOrderDir[fieldIndex] === 'asc' ? '▲' : '▼';

            if (currentOrderBy.length > 1) {
                const orderIndex = document.createElement('sup');
                orderIndex.innerText = fieldIndex + 1;
                icon.prepend(orderIndex);
            }

            header.prepend(icon);
        }

        header.addEventListener('click', () => {
            const fieldIndex = currentOrderBy.indexOf(fieldName);
            let newDirection = 'asc';

            if (fieldIndex > -1) {
                newDirection = currentOrderDir[fieldIndex] === 'asc' ? 'desc' : 'asc';
                currentOrderBy.splice(fieldIndex, 1);
                currentOrderDir.splice(fieldIndex, 1);
            }

            if (currentOrderBy.length >= maxSortColumns) {
                currentOrderBy.pop();
                currentOrderDir.pop();
            }

            currentOrderBy.unshift(fieldName);
            currentOrderDir.unshift(newDirection);

            urlParams.set('order_by', currentOrderBy.join(','));
            urlParams.set('order_dir', currentOrderDir.join(','));
            window.location.search = urlParams.toString();
        });
    });
});
