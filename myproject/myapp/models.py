from django.db import models

class SubmitData(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='new')

    def __str__(self):
        return self.name

class Pass(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    coordinates = models.CharField(max_length=100)
    height = models.FloatField()
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.EmailField(blank=True, null=True)
    user_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    models.ForeignKey(Pass, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos')

    def __str__(self):
        return f"Photo #{self.id}"