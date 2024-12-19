from django.db import models


class UserDetails(models.Model):
    username = models.CharField(max_length=100, unique=True)  
    email = models.EmailField()
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)  # student, executive, etc.

    def __str__(self):
        return self.username

    
class ComplaintDetails(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    executive_name = models.CharField(max_length=100)
    complaint_text = models.TextField()
    status = models.CharField(max_length=50, default='submitted')
    created_date = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    last_updated = models.DateTimeField(null=True, blank=True)  # Allow null if it hasn't been updated yet

    def __str__(self):
        return f"Complaint by {self.user.username} to {self.executive_name}"

