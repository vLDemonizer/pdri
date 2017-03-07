from django.contrib import admin
from .models import Project, CD, RatingElement, UserProfile

admin.site.register(Project)
admin.site.register(CD)
admin.site.register(RatingElement)
admin.site.register(UserProfile)

# Register your models here.
