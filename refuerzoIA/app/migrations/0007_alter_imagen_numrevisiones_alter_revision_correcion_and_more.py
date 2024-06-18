# Generated by Django 4.2.3 on 2023-07-14 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_revision_correcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='numRevisiones',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='revision',
            name='correcion',
            field=models.CharField(blank=True, max_length=3500, null=True),
        ),
        migrations.AlterField(
            model_name='revision',
            name='fechaAsignacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='revision',
            name='fechaRevision',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='revision',
            name='pendiente',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='revision',
            name='tipoRevision',
            field=models.BooleanField(default=0),
        ),
    ]