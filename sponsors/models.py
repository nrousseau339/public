from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey

from home.models import ATVLink, SponsorLink, Contact

#create model for sponsor levels, used as a sort for the sponsor index page
class SponsorLevels(models.Model):
    level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], unique=True, primary_key=True)
    sponsorship = models.CharField(max_length=150)
    long_description = models.CharField(max_length=255)

    def __str__(self):
        return(str(self.level))


class SponsorsIndexPage(Page):
    #is_creatable = False

    def get_context(self, request):
        context = super().get_context(request)
        #sponsorpages = self.get_children().live().order_by("-title")
        sponsorpages = SponsorsPage.objects.live().order_by("level")
        context['sponsorpages'] = sponsorpages
        return context
    def atvlink(self):
        return ATVLink.objects.get()
    def sponsorlink(self):
        return SponsorLink.objects.get()
    def contactlink(self):
        return Contact.objects.get()

    content_panels = Page.content_panels + [

                #FieldPanel('type'),

    ]

class SponsorsPage(Page):
    level_choice = SponsorLevels.objects.values_list('level','sponsorship',)
    level = models.IntegerField(choices=level_choice, blank=True, null=True)
    website = models.URLField(null=True, blank=True)
    
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = [
        MultiFieldPanel
            ([
                FieldPanel('title', heading='Sponsor', help_text='Add sponsor name'),
                FieldPanel('level', heading='Sponsorship Level', help_text='Add sponsorship level'),
                FieldPanel('website', help_text='Add sponsor website URL'),
            ]),
        InlinePanel('gallery_images', label="Gallery images"),
   ]




class SponsorLogo(Orderable):
    #is_creatable = False
    page = ParentalKey(SponsorsPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


