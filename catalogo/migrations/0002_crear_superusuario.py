from django.db import migrations
from django.contrib.auth.hashers import make_password


def crear_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")
    if not User.objects.filter(username="admin").exists():
        User.objects.create(
            username="admin",
            email="admin@ferreteria.cl",
            password=make_password("admin123"),
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )


def eliminar_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="admin", is_superuser=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalogo", "0001_initial"),
        ("auth", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(crear_superuser, eliminar_superuser),
    ]
