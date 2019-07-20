from django.contrib import admin

# Register your models here.
#from .models import Docname
#admin.site.register(Docname)

from .models import Docname, Taskname

admin.site.site_header = 'Shmaperalloy account access'

class DocnameAdmin(admin.ModelAdmin):
    list_display = ('doc_name', 'doc_creator', 'input_date')
    list_filter = ('doc_creator', 'input_date')

admin.site.register(Docname, DocnameAdmin)
