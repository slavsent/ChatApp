from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get model
    Deal = apps.get_model("crmapp", "Deal")
    if Deal.objects.all():
        Deal.objects.all().delete()
    # Create model's objects
    Deal.objects.create(
        name="Сделка 1",
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )
    Deal.objects.create(
        name="Сделка 1",
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )
    Deal.objects.create(
        name="Сделка 1",
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )


def reverse_func(apps, schema_editor):
    # Get model
    Deal = apps.get_model("crmapp", "Deal")
    # Delete objects
    Deal.objects.all().delete()
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("crmapp", "0002_data_contacts_migration"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
