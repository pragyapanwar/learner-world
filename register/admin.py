from django.db import models
from .models import Profile,subject,subcategory,resource
from django.contrib import admin


# Register your models here.
admin.site.register(Profile)
#admin.site.register(Managers)
admin.site.register(subject)
admin.site.register(subcategory)
admin.site.register(resource)
