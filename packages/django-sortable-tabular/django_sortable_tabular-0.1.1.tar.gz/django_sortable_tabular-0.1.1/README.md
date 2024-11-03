# django_sortable_tabular

`django_sortable_tabular` is a simple and lightweight Django library that enables column sorting for fields displayed in `TabularInline` in the Django admin panel.

## Author

Michał Konwiak
[GitHub](https://github.com/michalkonwiak).

## Features

- Column sorting for `TabularInline` using JavaScript and Django.
- Multi-column sorting with adjustable sort direction (ascending/descending).
- Seamless integration with the Django admin interface through the `SortableTabularInline` class.

## Requirements

- Python 3.8+
- Django 3.2+

## Installation

1. Install the library using `pip`:

   ```bash
   pip install django_sortable_tabular
2. Add a package to INSTALLED_APPS section. 
   ```bash
   INSTALLED_APPS = [
       # another apps
       'django_sortable_tabular',
   ]
3. Define a class that extends the `SortableTabularInline` class and use it as you would a standard inline class. Here’s an example:
   ```bash
   class CommentAdmin(SortableTabularInline):
    model = Comment

   class PostAdmin(admin.ModelAdmin):
       list_display = (
           "title",
           "text",
           "picture",
           "author"
       )
       inlines = [
           CommentAdmin
       ]

4. Run `python manage.py collectstatic`
5. Run server and enjoy
