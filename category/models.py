from django.db import models
from django.utils import timezone

# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=255,blank=True)
    cart_image = models.ImageField(upload_to='photos/categories',blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:  
            self.created_at = timezone.now()
        super(category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
       return self.category_name 
