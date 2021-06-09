from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Provider)
admin.site.register(Dealer)
admin.site.register(Category)
admin.site.register(Code)
admin.site.register(Number)
admin.site.register(Client)

