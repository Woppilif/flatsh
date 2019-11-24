from django.contrib import admin

# Register your models here.
from .models import *
from api.views import openDoorAPI

def open_door(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.id,"open",i.app_id)

open_door.short_description = "Open door"

def update_softare(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.id,"update",i.app_id)

update_softare.short_description = "Update software"

def get_log(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        openDoorAPI(i.id,"sendlog",i.app_id)
get_log.short_description = "Get log"

class ChoiceInline(admin.StackedInline):
    model = Images
    extra = 2

class PaymentsInline(admin.StackedInline):
    model = Payments
    extra = 0

class AccessInline(admin.StackedInline):
    model = Access
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('street','district','city','status','app_status')
    list_filter = ['district']
    search_fields = ['street']
    actions = [update_softare,open_door,get_log]

class RentsExtend(admin.ModelAdmin):
    inlines = [PaymentsInline,AccessInline]
    list_display = ('flat','start','end','status')
    list_filter = ['start','end']
    #search_fields = ['street']

class PaymentsAdmin(admin.ModelAdmin):
    
    list_display = ('rentor','renta','price','status')
    list_filter = ['status']

admin.site.register(Flats, QuestionAdmin)
admin.site.register(Countries)
admin.site.register(Cities)
admin.site.register(Districts)
admin.site.register(Images)
admin.site.register(Workers)
admin.site.register(Partners)
admin.site.register(Payments)
admin.site.register(Rents,RentsExtend)
admin.site.register(Access)
admin.site.register(UsersDocuments)
admin.site.register(SystemLogs)