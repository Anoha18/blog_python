# Generated by Django 3.1.5 on 2021-02-21 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('main', '0004_post_views_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_views',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sessions.session'),
        ),
    ]
