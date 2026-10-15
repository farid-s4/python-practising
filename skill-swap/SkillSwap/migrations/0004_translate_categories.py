from django.db import migrations


CATEGORY_NAMES = [
    ('Programming', 'Программирование'),
    ('Design', 'Дизайн'),
    ('Languages', 'Языки'),
    ('Marketing', 'Маркетинг'),
    ('Music', 'Музыка'),
    ('Photography', 'Фотография'),
    ('Business', 'Бизнес'),
    ('Mathematics', 'Математика'),
    ('Other', 'Другое'),
]


def translate_categories(apps, schema_editor):
    Category = apps.get_model('SkillSwap', 'Category')
    for english_name, russian_name in CATEGORY_NAMES:
        Category.objects.filter(name=english_name).update(name=russian_name)


def restore_categories(apps, schema_editor):
    Category = apps.get_model('SkillSwap', 'Category')
    for english_name, russian_name in CATEGORY_NAMES:
        Category.objects.filter(name=russian_name).update(name=english_name)


class Migration(migrations.Migration):
    dependencies = [
        ('SkillSwap', '0003_favorites'),
    ]

    operations = [
        migrations.RunPython(translate_categories, restore_categories),
    ]
