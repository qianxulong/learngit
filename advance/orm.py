import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advance.settings")
    import django
    django.setup()

    from app01 import models

    objs =[models.Book(name = '和我学python{}'.format(i)) for i in range(1500)]
    models.Book.objects.bulk_create(objs, 10)