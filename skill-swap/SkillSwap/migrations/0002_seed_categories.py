from django.db import migrations


CATEGORIES = [
    ('Programming', 'programming'),
    ('Design', 'design'),
    ('Languages', 'languages'),
    ('Marketing', 'marketing'),
    ('Music', 'music'),
    ('Photography', 'photography'),
    ('Business', 'business'),
    ('Mathematics', 'mathematics'),
    ('Other', 'other'),
]


def add_categories(apps, schema_editor):
    Category = apps.get_model('SkillSwap', 'Category')
    for name, slug in CATEGORIES:
        Category.objects.get_or_create(
            name=name,
            defaults={'slug': slug},
        )


class Migration(migrations.Migration):
    dependencies = [
        ('SkillSwap', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_categories, migrations.RunPython.noop),
    ]
