# Generated by Django 2.2.12 on 2020-07-29 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("registration", "0001_initial"),
        ("user", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Registration",
            fields=[],
            options={
                "ordering": ("date_joined",),
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("user.user",),
        ),
        migrations.AddField(
            model_name="registrationformsubmission",
            name="page",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="wagtailcore.Page"
            ),
        ),
        migrations.AddField(
            model_name="registrationformsubmission",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]