# Generated by Django 4.0.7 on 2022-10-24 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_alter_registeruser_address_alter_registeruser_city_and_more'),
        ('blog', '0002_blog_author_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.registeruser'),
        ),
    ]
