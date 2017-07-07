from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    top_addons_sum = models.IntegerField(default=0)
    top_addons_total_download_sum = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Addon(models.Model):
    vendor = models.ForeignKey(Vendor)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    downloads_count = models.IntegerField()

    def __unicode__(self):
        return self.name