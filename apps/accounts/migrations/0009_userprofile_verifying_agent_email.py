# Generated by Django 2.2.4 on 2020-02-05 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190918_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='verifying_agent_email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
