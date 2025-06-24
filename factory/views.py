import pandas as pd
from .product_history import ProductHistory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Product
from .manufacturing_queue import ManufacturingQueueItem  # Correct import

def product_upload(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        file = request.FILES['import_file']
        ext = file.name.split('.')[-1].lower()

        # Validate file size (max 5MB)
        if file.size > 5 * 1024 * 1024:
            messages.error(request, "File size exceeds 5MB limit.")
            return redirect('product-upload')

        # Validate file extension
        allowed_extensions = ['xls', 'xlsx', 'csv']
        if ext not in allowed_extensions:
            messages.error(request, "Unsupported file format. Allowed formats: xls, xlsx, csv.")
            return redirect('product-upload')

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
            return redirect('product-upload')

        created, updated = 0, 0
        skipped_rows = []

        for index, row in df.iterrows():
            name_en = row.get('Item title (EN)')
            code = str(row.get('Code') or row.get('Supplier code') or '').strip()

            if not name_en or pd.isna(name_en):
                skipped_rows.append(index + 2)  # +2 accounts for header and zero index
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
            import json
            snapshot_data = {
                'name_en': product.name_en,
                'image_url': product.image_url,
                'supplier': product.supplier,
                'price': str(product.price),
                'active': product.active,
            }
            # Ensure snapshot is valid JSON string
            snapshot_json = json.dumps(snapshot_data)
            ProductHistory.objects.create(
                product=product,
                changed_by=request.user if request.user.is_authenticated else None,
                change_type='created' if is_created else 'updated',
                snapshot=snapshot_json
            )


            if is_created:
                created += 1
            else:
                updated += 1

        if skipped_rows:
            messages.warning(request, f"⚠️ Skipped {len(skipped_rows)} row(s): {skipped_rows}")

        messages.success(request, f"✅ {created} product(s) created, {updated} updated.")
        return redirect('product-upload')

    return render(request, 'factory/product_upload.html')


def live_manufacturing_display(request):
    try:
        queue_items = ManufacturingQueueItem.objects.filter(
            status__in=['queued', 'in_progress']
        ).order_by('created_at')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f"Error loading manufacturing queue: {e}")
        queue_items = []

    return render(request, 'factory/live_display.html', {'queue_items': queue_items})
