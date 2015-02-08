from django.contrib.gis import admin
from .models import Job, Teacher, JobType, Region

class JobAdmin(admin.GeoModelAdmin):
    list_display = ('first_name', 'last_name', 'title', 'url', 'desc', 'point', 'image', 'all_teachers')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'var_name', 'icon_url')


admin.site.register(Job, JobAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(JobType, JobTypeAdmin)
