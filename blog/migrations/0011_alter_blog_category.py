# Generated by Django 4.1.2 on 2022-11-10 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('Entertainment', 'Entertainment'), ('Technology', 'Technology'), ('Food', 'Food'), ('Travel', 'Travel')], default='Technology', max_length=100),
        ),
    ]
