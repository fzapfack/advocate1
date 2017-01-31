from django.contrib import admin

from .models import TestModel

class TestAdmin(admin.ModelAdmin):
    list_display = ["__str__","number_labels","number_labels_correct", "created", "updated"]

admin.site.register(TestModel, TestAdmin)

# Register your models here.
