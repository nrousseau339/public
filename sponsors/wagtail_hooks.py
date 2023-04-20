from django.urls import path, reverse
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.admin.menu import MenuItem
from wagtail import hooks

from .models import SponsorLevels

#from .views import index
def index():
    return None


#register addon URL patterns with Wagtail URLS
@hooks.register('register_admin_urls')
def register_sponsor_url():
    return [
        path('pages/add/sponsors/sponsorspage/5/',index, name='pages/add/sponsors/sponsorspage/5/'),
    ]

#add link on admin page to quickly get to the page to add a new event
@hooks.register('register_admin_menu_item')
def register_sponsor_form_menu_item():
    return MenuItem('Add Sponsor', reverse('pages/add/sponsors/sponsorspage/5/'), icon_name='plus', order=2)



class ContactAdmin(ModelAdmin):
    model = SponsorLevels
    menu_label = "Sponsorship Levels"
    menu_icon = "pick"
    menu_order = 7
    #add_to_settings_menu = True




modeladmin_register(ContactAdmin)