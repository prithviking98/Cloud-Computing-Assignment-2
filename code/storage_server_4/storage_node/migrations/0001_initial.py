# Generated by Django 2.0 on 2019-11-01 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClockStamps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.IntegerField()),
                ('time_stamp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HandedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_key', models.CharField(max_length=100)),
                ('data_value', models.CharField(max_length=100)),
                ('vector_clock', models.CharField(max_length=200)),
                ('original_node_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RealData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_key', models.CharField(max_length=100)),
                ('data_value', models.CharField(max_length=100)),
                ('vector_clock', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SelfID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StorageServers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.IntegerField()),
                ('server_port', models.IntegerField()),
            ],
        ),
    ]
