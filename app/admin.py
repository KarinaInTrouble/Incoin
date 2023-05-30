from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Task)
admin.site.register(Urgency)
