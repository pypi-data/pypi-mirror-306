from django.contrib import admin
from django.templatetags.static import static


class SortableTabularInline(admin.TabularInline):
    def get_ordering(self, request):
        order_by_fields = request.GET.get('order_by', '').split(',')
        order_directions = request.GET.get('order_dir', '').split(',')

        fields = [f.name for f in self.model._meta.get_fields()]
        ordering = []

        for i, field in enumerate(order_by_fields):
            if field in fields:
                direction = order_directions[i] if i < len(order_directions) else 'asc'
                ordering.append(f'-{field}' if direction == 'desc' else field)

        return ordering if ordering else [fields[0]]

    class Media:
        js = [static("django_sortable_tabular/sortable_tabular.js")]
