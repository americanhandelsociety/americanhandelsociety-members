# Generated by Django 4.0 on 2022-08-26 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("americanhandelsociety_app", "0004_track_member_profile_updates"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="last_updated",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
