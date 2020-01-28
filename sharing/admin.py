from django.contrib import admin

# Register your models here.
from .models import *
from .views import opener
from rents.modules import bitx
from django.contrib import messages
def deletelog(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        opener.openDoorAPI(i.id,"deletelog",i.secret_key)

deletelog.short_description = "Clear log"

def open_door(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        opener.openDoorAPI(i.id,"open",i.secret_key)

open_door.short_description = "Open door"

def update_softare_new(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        opener.openDoorAPI(i.id,"updatenew",i.secret_key)
update_softare_new.short_description = "Update software [NEW]"

def update_softare(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        opener.openDoorAPI(i.id,"update",i.secret_key)

update_softare.short_description = "Update software [OLD]"

def get_log(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        opener.openDoorAPI(i.id,"sendlog",i.secret_key)
get_log.short_description = "Get log"

def get_ping(modeladmin, request, queryset):
    #queryset.update(status='p')
    for i in queryset:
        opener.openDoorAPI(i.id,"ping",i.secret_key)
get_ping.short_description = "Send ping"

def update_data(modeladmin, request, queryset):
    #queryset.update(status='p')
    soap = bitx.Soap()
    r = False
    for i in queryset:
        data = soap.getByInternalId(i.internal_id)
        for x in data:
            r = soap.parse_data(x)
        if r is True:
            messages.add_message(request,messages.INFO,"{0} успешно обновлена".format(i))
update_data.short_description = "Обновить данные у выбранных квартир"

class ChoiceInline(admin.StackedInline):
    model = Images
    extra = 2

class ChoiceInlineItems(admin.StackedInline):
    model = FlatsItems
    extra = 2

class PaymentsInline(admin.StackedInline):
    model = Payments
    extra = 0

class AccessInline(admin.StackedInline):
    model = Access
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline,ChoiceInlineItems]
    list_display = ('street','district','city','status')
    list_filter = ['district']
    search_fields = ['street']
    actions = [update_data]

class DeviceManager(admin.ModelAdmin):
    #inlines = [ChoiceInline,ChoiceInlineItems]
    list_display = ('flatId','status','description','created_at')
    list_filter = ['created_at']
    search_fields = ['created_at','description','status']
    actions = [update_softare_new,update_softare,open_door,get_log,get_ping,deletelog]

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
admin.site.register(Devices, DeviceManager)
admin.site.register(Partners)
admin.site.register(Payments)
admin.site.register(Rents,RentsExtend)
admin.site.register(Access)
admin.site.register(UsersDocuments)
admin.site.register(SystemLogs)
admin.site.register(Favorites)