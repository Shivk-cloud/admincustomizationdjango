

# Register your models here.
from django.contrib import admin
from .models import Category, Product, Customer, Order
from djangoql.admin import DjangoQLSearchMixin
from import_export import resources  
from import_export.admin import ImportExportMixin
from django.urls import reverse
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'id',)
    prepopulated_fields = {'slug': ('name',)}  # new


admin.site.register(Category, CategoryAdmin)



class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'is_active', 'id',)

class ProductAdmin(ImportExportMixin,DjangoQLSearchMixin,admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'id',)
    prepopulated_fields = {'slug': ('name',)}  # new
    filter_horizontal = ('category',)  # new
    search_fields = ('name',) #  new
    list_filter = ('category', 'is_active',)
    resource_classes=(ProductResource,)


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'id',)


admin.site.register(Customer, CustomerAdmin)


class OnlyActiveOrdersFilter(admin.SimpleListFilter):
    title = 'Show Only Active Orders'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(status__in=(ORDER_STATUSES.new, ORDER_STATUSES.processing, ORDER_STATUSES.shipped))
        return queryset


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_dt',
        'completed_dt',
        'status',
        'link_to_customer',
    )
    list_filter = ('status', OnlyActiveOrdersFilter,)
    list_display_links = ('id', 'created_dt',)
    list_select_related = ('customer',)  # new

    def link_to_customer(self, obj):
        link = reverse("admin:myapp_customer_change", args=[obj.customer.id])
        return format_html(
            '<a href="{}">{}</a>',
            link,
            obj.customer,
        )

    link_to_customer.short_description = 'Customer'


admin.site.register(Order, OrderAdmin)


class SomeModelAdmin(admin.ModelAdmin):
    ordering = ('name',)