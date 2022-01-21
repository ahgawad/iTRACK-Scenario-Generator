from django.contrib import admin
from django.forms.models import ModelForm

from .models import Awsd_incident
from .models import Awsd_incident_damage
from .models import Impact
from .models import Damage

#from .models import Sops_policies

from .models import Sop_policy
from .models import Sop_policy_damage_mitigation
from .models import Gtd_event
from .models import City_location
from .models import Natural_event
from .models import Natural_event_damage
from .models import Technical_event
from .models import Technical_event_damage
from .models import Technology_event
from .models import Technology_event_damage
from .models import Mechanical_event
from .models import Mechanical_event_damage
from .models import Traffic_event
from .models import Traffic_event_damage
from .models import City_attacker

from .models import Mission_default



admin.site.site_header = 'iTRACK Scenario Generator - administration'
admin.site.site_title = 'iTRACK Scenario Generator - administration'
admin.site.index_title = 'iTRACK Scenario Generator - administration'


#https://stackoverflow.com/questions/3657709/how-to-force-save-an-empty-unchanged-django-admin-inline
class AlwaysChangedModelForm(ModelForm):
    def has_changed(self, *args, **kwargs):
        if self.instance.pk is None:
            return True
        return super(AlwaysChangedModelForm, self).has_changed(*args, **kwargs)

#class Awsd_incident_damageInline(admin.TabularInline):
#    model = Awsd_incident
#    extra = 0

class Awsd_incidentAdmin(admin.ModelAdmin):
    list_display = ('id','Country','Location','Attack_context','Means_of_attack',)
    list_filter = ('Country','Location','Attack_context','Means_of_attack',)
    search_fields = ('id','Details',)
    #inlines = [ Awsd_incident_damageInline, ]

class Awsd_incident_damageAdmin(admin.ModelAdmin):
    list_display = ('id','Fixed_location','Fixed_attack_context','Fixed_means_of_attack',)
    list_filter = ('Fixed_location','Fixed_attack_context','Fixed_means_of_attack',)
    search_fields = ('Fixed_location','Fixed_attack_context','Fixed_means_of_attack',)

class DamageTypeInline(admin.TabularInline):
    model = Damage
    extra = 0
    form = AlwaysChangedModelForm

class ImpactAdmin(admin.ModelAdmin):
    list_display = ('id','Location','Attack_context','Means_of_attack','Impact','Impact_probability','Damage_type',)
    #list_editable = ('Location','Attack_context','Means_of_attack','Impact','Impact_probability',)
    list_filter = ('Impact','Location','Attack_context','Means_of_attack',)
    search_fields = ('Impact','Location','Attack_context','Means_of_attack',)
    inlines = [ DamageTypeInline, ]

class DamageTypeAdmin(admin.ModelAdmin):
    list_display  = ('id','Impact','Damage_type','Damage_probability_min', 'Damage_probability_max',)

'''
class Sops_policiesAdmin(admin.ModelAdmin):
    list_display = ('id','Ds_level','Sop_policy','Measure_family','Measure_type','Measure_description','Prerequesit_sop_policy','Implementation_stage','Damage_type','Damage_mitigation_fraction','Means_of_attack','Attack_context','Location','Mcda_criteria','Mcda_points','Implementation_cost','Cost_type','Measure_source',)
    list_editable = ('Ds_level','Sop_policy','Measure_family','Measure_type','Measure_description','Prerequesit_sop_policy','Implementation_stage','Damage_type','Damage_mitigation_fraction','Means_of_attack','Attack_context','Location','Mcda_criteria','Mcda_points','Implementation_cost','Cost_type','Measure_source',)
    list_filter = ('Location','Attack_context','Means_of_attack','Damage_type','Ds_level','Implementation_stage','Mcda_criteria',)
    search_fields = ('id','Measure_description',)
'''

class Gtd_eventAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ('id',)
    search_fields = ('id',)


class Mission_defaultAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ('id',)
    search_fields = ('id',)


class City_attackerAdmin(admin.ModelAdmin):
    list_display = ('id','Country', 'City', 'Latitude', 'Longitude', 'Attack_type', 'Gname', 'Weapon_type',)
    list_filter = ('Country', 'City', 'Latitude', 'Longitude', 'Attack_type', 'Gname', 'Weapon_type',)
    search_fields = ('Country', 'City', 'Latitude', 'Longitude', 'Attack_type', 'Gname', 'Weapon_type',)

class Natural_event_damageInline(admin.TabularInline):
    model = Natural_event_damage
    extra = 0
    form = AlwaysChangedModelForm

class Natural_eventAdmin(admin.ModelAdmin):
    list_display = ('id','Country','Location','Description','Impact','From_date','To_date','Event_probability',)
    #list_editable = ('Country','Location','Description','From_date','To_date','Event_probability',)
    list_filter = ('Country','Location','Description','From_date','To_date','Event_probability',)
    search_fields = ('Country','Location','Description','From_date','To_date','Event_probability',)
    inlines = [ Natural_event_damageInline, ]

class Natural_event_damageAdmin(admin.ModelAdmin):
    list_display  = ('id',)


class Technology_event_damageInline(admin.TabularInline):
    model = Technology_event_damage
    extra = 0
    form = AlwaysChangedModelForm

class Technology_eventAdmin(admin.ModelAdmin):
    list_display = ('id','Country','Location','Description','Impact','From_date','To_date','Event_probability',)
    #list_editable = ('Country','Location','Description','From_date','To_date','Event_probability',)
    list_filter = ('Country','Location','Description','From_date','To_date','Event_probability',)
    search_fields = ('Country','Location','Description','From_date','To_date','Event_probability',)
    inlines = [ Technology_event_damageInline, ]

class Technology_event_damageAdmin(admin.ModelAdmin):
    list_display  = ('id',)

class Mechanical_event_damageInline(admin.TabularInline):
    model = Mechanical_event_damage
    extra = 0
    form = AlwaysChangedModelForm

class Mechanical_eventAdmin(admin.ModelAdmin):
    list_display = ('id','Country','Location','Description','Impact','From_date','To_date','Event_probability',)
    #list_editable = ('Country','Location','Description','From_date','To_date','Event_probability',)
    list_filter = ('Country','Location','Description','From_date','To_date','Event_probability',)
    search_fields = ('Country','Location','Description','From_date','To_date','Event_probability',)
    inlines = [ Mechanical_event_damageInline, ]

class Mechanical_event_damageAdmin(admin.ModelAdmin):
    list_display  = ('id',)

class Traffic_event_damageInline(admin.TabularInline):
    model = Traffic_event_damage
    extra = 0
    form = AlwaysChangedModelForm

class Traffic_eventAdmin(admin.ModelAdmin):
    list_display = ('id','Country','Location','Description','Impact','From_date','To_date','Event_probability',)
    #list_editable = ('Country','Location','Description','From_date','To_date','Event_probability',)
    list_filter = ('Country','Location','Description','From_date','To_date','Event_probability',)
    search_fields = ('Country','Location','Description','From_date','To_date','Event_probability',)
    inlines = [ Traffic_event_damageInline, ]

class Traffic_event_damageAdmin(admin.ModelAdmin):
    list_display  = ('id',)

class Technical_event_damageInline(admin.TabularInline):
    model = Technical_event_damage
    extra = 0
    form = AlwaysChangedModelForm

class Technical_eventAdmin(admin.ModelAdmin):
    list_display = ('id','Country','Location','Description','Impact','From_date','To_date','Event_probability',)
    #list_editable = ('Country','Location','Description','From_date','To_date','Event_probability',)
    list_filter = ('Country','Location','Description','From_date','To_date','Event_probability',)
    search_fields = ('Country','Location','Description','From_date','To_date','Event_probability',)
    inlines = [ Technical_event_damageInline, ]

class Technical_event_damageAdmin(admin.ModelAdmin):
    list_display  = ('id',)




class Sop_policy_damage_mitigationInline(admin.TabularInline):
    model = Sop_policy_damage_mitigation
    extra = 0
    form = AlwaysChangedModelForm

class Sop_policyAdmin(admin.ModelAdmin):
    list_display = ('id','Ds_level','Sop_policy','Measure_family','Measure_type','Measure_description','Prerequesit_sop_policy','Implementation_stage','Means_of_attack','Attack_context','Location','Mcda_criteria','Mcda_points','Implementation_cost','Cost_type','Measure_source',)
    #list_editable = ('Ds_level','Sop_policy','Measure_family','Measure_type','Measure_description','Prerequesit_sop_policy','Implementation_stage','Means_of_attack','Attack_context','Location','Mcda_criteria','Mcda_points','Implementation_cost','Cost_type','Measure_source',)
    list_filter = ('Location','Attack_context','Means_of_attack','Ds_level','Implementation_stage','Mcda_criteria',)
    search_fields = ('Measure_description','Location','Attack_context','Means_of_attack','Ds_level','Implementation_stage','Mcda_criteria',)
    inlines = [ Sop_policy_damage_mitigationInline, ]

class Sop_policy_damage_mitigationAdmin(admin.ModelAdmin):
    list_display  = ('id','Damage_type','Damage_mitigation_fraction',)


#admin.site.register(Awsd_incident, Awsd_incidentAdmin)
admin.site.register(Awsd_incident_damage, Awsd_incident_damageAdmin)
admin.site.register(Impact, ImpactAdmin)
#admin.site.register(Damage, DamageTypeAdmin)

#this table was totally removed from the DB
#admin.site.register(Sops_policies, Sops_policiesAdmin)

#admin.site.register(Gtd_event, Gtd_eventAdmin)
#admin.site.register(Mission_default, Mission_defaultAdmin)
admin.site.register(City_attacker, City_attackerAdmin)

admin.site.register(Natural_event, Natural_eventAdmin)
#admin.site.register(Natural_event_damage, Natural_event_damageAdmin)


admin.site.register(Technology_event, Technology_eventAdmin)
#admin.site.register(Technology_event_damage, Technology_event_damageAdmin)
admin.site.register(Mechanical_event, Mechanical_eventAdmin)
#admin.site.register(Mechanical_event_damage, Mechanical_event_damageAdmin)
admin.site.register(Technical_event, Technical_eventAdmin)
#admin.site.register(Technical_event_damage, Technical_event_damageAdmin)
admin.site.register(Traffic_event, Traffic_eventAdmin)
#admin.site.register(Traffic_event_damage, Traffic_event_damageAdmin)


admin.site.register(Sop_policy, Sop_policyAdmin)
#admin.site.register(Sop_policy_damage_mitigation, Sop_policy_damage_mitigationAdmin)

