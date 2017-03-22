from django.contrib import admin
from .models import Region
# from .models import Departement, City


# Register your models here.
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "num_tweets_pos", "num_tweets_neg", 'num_tweets_net',
                    "num_tweets_pos_pred", "num_tweets_neg_pred", 'num_tweets_net_pred', "color"]

    class Meta:
        model = Region

admin.site.register(Region, RegionAdmin)

# class DepartementAdmin(admin.ModelAdmin):
#     list_display = ["name", "region_code", "num_tweets_pos", "num_tweets_neg", 'num_tweets_net']
#
#     class Meta:
#         model = Departement
#
#
# class CityAdmin(admin.ModelAdmin):
#     list_display = ["name", "pk", "num_tweets_pos", "num_tweets_neg", 'num_tweets_net']
#
#     class Meta:
#         model = City
# admin.site.register(Departement, DepartementAdmin)
# admin.site.register(City, CityAdmin)

    # def upper_case_name(self, obj):
    #     return ("%s %s" % (obj.first_name, obj.last_name)).upper()


