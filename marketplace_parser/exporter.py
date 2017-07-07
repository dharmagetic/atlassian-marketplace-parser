# -*- coding: utf-8 -*-
import csv

from django.db.models import Sum

from marketplace_parser.models import Vendor, Addon


def group_top_addons_vendors():
    vendors = Vendor.objects.all()
    top_addons = Addon.objects.order_by('-downloads_count')[:500]
    target_vendors_ids = []
    for v in vendors:
        top_vendors_addons_ids = set(v.addon_set.all().values_list('id', flat=True)).intersection(set(top_addons.values_list('id', flat=True)))
        if len(top_vendors_addons_ids) > 0:
            v.top_addons_sum = len(top_vendors_addons_ids)
            addons_total_download_sum = Addon.objects.filter(id__in=top_vendors_addons_ids).aggregate(Sum('downloads_count')).get('downloads_count__sum', 0)
            v.top_addons_total_download_sum = addons_total_download_sum
            v.save()
            target_vendors_ids.append(v.id)
    return Vendor.objects.filter(id__in=target_vendors_ids).order_by('-top_addons_total_download_sum').values()


def export_to_csv():
    vendors_values = group_top_addons_vendors()
    with open('top_vendors.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for vendor_values in vendors_values:
            row = [vendor_values['name'], vendor_values['top_addons_sum'], vendor_values['top_addons_total_download_sum']]
            writer.writerow([unicode(s).encode("utf-8") for s in row])
