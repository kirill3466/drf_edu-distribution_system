from django.contrib import admin

from .models import Access, Group, Lesson, Product

admin.site.register(Product)
admin.site.register(Group)
admin.site.register(Lesson)
admin.site.register(Access)
