from django.db import models

# Create your models here.
class Banner(models.Model):
    title=models.CharField(max_length=10)
    status=models.SmallIntegerField()
    pic=models.ImageField(upload_to='pics')
    create_time=models.DateTimeField(auto_now_add=True)
