from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get model
    Contact = apps.get_model("crmapp", "Contact")
    if Contact.objects.all():
        Contact.objects.all().delete()
    # Create model's objects
    Contact.objects.create(
        last_name="Контакт 1",
        email='contact1@mail.ru',
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )
    Contact.objects.create(
        last_name="Контакт 2",
        email='contact2@mail.ru',
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )
    Contact.objects.create(
        last_name="Контакт 3",
        email='contact3@mail.ru',
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )


def reverse_func(apps, schema_editor):
    # Get model
    Contact = apps.get_model("users", "Role")
    # Delete objects
    Contact.objects.all().delete()
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("crmapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
