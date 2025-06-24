from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import pandas as pd
from unfold.admin import ModelAdmin
from .models import Product
from .manufacturing_queue import ManufacturingQueueItem
from .product_history import ProductHistory

admin.site.site_header = "Global Snus CRM"
admin.site.site_title = "Global Snus CRM"
admin.site.index_title = "Global Snus CRM"

class ProductAdmin(ModelAdmin):
    list_display = (
        'name_en', 'code', 'thumbnail_preview', 'supplier',
        'price', 'active', 'created_at',
    )
    list_filter = ('active', 'supplier', 'category', 'manufacturer')
    search_fields = ('name_en', 'code', 'supplier', 'manufacturer')
    change_list_template = "admin/product_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import/', self.import_products, name='product-import'),
        ]
        return custom_urls + urls

    def import_products(self, request):
        if request.method == 'POST' and request.FILES.get('import_file'):
            file = request.FILES['import_file']
            ext = file.name.split('.')[-1].lower()

            if file.size > 5 * 1024 * 1024:
                messages.error(request, "File size exceeds 5MB limit.")
                return redirect('..')

            allowed_extensions = ['xls', 'xlsx', 'csv']
            if ext not in allowed_extensions:
                messages.error(request, "Unsupported file format. Allowed formats: xls, xlsx, csv.")
                return redirect('..')

            fs = FileSystemStorage()
            saved_file = fs.save(file.name, file)
            file_path = fs.path(saved_file)

            try:
                if ext in ['xls', 'xlsx']:
                    df = pd.read_excel(file_path)
                elif ext == 'csv':
                    df = pd.read_csv(file_path)
            except Exception as e:
                messages.error(request, f"Error reading file: {e}")
                return redirect('..')

            created, updated = 0, 0
            skipped_rows = []

            for index, row in df.iterrows():
                name_en = row.get('Item title (EN)')
                code = str(row.get('Code') or row.get('Supplier code') or '').strip()

                if not name_en or pd.isna(name_en):
                    skipped_rows.append(index + 2)
                    continue

                if not code:
                    code = f"SKU-{str(index).zfill(5)}"

                product, is_created = Product.objects.update_or_create(
                    code=code,
                    defaults={
                        'name_en': name_en,
                        'image_url': row.get('Image'),
                        'description_en': row.get('Description (EN)'),
                        'supplier': row.get('Supplier'),
                        'supplier_code': row.get('Supplier code'),
                        'price': row.get('Price'),
                        'cost': row.get('Prime cost'),
                        'vat': row.get('VAT'),
                        'weight': row.get('Weight, kg'),
                        'manufacturer': row.get('Manufacturer'),
                        'pouch_tip': row.get('pouch_tip'),
                        'pouch_length': row.get('pouch_length'),
                        'unit': row.get('Unit'),
                        'category': row.get('Category title'),
                        'active': str(row.get('Active')).lower() in ['yes', 'true', '1'],
                    }
                )

                if is_created:
                    created += 1
                else:
                    updated += 1

            if skipped_rows:
                messages.warning(request, f"⚠️ Skipped {len(skipped_rows)} row(s): {skipped_rows}")

            messages.success(request, f"✅ {created} product(s) created, {updated} updated.")
            return redirect('..')

        return redirect('..')

    def thumbnail_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover;" />',
                obj.image_url
            )
        elif obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    thumbnail_preview.short_description = 'Image'

class ProductHistoryAdmin(ModelAdmin):
    list_display = ('product', 'product_thumbnail', 'change_type', 'lot_number', 'production_date', 'quantity_produced', 'changed_at')
    list_filter = ('change_type', 'changed_by', 'changed_at', 'production_date')
    search_fields = ('product__code', 'product__name_en', 'lot_number')
    readonly_fields = (
        'product', 'change_type', 'changed_by', 'snapshot', 'changed_at',
        'manufacturing_queue_item', 'lot_number', 'production_date', 'quantity_produced'
    )

    def product_thumbnail(self, obj):
        if obj.product.image_url:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover;" />',
                obj.product.image_url
            )
        elif obj.product.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover;" />',
                obj.product.image.url
            )
        return "-"
    product_thumbnail.short_description = 'Product Image'

    def get_queryset(self, request):
        # Show most recent entries first
        return super().get_queryset(request).order_by('-changed_at')

class ManufacturingQueueAdmin(ModelAdmin):  # Using ModelAdmin directly
    list_display = ('product', 'product_thumbnail', 'status', 'strength', 'pouch_quantity', 'order_quantity', 'created_at')
    list_filter = ('status', 'product__supplier', 'product__category')
    search_fields = ('product__name_en', 'product__code', 'lot_number')

    def product_thumbnail(self, obj):
        if obj.product.image_url:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover;" />',
                obj.product.image_url
            )
        elif obj.product.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover;" />',
                obj.product.image.url
            )
        return "-"
    product_thumbnail.short_description = 'Product Image'

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductHistory, ProductHistoryAdmin)
admin.site.register(ManufacturingQueueItem, ManufacturingQueueAdmin)
