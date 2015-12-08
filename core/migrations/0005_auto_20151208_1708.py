# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151208_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='comment',
            field=models.ForeignKey(blank=True, to='core.Comment', null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='review',
            field=models.ForeignKey(blank=True, to='core.Review', null=True),
        ),
    ]
