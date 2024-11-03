from setuptools import setup, find_packages

setup(
    name="django_sortable_tabular",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=3.2",
    ],
    description="A Django library for sortable TabularInline in admin interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/michalkonwiak/django_sortable_tabular",
    author="Michał Konwiak",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)
