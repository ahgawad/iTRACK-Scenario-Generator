from django.db import models

keys_means_of_attacks={
    'AB': 'Aerial bombardment/missile/mortar/RPG/lobbed grenade',
    'BA': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons',
    'B': 'Bombing (set explosives with a stationary target: building: facility: home)',
    'BBIED': 'Body-borne IED',
    'CX': 'Complex attack (explosives in conjunction with small arms)',
    'RIED': 'Roadside IED',
    'VBIED': 'Vehicle-born IED (unknown whether remote control or suicide)',
    'VBIED-RC': 'Vehicle-borne IED (remote control detonation)',
    'VBIED-S': 'Vehicle-borne IED (suicide)',
    'K': 'Kidnapping (not killed)',
    'KK': 'Kidnap-killing',
    'RSA': 'Rape or serious sexual assault',
    'LM': 'Landmine or UXO detonation',
    'S': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns)',
    'U': 'Unknown',
    '*': 'Wildcard',
}
keys_means_of_attacks_fixed={
    'AB': 'Aerial bombardment/missile/mortar/RPG/lobbed grenade',
    'BA': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons',
    'BA-K': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons -> Kidnapping (not killed)',
    'B': 'Bombing (set explosives with a stationary target: building: facility: home)',
    'BBIED': 'Body-borne IED',
    'CX': 'Complex attack (explosives in conjunction with small arms)',
    'CX-K': 'Complex attack (explosives in conjunction with small arms) -> Kidnapping (not killed)',
    'RIED': 'Roadside IED',
    'VBIED': 'Vehicle-born IED (unknown whether remote control or suicide)',
    'VBIED-RC': 'Vehicle-borne IED (remote control detonation)',
    'VBIED-S': 'Vehicle-borne IED (suicide)',
    'S-K': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns) -> Kidnapping (not killed)',
    'S-KK': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns)) -> Kidnap-killing',
    'S-RSA': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns) -> Rape or serious sexual assault',
    'LM': 'Landmine or UXO detonation',
    'S': 'Shooting (small arms / light weapons: e.g. pistols: rifles: machine guns)',
    'U': 'Unknown',
    '*': 'Wildcard',
}
keys_attack_contexts={
    'Am': 'Ambush/attack on road',
    'C': 'Combat (or police operations) / Crossfire',
    'IA': 'Individual attack or assassination',
    'MV': 'Mob violence: rioting',
    'R': 'Raid (armed incursion by group on home: office: or project site)',
    'D': 'Detention (by official government forces or police: where abuse takes place)',
    'U': 'Unknown',
    '*': 'Wildcard',
}
keys_locations={
    'H': 'Home (private home: not compound)',
    'OC': 'Office or organization compound/residence',
    'PS': 'Project site (village: camp: distribution point: hospital: etc.)',
    'P': 'Other public location (street: market: restaurant: etc.)',
    'R': 'Road (in transit)',
    'C': 'Custody (official forces/police)',
    'U': 'Unknown',
    '*': 'Wildcard',
}

keys_damage_types={
    'KK': 'Staff killed',
    'K': 'Staff kidnapped',
    'W': 'Staff wounded',
    'RSA': 'Staff raped',
    'B': 'Damage in buildings',
    'V': 'Damage in vehicles',
    'C': 'Damage in commodities',
    'E': 'Damage in equipment',
    'U': 'Unknown',
    '*': 'Wildcard',
}

keys_sop_policies_ds_levels={
    'O': 'Operational',
    'T': 'Tactical',
    'S': 'Strategic',
}

keys_sop_policies_implementation_stages={
    'P': 'Precautionary',
    'A': 'Adaptive',
}

keys_sop_cost_types={
    'O': 'Overall',
    'I': 'Individual',
}

keys_sop_policies_types={
    'S': 'SOP',
    'P': 'Policy',
}

keys_countries = {
    'syria': 'Syrian Arab Republic',
    'iraq': 'Iraq',
    'yemen': 'Yemen',
    '*': 'Wildcard',
}

class Awsd_incident(models.Model):
    id=models.IntegerField('Incident ID', primary_key=True)
    Year=models.IntegerField(default=0)
    Month=models.CharField(max_length=2, null=True)
    Day=models.CharField(max_length=2, null=True)
    Country=models.CharField(max_length=32, null=True)
    Region=models.CharField(max_length=37, null=True)
    District=models.CharField(max_length=32, null=True)
    City=models.CharField(max_length=101, null=True)
    UN=models.IntegerField(default=0)
    INGO=models.IntegerField(default=0)
    LNGO_NRCS=models.IntegerField(default=0)
    ICRC=models.IntegerField(default=0)
    IFRC=models.IntegerField(default=0)
    Other=models.IntegerField(default=0)
    Nationals_killed=models.IntegerField(default=0)
    Nationals_wounded=models.IntegerField(default=0)
    Nationals_kidnapped=models.IntegerField(default=0)
    Total_nationals=models.IntegerField(default=0)
    Internationals_killed=models.IntegerField(default=0)
    Internationals_wounded=models.IntegerField(default=0)
    Internationals_kidnapped=models.IntegerField(default=0)
    Total_internationals=models.IntegerField(default=0)
    Total_killed=models.IntegerField(default=0)
    Total_wounded=models.IntegerField(default=0)
    Total_kidnapped=models.IntegerField(default=0)
    Total_affected=models.IntegerField(default=0)
    Gender_Male=models.IntegerField(default=0)
    Gender_Female=models.IntegerField(default=0)
    Gender_Unknown=models.IntegerField(default=0)

    Location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    Attack_context=models.CharField(max_length=10, choices=keys_attack_contexts.items(), null=True)
    # Attack_context=models.Field.attname='Attack context'

    Means_of_attack=models.CharField(max_length=10, choices=keys_means_of_attacks.items(), null=True)
    # Means_of_attack=models.Field.attname='Means of attack'


    Latitude=models.CharField(max_length=20, null=True)
    Longitude=models.CharField(max_length=11, null=True)
    Details=models.TextField(max_length=807, blank=True)

    def __str__(self):
       return 'Incident ID: ' + str(self.id)


class Awsd_incident_damage(Awsd_incident):
    #generatescenario_damage
    #generatescenario_responses
    #id=models.AutoField(primary_key=True)

    #id=models.IntegerField('Incident ID',primary_key=True)
    Incident_id=models.OneToOneField(Awsd_incident, verbose_name='Incident ID', on_delete=models.CASCADE, parent_link=True,primary_key=True)
    #id=models.OneToOneField(Awsd_incident, verbose_name='Incident ID', primary_key=True)

    #Incident_ID=models.Field.name='Incident ID'

    Fixed_location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    Fixed_attack_context=models.CharField(max_length=10, choices=keys_attack_contexts.items(), null=True)
    #Attack_context=models.Field.name='Attack context'

    Fixed_means_of_attack=models.CharField(max_length=10, choices=keys_means_of_attacks_fixed.items(), null=True)
    #Means_of_attack=models.Field.name='Means of attack'

    RSA=models.IntegerField(default=0)

    V=models.IntegerField('Vehicles Damage')
    E=models.IntegerField('Equipment Damage')
    C=models.IntegerField('Commodities Damage')
    B=models.IntegerField('Buildings Damage')

    def __str__(self):
       return 'Incident ID: ' + str(self.Incident_id)

    class Meta:
        verbose_name = 'AWSD Incident (Fixed)'
        verbose_name_plural = 'AWSD Incidents (Fixed)'

class Impact(models.Model):
    #generatescenario_impact
    #generatescenario_responses
    #id=models.AutoField(primary_key=True)
    id=models.AutoField('Impact ID',primary_key=True)

    Location=models.CharField(max_length=10, choices=keys_locations.items(), default='*')
    Attack_context=models.CharField(max_length=10, choices=keys_attack_contexts.items(), default='*')
    Means_of_attack=models.CharField(max_length=10, choices=keys_means_of_attacks_fixed.items(), default='*')
    Impact=models.CharField(max_length=100, null=True)
    Impact_probability=models.FloatField(default=0)

    def Damage_type(self):
        # use reverse relation to get a list of all recorded numbers
        damage_types=self.damage_set.values_list('Damage_type', flat=True)
        damage_types_count =self.damage_set.count()
        return "This security impact has %s damage types recorded: %s" % (damage_types_count, ', '.join(damage_types))

    def __str__(self):
       return 'Impact ID: ' + str(self.id)

    class Meta:
        verbose_name = 'Security Event Impact'
        verbose_name_plural = 'Security Event Impacts'

class Damage(models.Model):
    id=models.AutoField('Damage ID',primary_key=True)
    Impact=models.ForeignKey(Impact, on_delete=models.CASCADE)
    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_probability_min=models.FloatField(default=0)
    Damage_probability_max=models.FloatField(default=1)

    def __str__(self):
       return 'Damage ID: ' + str(self.id)

'''
class Sops_policies(models.Model):
    id=models.AutoField('SOP Policy ID',primary_key=True)
    Ds_level=models.CharField(max_length=1, choices=keys_sop_policies_ds_levels.items(), default='O')
    Sop_policy=models.CharField(max_length=1, choices=keys_sop_policies_types.items(), default='S')
    Measure_family=models.CharField(max_length=50, blank=True)
    Measure_type=models.CharField(max_length=50, blank=True)
    Measure_description=models.TextField(max_length=500)
    Prerequesit_sop_policy=models.CharField(max_length=100, blank=True)
    Implementation_stage=models.CharField(max_length=1, choices=keys_sop_policies_implementation_stages.items(), default='P')
    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_mitigation_fraction=models.FloatField(default=0)
    Means_of_attack=models.CharField(max_length=10, choices=keys_means_of_attacks_fixed.items(), default='*')
    Attack_context=models.CharField(max_length=10, choices=keys_attack_contexts.items(), default='*')
    Location=models.CharField(max_length=10, choices=keys_locations.items(), default='*')
    Mcda_criteria=models.CharField(max_length=50, blank=True)
    Mcda_points=models.IntegerField(default=0)
    Implementation_cost=models.IntegerField(default=0)
    Cost_type=models.CharField(max_length=1, choices=keys_sop_cost_types.items(), default='O')
    Measure_source=models.CharField(max_length=200, blank=True)

    def __str__(self):
       return 'SOP/Policy ID: ' + str(self.id)
'''

class Sop_policy(models.Model):
    id=models.AutoField('SOP Policy ID',primary_key=True)
    Ds_level=models.CharField(max_length=1, choices=keys_sop_policies_ds_levels.items(), default='O')
    Sop_policy=models.CharField(max_length=1, choices=keys_sop_policies_types.items(), default='S')
    Measure_family=models.CharField(max_length=50, blank=True)
    Measure_type=models.CharField(max_length=50, blank=True)
    Measure_description=models.TextField(max_length=500)
    Prerequesit_sop_policy=models.CharField(max_length=100, blank=True)
    Implementation_stage=models.CharField(max_length=1, choices=keys_sop_policies_implementation_stages.items(), default='P')
    #Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    #Damage_mitigation_fraction=models.FloatField(default=0)
    Means_of_attack=models.CharField(max_length=10, choices=keys_means_of_attacks_fixed.items(), default='*')
    Attack_context=models.CharField(max_length=10, choices=keys_attack_contexts.items(), default='*')
    Location=models.CharField(max_length=10, choices=keys_locations.items(), default='*')
    Mcda_criteria=models.CharField(max_length=50, blank=True)
    Mcda_points=models.IntegerField(default=0)
    Implementation_cost=models.IntegerField(default=0)
    Cost_type=models.CharField(max_length=1, choices=keys_sop_cost_types.items(), default='O')
    Measure_source=models.CharField(max_length=200, blank=True)

    def Damage_mitigation_type(self):
        # use reverse relation to get a list of all recorded numbers
        sop_policy_damage_mitigation_types=self.sop_policy_damage_mitigation_set.values_list('Damage_type', flat=True)
        sop_policy_damage_mitigation_types_count =self.sop_policy_damage_mitigation_set.count()
        return "This SOP/Policy has %s damage mitigation types recorded: %s" % (sop_policy_damage_mitigation_types_count, ', '.join(sop_policy_damage_mitigation_types))

    def __str__(self):
       return 'SOP/Policy ID: ' + str(self.id)

    class Meta:
        verbose_name = 'SOP/Policy'
        verbose_name_plural = 'SOPs/Policies'

class Sop_policy_damage_mitigation(models.Model):
    id=models.AutoField('Damage mitigation type ID',primary_key=True)

    Sop_policy=models.ForeignKey(Sop_policy, on_delete=models.CASCADE)

    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_mitigation_fraction=models.FloatField(default=0)

    def __str__(self):
       return 'SOP Policy Damage Mitigation Type ID: ' + str(self.id)


class Gtd_event(models.Model):
    id=models.BigIntegerField('Event ID', primary_key=True)
    Iyear=models.IntegerField(default=0)
    Imonth=models.IntegerField(default=0)
    Iday=models.IntegerField(default=0)
    Approxdate=models.CharField(max_length=27, null=True)
    Extended=models.IntegerField(default=0)
    Resolution=models.CharField(max_length=10, null=True)
    Country=models.IntegerField(default=0)
    Country_txt=models.CharField(max_length=5, null=True)
    Region=models.IntegerField(default=0)
    Region_txt=models.CharField(max_length=26, null=True)
    Provstate=models.CharField(max_length=16, null=True)
    City=models.CharField(max_length=26, null=True)
    Ilatitude=models.CharField(max_length=9, null=True)
    Ilongitude=models.CharField(max_length=9, null=True)
    Specificity=models.IntegerField(default=0)
    Vicinity=models.IntegerField(default=0)
    Location=models.CharField(max_length=255, null=True)
    Summary=models.CharField(max_length=255, null=True)
    Crit1=models.CharField(max_length=255, null=True)
    Crit2=models.IntegerField(default=0)
    Crit3=models.IntegerField(default=0)
    Doubtterr=models.IntegerField(default=0)
    Alternative=models.CharField(max_length=1, null=True)
    Alternative_txt=models.CharField(max_length=26, null=True)
    Multiple=models.CharField(max_length=26, null=True)
    Success=models.IntegerField(default=0)
    Suicide=models.IntegerField(default=0)
    Attacktype1=models.IntegerField(default=0)
    Attacktype1_txt=models.CharField(max_length=35, null=True)
    Attacktype2=models.CharField(max_length=27, null=True)
    Attacktype2_txt=models.CharField(max_length=35, null=True)
    Attacktype3=models.CharField(max_length=1, null=True)
    Attacktype3_txt=models.CharField(max_length=30, null=True)
    Targtype1=models.CharField(max_length=2, null=True)
    Targtype1_txt=models.CharField(max_length=30, null=True)
    Targsubtype1=models.CharField(max_length=27, null=True)
    Targsubtype1_txt=models.CharField(max_length=71, null=True)
    Corp1=models.CharField(max_length=111, null=True)
    Target1=models.CharField(max_length=255, null=True)
    Natlty1=models.CharField(max_length=111, null=True)
    Natlty1_txt=models.CharField(max_length=95, null=True)
    Targtype2=models.CharField(max_length=31, null=True)
    Targtype2_txt=models.CharField(max_length=31, null=True)
    Targsubtype2=models.CharField(max_length=55, null=True)
    Targsubtype2_txt=models.CharField(max_length=71, null=True)
    Corp2=models.CharField(max_length=69, null=True)
    Target2=models.CharField(max_length=169, null=True)
    Natlty2=models.CharField(max_length=55, null=True)
    Natlty2_txt=models.CharField(max_length=24, null=True)
    Targtype3=models.CharField(max_length=27, null=True)
    Targtype3_txt=models.CharField(max_length=30, null=True)
    Targsubtype3=models.CharField(max_length=39, null=True)
    Targsubtype3_txt=models.CharField(max_length=60, null=True)
    Corp3=models.CharField(max_length=70, null=True)
    Target3=models.CharField(max_length=81, null=True)
    Natlty3=models.CharField(max_length=27, null=True)
    Natlty3_txt=models.CharField(max_length=43, null=True)
    Gname=models.CharField(max_length=64, null=True)
    Gsubname=models.CharField(max_length=74, null=True)
    Gname2=models.CharField(max_length=53, null=True)
    Gsubname2=models.CharField(max_length=47, null=True)
    Gname3=models.CharField(max_length=255, null=True)
    Gsubname3=models.CharField(max_length=255, null=True)
    Motive=models.CharField(max_length=255, null=True)
    Guncertain1=models.CharField(max_length=153, null=True)
    Guncertain2=models.CharField(max_length=233, null=True)
    Guncertain3=models.CharField(max_length=3, null=True)
    Individual=models.CharField(max_length=3, null=True)
    Nperps=models.CharField(max_length=4, null=True)
    Nperpcap=models.CharField(max_length=3, null=True)
    Claimed=models.CharField(max_length=29, null=True)
    Claimmode=models.CharField(max_length=29, null=True)
    Claimmode_txt=models.CharField(max_length=29, null=True)
    Claim2=models.CharField(max_length=29, null=True)
    Claimmode2=models.CharField(max_length=29, null=True)
    Claimmode2_txt=models.CharField(max_length=29, null=True)
    Claim3=models.CharField(max_length=29, null=True)
    Claimmode3=models.CharField(max_length=29, null=True)
    Claimmode3_txt=models.CharField(max_length=29, null=True)
    Compclaim=models.CharField(max_length=29, null=True)
    Weaptype1=models.CharField(max_length=39, null=True)
    Weaptype1_txt=models.CharField(max_length=75, null=True)
    Weapsubtype1=models.CharField(max_length=41, null=True)
    Weapsubtype1_txt=models.CharField(max_length=41, null=True)
    Weaptype2=models.CharField(max_length=41, null=True)
    Weaptype2_txt=models.CharField(max_length=75, null=True)
    Weapsubtype2=models.CharField(max_length=41, null=True)
    Weapsubtype2_txt=models.CharField(max_length=41, null=True)
    Weaptype3=models.CharField(max_length=41, null=True)
    Weaptype3_txt=models.CharField(max_length=75, null=True)
    Weapsubtype3=models.CharField(max_length=29, null=True)
    Weapsubtype3_txt=models.CharField(max_length=41, null=True)
    Weaptype4=models.CharField(max_length=16, null=True)
    Weaptype4_txt=models.CharField(max_length=54, null=True)
    Weapsubtype4=models.CharField(max_length=117, null=True)
    Weapsubtype4_txt=models.CharField(max_length=159, null=True)
    Weapdetail=models.CharField(max_length=255, null=True)
    Nkill=models.CharField(max_length=83, null=True)
    Nkillus=models.CharField(max_length=7, null=True)
    Nkillter=models.CharField(max_length=3, null=True)
    Nwound=models.CharField(max_length=4, null=True)
    Nwoundus=models.CharField(max_length=2, null=True)
    Nwoundte=models.CharField(max_length=27, null=True)
    Property=models.CharField(max_length=27, null=True)
    Propextent=models.CharField(max_length=67, null=True)
    Propextent_txt=models.CharField(max_length=158, null=True)
    Propvalue=models.CharField(max_length=128, null=True)
    Propcomment=models.CharField(max_length=255, null=True)
    Ishostkid=models.CharField(max_length=86, null=True)
    Nhostkid=models.CharField(max_length=51, null=True)
    Nhostkidus=models.CharField(max_length=3, null=True)
    Nhours=models.CharField(max_length=3, null=True)
    Ndays=models.CharField(max_length=4, null=True)
    Divert=models.CharField(max_length=8, null=True)
    Kidhijcountry=models.CharField(max_length=8, null=True)
    Ransom=models.CharField(max_length=7, null=True)
    Ransomamt=models.CharField(max_length=9, null=True)
    Ransomamtus=models.CharField(max_length=9, null=True)
    Ransompaid=models.CharField(max_length=8, null=True)
    Ransompaidus=models.CharField(max_length=3, null=True)
    Ransomnote=models.CharField(max_length=255, null=True)
    Hostkidoutcome=models.CharField(max_length=150, null=True)
    Hostkidoutcome_txt=models.CharField(max_length=255, null=True)
    Nreleased=models.CharField(max_length=255, null=True)
    Addnotes=models.CharField(max_length=255, null=True)
    Scite1=models.CharField(max_length=255, null=True)
    Scite2=models.CharField(max_length=255, null=True)
    Scite3=models.CharField(max_length=255, null=True)
    Dbsource=models.CharField(max_length=144, null=True)
    Int_log=models.CharField(max_length=89, null=True)
    Int_ideo=models.CharField(max_length=24, null=True)
    Int_misc=models.CharField(max_length=208, null=True)
    Int_any=models.CharField(max_length=255, null=True)
    Related=models.CharField(max_length=255, null=True)

    def __str__(self):
       return 'Event ID: ' + str(self.id)


class City_attacker(models.Model):
    id=models.BigIntegerField('Record ID', primary_key=True)
    Attack_date=models.DateField(default="2000-01-01")
    Country=models.CharField(max_length=5, null=True)
    City=models.CharField(max_length=26, null=True)
    Latitude=models.CharField(max_length=9, null=True)
    Longitude=models.CharField(max_length=9, null=True)
    Attack_type=models.CharField(max_length=35, null=True)
    Gname=models.CharField(max_length=64, null=True)
    Weapon_type=models.CharField(max_length=75, null=True)

    def __str__(self):
       return 'Record ID: ' + str(self.id)

    class Meta:
        verbose_name = 'City Attacker Record'
        verbose_name_plural = 'City Attacker Records'


class City_location(models.Model):
    id=models.AutoField('City ID', primary_key=True)
    City=models.CharField(max_length=30, null=False)
    Country=models.CharField(max_length=10, null=False)
    Latitude=models.FloatField(default=0)
    Longitude=models.FloatField(default=0)

    def __str__(self):
       return 'City ID: ' + str(self.id)



class Mission_default(models.Model):
    id=models.AutoField(primary_key=True)

    Country=models.CharField(max_length=32, null=True)
    Location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    mission_leader=models.IntegerField('Mission leaders', 0)
    logistics_officer=models.IntegerField('Logistics Officers', 0)
    warehouse_manager=models.IntegerField('warehouse Managers', 0)
    transportation_manager=models.IntegerField('transportation_managers', 0)
    distribution_manager=models.IntegerField('distribution_managers', 0)
    information_management_officer=models.IntegerField('Information Management Officers', 0)
    data_coordinator=models.IntegerField('Data Coordinators', 0)
    gis_specialist=models.IntegerField('GIS Specialists', 0)
    security_officer=models.IntegerField('Security Officers', 0)
    assessment_monitoring_support=models.IntegerField('Assessment Monitoring Support', 0)
    im_focal_points=models.IntegerField('IM Focal Points', 0)
    local_transportation=models.IntegerField('Local Transportation', 0)
    local_warehouse=models.IntegerField('Local Warehouse', 0)
    local_security=models.IntegerField('Local Security', 0)
    local_ngos=models.IntegerField('Local NGOs', 0)
    local_government=models.IntegerField('Local Government', 0)
    local_communities=models.IntegerField('Local Communities', 0)

    V=models.IntegerField('Vehicles', 0)
    E=models.IntegerField('Equipment Units', 0)
    C=models.IntegerField('Commodities Units', 0)
    B=models.IntegerField('Buildings', 0)

    def __str__(self):
       return 'ID: ' + str(self.id)


class Natural_event(models.Model):
    id=models.AutoField(primary_key=True)

    Country=models.CharField(max_length=32, choices=keys_countries.items(), default='*')
    Location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    Description=models.TextField(max_length=100, null=True)
    Impact=models.CharField(max_length=100, null=True)

    From_date=models.DateField(default="2000-01-01")
    To_date=models.DateField(default="2000-12-31")

    #From_date1=models.DateField(default="2000-01-01")
    #To_date1=models.DateField(default="2000-12-31")

    Event_probability=models.FloatField(default=0)

    def Natural_event_damage_type(self):
        # use reverse relation to get a list of all recorded numbers
        damage_types=self.damage_set.values_list('Damage_type', flat=True)
        damage_types_count=self.damage_set.count()
        return "This natural event has %s damage types recorded: %s" % (damage_types_count, ', '.join(damage_types))

    def __str__(self):
        return 'ID: ' + str(self.id)

    class Meta:
        verbose_name = 'Natural Event'
        verbose_name_plural = 'Natural Events'

class Natural_event_damage(models.Model):
    id=models.AutoField(primary_key=True)
    Natural_event=models.ForeignKey(Natural_event, on_delete=models.CASCADE)
    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_probability_min=models.FloatField(default=0)
    Damage_probability_max=models.FloatField(default=1)

    def __str__(self):
        return 'ID: ' + str(self.id)





class Technology_event(models.Model):
    id=models.AutoField(primary_key=True)

    Country=models.CharField(max_length=32, choices=keys_countries.items(), default='*')
    Location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    Description=models.TextField(max_length=100, null=True)
    Impact=models.CharField(max_length=100, null=True)

    From_date=models.DateField(default="2000-01-01")
    To_date=models.DateField(default="2000-12-31")

    #From_date1=models.DateField(default="2000-01-01")
    #To_date1=models.DateField(default="2000-12-31")

    Event_probability=models.FloatField(default=0)

    def Technology_event_damage_type(self):
        # use reverse relation to get a list of all recorded numbers
        damage_types=self.damage_set.values_list('Damage_type', flat=True)
        damage_types_count=self.damage_set.count()
        return "This technology event has %s damage types recorded: %s" % (damage_types_count, ', '.join(damage_types))

    def __str__(self):
        return 'ID: ' + str(self.id)

    class Meta:
        verbose_name = 'Technology Event'
        verbose_name_plural = 'Technology Events'

class Technology_event_damage(models.Model):
    id=models.AutoField(primary_key=True)
    Technology_event=models.ForeignKey(Technology_event, on_delete=models.CASCADE)
    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_probability_min=models.FloatField(default=0)
    Damage_probability_max=models.FloatField(default=1)

    def __str__(self):
        return 'ID: ' + str(self.id)

class Mechanical_event(models.Model):
    id=models.AutoField(primary_key=True)

    Country=models.CharField(max_length=32, choices=keys_countries.items(), default='*')
    Location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    Description=models.TextField(max_length=100, null=True)
    Impact=models.CharField(max_length=100, null=True)

    From_date=models.DateField(default="2000-01-01")
    To_date=models.DateField(default="2000-12-31")

    #From_date1=models.DateField(default="2000-01-01")
    #To_date1=models.DateField(default="2000-12-31")

    Event_probability=models.FloatField(default=0)

    def Mechanical_event_damage_type(self):
        # use reverse relation to get a list of all recorded numbers
        damage_types=self.damage_set.values_list('Damage_type', flat=True)
        damage_types_count=self.damage_set.count()
        return "This mechanical event has %s damage types recorded: %s" % (damage_types_count, ', '.join(damage_types))

    def __str__(self):
        return 'ID: ' + str(self.id)

    class Meta:
        verbose_name = 'Mechanical Event'
        verbose_name_plural = 'Mechanical Events'

class Mechanical_event_damage(models.Model):
    id=models.AutoField(primary_key=True)
    Mechanical_event=models.ForeignKey(Mechanical_event, on_delete=models.CASCADE)
    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_probability_min=models.FloatField(default=0)
    Damage_probability_max=models.FloatField(default=1)

    def __str__(self):
        return 'ID: ' + str(self.id)

class Traffic_event(models.Model):
    id=models.AutoField(primary_key=True)

    Country=models.CharField(max_length=32, choices=keys_countries.items(), default='*')
    Location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    Description=models.TextField(max_length=100, null=True)
    Impact=models.CharField(max_length=100, null=True)

    From_date=models.DateField(default="2000-01-01")
    To_date=models.DateField(default="2000-12-31")

    #From_date1=models.DateField(default="2000-01-01")
    #To_date1=models.DateField(default="2000-12-31")

    Event_probability=models.FloatField(default=0)

    def Traffic_event_damage_type(self):
        # use reverse relation to get a list of all recorded numbers
        damage_types=self.damage_set.values_list('Damage_type', flat=True)
        damage_types_count=self.damage_set.count()
        return "This traffic event has %s damage types recorded: %s" % (damage_types_count, ', '.join(damage_types))

    def __str__(self):
        return 'ID: ' + str(self.id)

    class Meta:
        verbose_name = 'Traffic Event'
        verbose_name_plural = 'Traffic Events'

class Traffic_event_damage(models.Model):
    id=models.AutoField(primary_key=True)
    Traffic_event=models.ForeignKey(Traffic_event, on_delete=models.CASCADE)
    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_probability_min=models.FloatField(default=0)
    Damage_probability_max=models.FloatField(default=1)

    def __str__(self):
        return 'ID: ' + str(self.id)

class Technical_event(models.Model):
    id=models.AutoField(primary_key=True)

    Country=models.CharField(max_length=32, choices=keys_countries.items(), default='*')
    Location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    Description=models.TextField(max_length=100, null=True)
    Impact=models.CharField(max_length=100, null=True)

    From_date=models.DateField(default="2000-01-01")
    To_date=models.DateField(default="2000-12-31")

    #From_date1=models.DateField(default="2000-01-01")
    #To_date1=models.DateField(default="2000-12-31")

    Event_probability=models.FloatField(default=0)

    def Technical_event_damage_type(self):
        # use reverse relation to get a list of all recorded numbers
        damage_types=self.damage_set.values_list('Damage_type', flat=True)
        damage_types_count=self.damage_set.count()
        return "This technical event has %s damage types recorded: %s" % (damage_types_count, ', '.join(damage_types))

    def __str__(self):
        return 'ID: ' + str(self.id)

    class Meta:
        verbose_name = 'Technical Event'
        verbose_name_plural = 'Technical Events'

class Technical_event_damage(models.Model):
    id=models.AutoField(primary_key=True)
    Technical_event=models.ForeignKey(Technical_event, on_delete=models.CASCADE)
    Damage_type=models.CharField(max_length=10, choices=keys_damage_types.items(), default='*')
    Damage_probability_min=models.FloatField(default=0)
    Damage_probability_max=models.FloatField(default=1)

    def __str__(self):
        return 'ID: ' + str(self.id)






'''
# empty table
class mission_defaults(models.Model):
    id=models.AutoField(primary_key=True)
    
    Country=models.CharField(max_length=32, null=True)
    Location=models.CharField(max_length=10, choices=keys_locations.items(), null=True)

    def __str__(self):
       return 'ID: ' + str(self.id)
'''
