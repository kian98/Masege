# Generated by Django 2.2.5 on 2019-09-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masege_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='studentUnion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('unionName', models.CharField(max_length=20, verbose_name='社团名称')),
                ('unionNum', models.IntegerField(default=0, verbose_name='人数')),
                ('unionRoot', models.OneToOneField(on_delete=None, to='Masege_app.Test')),
            ],
            options={
                'db_table': 'student_union',
            },
        ),
    ]