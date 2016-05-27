# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models, migrations
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Region
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import DataSource


class Migration(migrations.Migration):

    def insert_regions(apps, schema_editor):
        Region = apps.get_model('jobs', 'Region')

        ds = DataSource(os.path.dirname(os.path.realpath(__file__)) + '/world.geojson')
        layer = ds[0]
        geom = layer.get_geoms(geos=True)[0]
        the_geom = GEOSGeometry(geom.wkt, srid=4326)
        the_geog = GEOSGeometry(geom.wkt)
        the_geom_webmercator = the_geom.transform(ct=3857, clone=True)
        region = Region.objects.create(name="The World", description="Worldwide export region",
                        the_geom=the_geom, the_geog=the_geog, the_geom_webmercator=the_geom_webmercator
        )
        ds = None

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_regions),
    ]
