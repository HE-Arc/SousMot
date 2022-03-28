# Generated by Django 4.0.3 on 2022-03-24 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Dictionaries',
            },
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=20)),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sousmotapp.dictionary')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_letters', models.PositiveSmallIntegerField()),
                ('time_s', models.PositiveIntegerField()),
                ('nb_words', models.PositiveSmallIntegerField()),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sousmotapp.dictionary')),
                ('mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sousmotapp.mode')),
            ],
        ),
        migrations.CreateModel(
            name='HistorySolo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_words', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sousmotapp.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sousmotapp.user')),
            ],
            options={
                'verbose_name_plural': 'HistorySolo',
                'unique_together': {('user', 'game')},
            },
        ),
        migrations.CreateModel(
            name='GamesPerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sousmotapp.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sousmotapp.user')),
            ],
            options={
                'verbose_name_plural': 'GamesPerUser',
                'unique_together': {('user', 'game')},
            },
        ),
    ]
