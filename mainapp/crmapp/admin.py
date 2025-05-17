from django.contrib import admin
from .models import Contact, Deal, Stage, Funnel


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    pass


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    pass


@admin.register(Funnel)
class FunnelAdmin(admin.ModelAdmin):
    pass
