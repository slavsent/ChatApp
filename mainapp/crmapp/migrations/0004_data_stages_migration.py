from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get model
    Stage = apps.get_model("crmapp", "Stage")
    if Stage.objects.all():
        Stage.objects.all().delete()
    # Create model's objects
    Stage.objects.create(
        name="Этап 1",
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )
    Stage.objects.create(
        name="Сделка 2",
        created="2025-05-18T18:32:47.331Z",
        last_updated="2025-05-18T18:32:47.331Z",
    )


def reverse_func(apps, schema_editor):
    # Get model
    Stage = apps.get_model("crmapp", "Stage")
    # Delete objects
    Stage.objects.all().delete()
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("crmapp", "0003_data_deals_migration"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
