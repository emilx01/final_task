from django.db import models

class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField(default=dict)
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} - {self.status}"

class ImagesArtifact(models.Model):
    request_log = models.ForeignKey(
        RequestLog, 
        on_delete=models.CASCADE, 
        related_name="artifacts"
    )
    filename = models.CharField(max_length=255)
    
    TYPE_CHOICES = [
        ('INPUT', 'Input Image'),
        ('OUTPUT', 'Processed Output'),
    ]
    
    artifact_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_image = models.ImageField(upload_to="uploaded/")
    processed_image = models.ImageField(upload_to="processed/")

    def __str__(self):
        return f"{self.filename} ({self.artifact_type})"
    