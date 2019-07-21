from django.contrib import admin

# Register your models here.
#from .models import Docname
#admin.site.register(Docname)

from .models import Docname, Taskname

admin.site.site_header = 'Shmaperalloy account access'

class DocnameAdmin(admin.ModelAdmin):
    list_display = ('doc_name', 'doc_creator', 'input_date')
    list_filter = ('doc_creator', 'input_date')

##IS THIS SAVE FUNCTION NECESSARY WHEN WE ARE SAVING IN THE VIEWS.PY FILE??
    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance, 'doc_creator'):
            instance.doc_creator = request.user
#        instance.edit_contributor = request.user
        if not instance.doc_owner.filter(owner=instance.doc_creator).exists():
            instance.owner.add(instance.doc_creator)

        instance.save()
        ##CANNOT SAVE MANY-TO-MANY FORM DATA WHEN COMMIT=FALSE UNTIL THE INSTANCE IS SAVED IN THE DATABASE
        form.save_m2m()
        return instance

    def save_formset(self, request, form, formset, change):

        def set_user(instance):
            if not instance.doc_creator:
                instance.doc_creator = request.user
#            instance.edit_contributor = request.user
            instance.save()

        if formset.model == Docname:
            instances = formset.save(commit=False)
            map(set_user, instances)
            formset.save_m2m()
            return instances
        else:
            return formset.save()

admin.site.register(Docname, DocnameAdmin)
