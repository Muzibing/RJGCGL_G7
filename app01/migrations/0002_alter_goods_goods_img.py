# Generated by Django 5.0.6 on 2024-11-25 11:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goods",
            name="goods_img",
            field=models.CharField(max_length=256, verbose_name="图片链接"),
        ),
    ]
