from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get model
    NameGroup = apps.get_model("auth", "Group")
    if NameGroup.objects.all():
        NameGroup.objects.all().delete()
    # Create model's objects
    NameGroup.objects.create(
        name="admin",
    )
    NameGroup.objects.create(
        name="user",
    )


def reverse_func(apps, schema_editor):
    # Get model
    NameGroup = apps.get_model("auth", "Group")
    # Delete objects
    NameGroup.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
