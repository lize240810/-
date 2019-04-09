# Generated by Django 2.0.2 on 2019-04-09 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='goods_num',
            field=models.IntegerField(default=0, verbose_name='商品数量'),
        ),
        migrations.AddField(
            model_name='goods',
            name='market_price',
            field=models.FloatField(default=0.0, verbose_name='市场价格'),
        ),
    ]