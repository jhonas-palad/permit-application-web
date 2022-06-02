from django.db import models
from client.models import BusinessPermitApplication as BPA
from django.contrib.auth import get_user_model

Staff = get_user_model()

class BusinessPermit(models.Model):
    
    bpa = models.OneToOneField(BPA, on_delete=models.CASCADE, primary_key=True)
    date_issued = models.DateField(auto_now_add=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    
