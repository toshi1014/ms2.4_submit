# Generated by Django 3.0.7 on 2020-07-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_mypage_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypage',
            name='fav_class',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='mypage',
            name='like',
            field=models.TextField(null=True),
        ),
    ]