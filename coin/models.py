__author__ = 'kolobok'

from django.db import models


class Coin(models.Model):
    name = models.CharField(u'Наименование', max_length=50)
    circulation = models.IntegerField(u'Тираж', null=True, blank=True)
    inscription = models.CharField(u'Надпись на монете', max_length=200, blank=True)
    year = models.SmallIntegerField(u'Год монеты')
    weight = models.DecimalField(u'Масса монеты', max_digits=5, decimal_places=3, null=True, blank=True)
    diameter = models.DecimalField(u'Диаметр монеты', max_digits=4, decimal_places=2, null=True, blank=True)
    thickness = models.DecimalField(u'Толщина монеты', max_digits=3, decimal_places=2, null=True, blank=True)
    metal = models.ManyToManyField('Metal', verbose_name=u'Металл', db_column='id_metal')
    edge = models.ForeignKey('Edge', verbose_name=u'Вид гурта', null=True, blank=True, db_column='id_edge')
    section = models.ForeignKey('Section', verbose_name=u'Раздел', db_column='id_section')
    mint = models.ForeignKey('Mint', verbose_name=u'Монетный двор', null=True, blank=True, db_column='id_mint')

    def __str__(self):
        return u'%s %s %s %s' % (self.name, self.year, self.inscription, self.circulation,)


class Mint(models.Model):
    name = models.CharField(u'Наименование', max_length=100)

    def __str__(self):
        return u'%s %s %s %s' % (self.name, self.year, self.inscription, self.circulation,)


class Image(models.Model):
    image = models.FileField(u'Файл изображения', upload_to='images', blank=True, null=True)
    coin = models.ForeignKey('Coin', verbose_name=u'Монета', db_column='id_coin')

    def __str__(self):
        return u'%s' % (self.image,)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = 'images/origin/coins/%d' % self.coin.year
        super(Image, self).save()


class Metal(models.Model):
    name = models.CharField(u'Наименование металла', max_length=50)

    def __str__(self):
        return u'%s' % (self.name,)


class Edge(models.Model):
    name = models.CharField(u'Вид гурта', max_length=50)

    def __str__(self):
        return u'%s' % (self.name,)


class Section(models.Model):
    name = models.CharField(u'Наименование раздела', max_length=200)
    parent_section = models.ForeignKey('Section', verbose_name=u'Корневой раздел', null=True, blank=True, db_column='id_parent_section')

    def __str__(self):
        return u'%s' % (self.name,)