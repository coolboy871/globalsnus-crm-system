from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from factory.models import Product
from .product_history import ProductHistory

class ManufacturingQueueItem(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')

    # Production-specific details (manually entered)
    strength = models.PositiveIntegerField(blank=True, null=True)
    pouch_quantity = models.PositiveIntegerField(blank=True, null=True)
    spray_function = models.BooleanField(default=False)
    production_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    lot_number = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    box_color = models.CharField(max_length=100, blank=True, null=True)
    lid_color = models.CharField(max_length=100, blank=True, null=True)
    order_quantity = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name_en} – {self.get_status_display()}"


from django.db.models.signals import post_save

@receiver(post_save, sender=ManufacturingQueueItem)
def handle_completion(sender, instance, created, **kwargs):
    """Handle manufacturing item completion - create history and remove from queue"""
    if not created and instance.status == 'completed':  # Only for updates to completed status
        try:
            # Check if this is a new completion (no existing history entry)
            existing_history = ProductHistory.objects.filter(
                manufacturing_queue_item=instance,
                change_type='manufacturing_completed'
            ).first()
            
            if not existing_history:
                # Create ProductHistory entry for manufacturing completion
                ProductHistory.objects.create(
                    product=instance.product,
                    change_type='manufacturing_completed',
                    manufacturing_queue_item=instance,
                    lot_number=instance.lot_number,
                    production_date=instance.production_date,
                    quantity_produced=instance.order_quantity,
                    snapshot={
                        'product_name': instance.product.name_en,
                        'product_code': instance.product.code,
                        'status': 'completed',
                        'lot_number': instance.lot_number,
                        'production_date': str(instance.production_date) if instance.production_date else None,
                        'strength': instance.strength,
                        'pouch_quantity': instance.pouch_quantity,
                        'order_quantity': instance.order_quantity,
                        'box_color': instance.box_color,
                        'lid_color': instance.lid_color,
                        'language': instance.language,
                        'spray_function': instance.spray_function,
                    }
                )
                
                # Remove the completed item from the manufacturing queue
                instance.delete()
                
        except Exception as e:
            # Log error but don't break the save process
            print(f"Error handling manufacturing completion: {e}")
