from django.contrib import admin
from kb.models import App, Departament, UserManual, Document, Instruction, KbUserManualName

class UserManualAdmin(admin.ModelAdmin):
    pass

# admin.site.register(KbCollection, admin.ModelAdmin)
admin.site.register(App, admin.ModelAdmin)
admin.site.register(Departament, admin.ModelAdmin)
admin.site.register(UserManual, UserManualAdmin)
admin.site.register(Document, admin.ModelAdmin)
admin.site.register(Instruction, admin.ModelAdmin)
admin.site.register(KbUserManualName, admin.ModelAdmin)
