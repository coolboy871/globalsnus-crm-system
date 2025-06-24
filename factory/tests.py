from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product
from factory.manufacturing_queue import ManufacturingQueueItem
import io
import pandas as pd

class ProductUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('product-upload')

    def test_upload_valid_csv(self):
        csv_content = "Item title (EN),Code,Image,Description (EN),Supplier,Supplier code,Price,Prime cost,VAT,Weight,Manufacturer,pouch_tip,pouch_length,Unit,Category title,Active\n" \
                      "Test Product,SKU-001,,Test Description,Test Supplier,TS001,10.00,5.00,20,0.5,Test Manufacturer,Tip,100,,Category,Yes\n"
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post(self.upload_url, {'import_file': csv_file})
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.name_en, "Test Product")



    def test_upload_unsupported_file(self):
        txt_file = SimpleUploadedFile("test.txt", b"Unsupported content", content_type="text/plain")
        response = self.client.post(self.upload_url, {'import_file': txt_file})
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Unsupported file format" in str(m) for m in messages))

class ManufacturingQueueTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name_en="Queue Product")
        self.queue_item = ManufacturingQueueItem.objects.create(product=self.product, status='queued')
        self.client = Client()
        self.live_url = reverse('live-manufacturing-display')

    def test_live_manufacturing_display(self):
        response = self.client.get(self.live_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name_en)

class ProductModelTests(TestCase):
    def test_product_validation(self):
        product = Product(name_en="Test Product", price=-10)
        with self.assertRaises(Exception):
            product.full_clean()

        product.price = 10
        product.vat = 150
        with self.assertRaises(Exception):
            product.full_clean()

        product.vat = 20
        product.weight = -5
        with self.assertRaises(Exception):
            product.full_clean()

        product.weight = 1
        product.pouch_length = -10
        with self.assertRaises(Exception):
            product.full_clean()

        product.pouch_length = 10
        # Should not raise
        product.full_clean()
