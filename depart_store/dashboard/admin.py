from django.contrib import admin
from .models import customer , employee , product , transction

# Register your models here.
admin.site.register(customer)
admin.site.register(employee)
admin.site.register(product)
admin.site.register(transction)