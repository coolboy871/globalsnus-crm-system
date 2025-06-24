from django.db import models
from django.conf import settings

class ProductHistory(models.Model):
    CHANGE_TYPE_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('manufacturing_completed', 'Manufacturing Completed'),
    ]
    
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    change_type = models.CharField(max_length=30, choices=CHANGE_TYPE_CHOICES)
    snapshot = models.JSONField()
    
    # Manufacturing completion specific fields
    manufacturing_queue_item = models.ForeignKey(
        'ManufacturingQueueItem', null=True, blank=True, on_delete=models.SET_NULL
    )
    lot_number = models.CharField(max_length=100, blank=True, null=True)
    production_date = models.DateField(blank=True, null=True)
    quantity_produced = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'Product History'
        verbose_name_plural = 'Product Histories'

    def __str__(self):
        return f"{self.change_type.title()} – {self.product.code} – {self.changed_at.strftime('%Y-%m-%d %H:%M')}"
