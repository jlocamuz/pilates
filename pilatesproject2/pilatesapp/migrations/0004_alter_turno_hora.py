# Generated by Django 5.1.1 on 2024-10-01 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pilatesapp', '0003_remove_turno_fecha_turno_dia_turno_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='hora',
            field=models.CharField(choices=[('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'), ('21:00', '21:00')], default='17:00', max_length=5),
        ),
    ]
