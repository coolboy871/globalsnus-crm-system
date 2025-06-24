from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

class Product(models.Model):
    code = models.CharField(_('Code'), max_length=50, blank=True, null=True)
    supplier = models.CharField(_('Supplier'), max_length=100, blank=True, null=True)
    supplier_code = models.CharField(_('Supplier Code'), max_length=50, blank=True, null=True)

    name_en = models.CharField(_('Item Title (EN)'), max_length=200)
    name_lt = models.CharField(_('Item Title (LT)'), max_length=200, blank=True, null=True)
    description_en = models.TextField(_('Description (EN)'), blank=True, null=True)
    description_lt = models.TextField(_('Description (LT)'), blank=True, null=True)

    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=5, blank=True, null=True)
    cost = models.DecimalField(_('Prime Cost'), max_digits=10, decimal_places=5, blank=True, null=True)
    vat = models.DecimalField(_('VAT'), max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(_('Weight (kg)'), max_digits=6, decimal_places=3, blank=True, null=True)
    pouch_length = models.PositiveIntegerField(_('Pouch Length (mm)'), blank=True, null=True)

    manufacturer = models.CharField(_('Manufacturer'), max_length=100, blank=True, null=True)
    unit = models.CharField(_('Unit'), max_length=50, blank=True, null=True)
    category = models.CharField(_('Category'), max_length=100, blank=True, null=True)

    image = models.ImageField(_('Product Image'), upload_to='product_images/', blank=True, null=True)
    image_url = models.URLField(_('Product Image URL'), blank=True, null=True)

    active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    pouch_tip = models.CharField(_('Pouch Tip'), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name_en or f"{self.code or 'Unnamed Product'}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.price is not None and self.price < 0:
            raise ValidationError({'price': 'Price cannot be negative.'})
        if self.cost is not None and self.cost < 0:
            raise ValidationError({'cost': 'Cost cannot be negative.'})
        if self.vat is not None and (self.vat < 0 or self.vat > 100):
            raise ValidationError({'vat': 'VAT must be between 0 and 100.'})
        if self.weight is not None and self.weight < 0:
            raise ValidationError({'weight': 'Weight cannot be negative.'})
        if self.pouch_length is not None and self.pouch_length < 0:
            raise ValidationError({'pouch_length': 'Pouch length cannot be negative.'})
