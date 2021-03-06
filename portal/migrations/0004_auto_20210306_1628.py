# Generated by Django 3.1.7 on 2021-03-06 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(max_length=1000)),
                ('question', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('chosen_option', models.CharField(max_length=1)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.poll')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.profile')),
            ],
        ),
        migrations.AddField(
            model_name='poll',
            name='people',
            field=models.ManyToManyField(through='portal.Vote', to='portal.Profile'),
        ),
    ]
