# Generated by Django 4.0 on 2023-12-24 21:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("americanhandelsociety_app", "0008_alter_member_contact_preference"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="publish_member_name_consent",
            field=models.CharField(
                choices=[
                    ("NO", "No"),
                    ("YES", "Yes"),
                    ("ANONYMOUS", "Yes, but display member name as 'Anonymous'"),
                ],
                default="NO",
                max_length=9,
            ),
        ),
    ]
