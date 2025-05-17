from django.db import migrations


def forwards_func(apps, schema_editor):
    # Get model
    DataUser = apps.get_model("users", "User")
    # Create model's objects
    DataUser.objects.create(
        username="admin@admin.com",
        email="admin@admin.com",
        password="pbkdf2_sha256$1000000$4TqZG30ajAgJRq0M5J5uJA$CTFmHcSlQU5nAR5H6uNQh1obVPHDRRlef/dtDFxyLVo=",  # 1234
        is_superuser=True,
        is_staff=True,
        is_active=True,
    )


def reverse_func(apps, schema_editor):
    pass
    # Get model
    DataUser = apps.get_model("users", "User")
    # Delete objects
    if DataUser.objects.filter(username="admin@admin.com"):
        DataUser.objects.get(username="admin@admin.com").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_data_group_migration"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
