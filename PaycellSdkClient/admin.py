from django.contrib import admin
from .models import Metadata, Payment, InstallmentPlan
# Register your model here.


admin.site.register(Metadata)
admin.site.register(Payment)
admin.site.register(InstallmentPlan)
