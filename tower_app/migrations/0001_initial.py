# Generated by Django 3.0 on 2020-01-09 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=64)),
                ('strength', models.IntegerField(default=5)),
                ('item_type', models.CharField(default='weapon', max_length=64)),
                ('playerID', models.IntegerField(blank=True, null=True)),
                ('roomID', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=64)),
                ('description', models.CharField(default="No Room description'", max_length=500)),
                ('up', models.CharField(default='', max_length=64)),
                ('down', models.CharField(default='', max_length=64)),
                ('left', models.CharField(default='', max_length=64)),
                ('right', models.CharField(default='', max_length=64)),
                ('floor', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hp', models.IntegerField(default=10)),
                ('name', models.CharField(default='Room n', max_length=64)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tower_app.Room')),
            ],
        ),
    ]
