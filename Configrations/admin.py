from django.contrib import admin

from .models import  models_to_be_registerd_in_admin_pannel

[admin.site.register(_) for _ in models_to_be_registerd_in_admin_pannel]