from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=255)
    manufacturer_name = models.CharField(max_length=255)
    product_qunatity = models.IntegerField()
    product_expiry = models.DateField()
    product_price = models.IntegerField()
   
    
class customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=255)
    customer_phonenumber = models.CharField(max_length=10) 
    
class employee(models.Model):
    jobs = (
        ('A', 'Admin'),
        ('R', 'Receptionist'),
    )
    employee_id = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_address = models.CharField(max_length=255,blank=True)
    employee_phonenumber = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')],blank=True)
    employee_role = models.CharField(max_length=1, choices=jobs,blank=True)

class transction(models.Model):
    transction_id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(product,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_sum = models.IntegerField()
    customer_id = models.ForeignKey(customer,on_delete=models.CASCADE,null=True)
    employee_id = models.ForeignKey(employee,on_delete=models.CASCADE,null=True)
