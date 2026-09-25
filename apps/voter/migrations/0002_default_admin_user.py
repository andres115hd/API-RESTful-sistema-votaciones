from django.conf import settings
from django.db import migrations


def create_default_admin(apps, schema_editor):
    from django.contrib.auth.hashers import make_password

    User = apps.get_model("auth", "User")
    User.objects.update_or_create(
        username="admin",
        defaults={
            "email": "admin@gmail.com",
            "password": make_password("administrator1"),
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )


def remove_default_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="admin", email="admin@gmail.com").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("voter", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_default_admin, remove_default_admin),
    ]
