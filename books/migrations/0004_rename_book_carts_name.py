# Generated by Django 4.1.2 on 2022-11-24 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_rename_book_name_carts_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carts',
            old_name='book',
            new_name='name',
        ),
    ]