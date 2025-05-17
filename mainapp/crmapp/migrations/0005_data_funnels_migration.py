from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get model
    Funnel = apps.get_model("crmapp", "Funnel")
    if Funnel.objects.all():
        Funnel.objects.all().delete()
    # Create model's objects
    Funnel.objects.create(
        name="Воронка 1",
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )
    Funnel.objects.create(
        name="Воронка 2",
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )


def reverse_func(apps, schema_editor):
    # Get model
    Funnel = apps.get_model("crmapp", "Funnel")
    # Delete objects
    Funnel.objects.all().delete()
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("crmapp", "0004_data_stages_migration"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
