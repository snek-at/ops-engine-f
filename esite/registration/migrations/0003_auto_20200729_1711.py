# Generated by Django 2.2.12 on 2020-07-29 15:11

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("utils", "0001_initial"),
        ("registration", "0002_auto_20200729_1711"),
    ]

    operations = [
        migrations.AddField(
            model_name="registrationformpage",
            name="registration_button",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="utils.Button",
            ),
        ),
        migrations.AddField(
            model_name="formfield",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="form_fields",
                to="registration.RegistrationFormPage",
            ),
        ),
    ]
