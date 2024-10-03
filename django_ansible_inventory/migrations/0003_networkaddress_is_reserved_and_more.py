# Generated by Django 5.1.1 on 2024-09-24 17:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_ansible_inventory", "0002_alter_networklabel_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="networkaddress",
            name="is_reserved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="networkaddress",
            name="reservation_timestamp",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="networkaddress",
            name="reserved_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
