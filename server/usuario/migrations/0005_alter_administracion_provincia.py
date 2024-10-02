# Generated by Django 5.1.1 on 2024-10-01 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0004_alter_administracion_provincia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administracion',
            name='provincia',
            field=models.CharField(choices=[('ALAVA', 'ALAVA/ARABA'), ('ALBACETE', 'ALBACETE'), ('ALICANTE', 'ALICANTE/ALACANT'), ('ALMERIA', 'ALMERIA'), ('ASTURIAS', 'ASTURIAS'), ('AVILA', 'AVILA'), ('BADAJOZ', 'BADAJOZ'), ('BALEARES', 'BALEARES'), ('BARCELONA', 'BARCELONA'), ('VIZCAYA', 'BIZKAIA/VIZCAYA'), ('BURGOS', 'BURGOS'), ('CACERES', 'CACERES'), ('CADIZ', 'CADIZ'), ('CANTABRIA', 'CANTABRIA'), ('CASTELLON', 'CASTELLON/CASTELLÓ'), ('CEUTA', 'CEUTA'), ('CIUDAD_REAL', 'CIUDAD REAL'), ('CORDOBA', 'CORDOBA'), ('CORUÑA', 'CORUÑA (A)'), ('CUENCA', 'CUENCA'), ('GUIPUZCOA', 'GIPUZKOA'), ('GIRONA', 'GIRONA'), ('GRANADA', 'GRANADA'), ('GUADALAJARA', 'GUADALAJARA'), ('HUELVA', 'HUELVA'), ('HUESCA', 'HUESCA'), ('JAEN', 'JAEN'), ('LEON', 'LEON'), ('LLEIDA', 'LLEIDA'), ('LUGO', 'LUGO'), ('MADRID', 'MADRID'), ('MALAGA', 'MALAGA'), ('MELILLA', 'MELILLA'), ('MURCIA', 'MURCIA'), ('NAVARRA', 'NAVARRA'), ('OURENSE', 'OURENSE'), ('PALENCIA', 'PALENCIA'), ('LAS_PALMAS', 'LAS PALMAS'), ('PONTEVEDRA', 'PONTEVEDRA'), ('LA_RIOJA', 'LA RIOJA'), ('SALAMANCA', 'SALAMANCA'), ('SEGOVIA', 'SEGOVIA'), ('SEVILLA', 'SEVILLA'), ('SORIA', 'SORIA'), ('SANTA_CRUZ_DE_TENERIFE', 'SANTA CRUZ DE TENERIFE'), ('TARRAGONA', 'TARRAGONA'), ('TERUEL', 'TERUEL'), ('TOLEDO', 'TOLEDO'), ('VALENCIA', 'VALENCIA/VALÈNCIA'), ('VALLADOLID', 'VALLADOLID'), ('ZAMORA', 'ZAMORA'), ('ZARAGOZA', 'ZARAGOZA')], max_length=100),
        ),
    ]
