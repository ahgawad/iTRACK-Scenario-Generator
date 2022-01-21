from .models import Awsd_incident
from .models import Awsd_incident_damage
from .models import Impact
from .models import Damage

#from .models import sops_policies

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

import math
import graphviz
import functools
import random
import sys
from decimal import *
from datetime import datetime


from django.db import connection
# import the logging library
import logging


# Initialisations - Start
mena_countries = ['Iraq', 'Jordan', 'Lebanon', 'Libyan Arab Jamahiriya', 'Mauritania',
                  'Occupied Palestinian Territories', 'Somalia', 'South Sudan', 'Sudan', 'Syrian Arab Republic',
                  'Tunisia', 'Turkey', 'Yemen']

countries = {
    'syria': 'Syrian Arab Republic',
    'iraq': 'Iraq',
    'yemen': 'Yemen'
}

# K, KK, RSA --> S-K, S-KK, S-RSA, CX-K, BA-K
# Generate new column RSA number of wounded or (0 and 1)
# drop U
keys_means_of_attacks = {
    'AB': 'Aerial bombardment/missile/mortar/RPG/lobbed grenade',
    'BA': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons',
    'BA-K': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons -> Kidnapping (not killed)',
    'B': 'Bombing (set explosives with a stationary target, building, facility, home)',
    'BBIED': 'Body-borne IED',
    'CX': 'Complex attack (explosives in conjunction with small arms)',
    'CX-K': 'Complex attack (explosives in conjunction with small arms) -> Kidnapping (not killed)',
    'RIED': 'Roadside IED',
    'VBIED': 'Vehicle-born IED (unknown whether remote control or suicide)',
    'VBIED-RC': 'Vehicle-borne IED (remote control detonation)',
    'VBIED-S': 'Vehicle-borne IED (suicide)',
    'K': 'Kidnapping (not killed)',
    'KK': 'Kidnap-killing',
    'RSA': 'Rape or serious sexual assault',
    'S-K': 'Shooting (small arms / light weapons; e.g. pistols, rifles, machine guns) -> Kidnapping (not killed)',
    'S-KK': 'Shooting (small arms / light weapons; e.g. pistols, rifles, machine guns)) -> Kidnap-killing',
    'S-RSA': 'Shooting (small arms / light weapons; e.g. pistols, rifles, machine guns) -> Rape or serious sexual assault',
    'LM': 'Landmine or UXO detonation',
    'S': 'Shooting (small arms / light weapons; e.g. pistols, rifles, machine guns)',
    'U': 'Unknown',
}
keys_means_of_attacks = {
    'AB': 'Aerial bombardment/missile/mortar/RPG/lobbed grenade',
    'BA': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons',
    'BA-K': 'Bodily assault/beating/stabbing with non-fire weapons or no weapons',
    'B': 'Bombing (set explosives with a stationary target, building, facility, home)',
    'BBIED': 'Body-borne IED',
    'CX': 'Complex attack (explosives in conjunction with small arms)',
    'CX-K': 'Complex attack (explosives in conjunction with small arms)',
    'RIED': 'Roadside IED',
    'VBIED': 'Vehicle-born IED (unknown whether remote control or suicide)',
    'VBIED-RC': 'Vehicle-borne IED (remote control detonation)',
    'VBIED-S': 'Vehicle-borne IED (suicide)',
    'K': 'Kidnapping (not killed)',
    'KK': 'Kidnap-killing',
    'RSA': 'Rape or serious sexual assault',
    'S-K': 'Shooting (small arms / light weapons; e.g. pistols, rifles, machine guns)',
    'S-KK': 'Shooting (small arms / light weapons; e.g. pistols, rifles, machine guns))',
    'S-RSA': 'Shooting (small arms / light weapons; e.g. pistols, rifles, machine guns)',
    'LM': 'Landmine or UXO detonation',
    'S': 'Shooting (small arms / light weapons; e.g. pistols, rifles, machine guns)',
    'U': 'Unknown',
}
# drop U
keys_attack_contexts = {
    'Am': 'Ambush/attack on road',
    'C': 'Combat (or police operations) / Crossfire',
    'IA': 'Individual attack or assassination',
    'MV': 'Mob violence, rioting',
    'R': 'Raid (armed incursion by group on home, office, or project site)',
    'D': 'Detention (by official government forces or police, where abuse takes place)',
    'U': 'Unknown',
}
# drop U
keys_locations = {
    'H': 'Home (private home, not compound)',
    'OC': 'Office or organization compound/residence',
    'PS': 'Project site (village, camp, distribution point, hospital, etc.)',
    'P': 'Other public location (street, market, restaurant, etc.)',
    'R': 'Road (in transit)',
    'C': 'Custody (official forces/police)',
    'U': 'Unknown',
}

keys_damage_types = {
    'KK': 'Staff killed',
    'K': 'Staff kidnapped',
    'W': 'Staff wounded',
    'RSA': 'Staff raped',
    'B': 'Damage in buildings',
    'V': 'Damage in vehicles',
    'C': 'Damage in commodities',
    'E': 'Damage in equipment',
    'U': 'Unknown',
}

keys_damage_types_wo_u = {
    'KK': 'Staff killed',
    'K': 'Staff kidnapped',
    'W': 'Staff wounded',
    'RSA': 'Staff raped',
    'B': 'Damage in buildings',
    'V': 'Damage in vehicles',
    'C': 'Damage in commodities',
    'E': 'Damage in equipment',
}

# Initialisations - End


# Graphviz helpers - Start
styles_overall = {
    'graph': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'rankdir': 'TB',
        'tooltip': 'Scenario module',
    },
    'nodes': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
    },
    'edges': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'arrowhead': 'open',
    }
}

styles_base = {
    'graph': {
        'label': 'Base',
        'labeljust': 'l',
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'rankdir': 'TB',
        'tooltip': 'Base',
    },
    'nodes': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'shape': 'rectangle',
        'style': 'filled',
        'fillcolor': '#ffbf00',
    },
    'edges': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'arrowhead': 'open',
    }
}

styles_impact = {
    'graph': {
        'label': 'Impact',
        'labeljust': 'l',
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'rankdir': 'TB',
        'tooltip': 'Impact',
    },
    'nodes': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'shape': 'box',
        'style': 'filled',
        'fillcolor': '#ff8000',
    },
    'edges': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'arrowhead': 'open',
    }
}

styles_damage = {
    'graph': {
        'label': 'Damage',
        'labeljust': 'l',
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'rankdir': 'TB',
        'tooltip': 'Damage',
    },
    'nodes': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'shape': 'rectangle',
        'style': 'filled',
        'fillcolor': '#FF0000',
    },
    'edges': {
        'fontname': 'Segoe UI',
        'fontsize': '11',
        'arrowhead': 'open',
    }
}


def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph


def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph


def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph


# Graphviz helpers - End


# Calculate distance between 2 cities in Kilometers using their Latitudes and Logitudes
def dis_bet_cities(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def get_len(rawqueryset):
    sql = 'SELECT COUNT(*) FROM (' + rawqueryset + ') B;'
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    return row[0]


# Main function - Start
def generate_scenario_module(missionID, mission_level, last_mission_score, last_mission_score_1, last_mission_score_2, seed_value, country, location, current_day, current_month):
    # Get an instance of a logger
    logger = logging.getLogger(__name__)

    sops_policies = {
        'sops_policies_precautionary_strategic': [],
        'sops_policies_precautionary_tactical': [],
        'sops_policies_precautionary_operational': [],
        'sops_policies_adaptive_strategic': [],
        'sops_policies_adaptive_tactical': [],
        'sops_policies_adaptive_operational': [],
    }
    generated_damage_types = {}
    scenario_location = ''
    scenario_attack_context = ''
    scenario_means_of_attack = ''
    scenario_attackers_group_name = ''
    scenario_cities = []
    scenario_total_damage_mitigation_fraction_by_type = []

    damage_probability_by_type_min = keys_damage_types_wo_u.fromkeys(list(keys_damage_types_wo_u.keys()), 0)
    damage_probability_by_type_max = keys_damage_types_wo_u.fromkeys(list(keys_damage_types_wo_u.keys()), 0)
    damage_probability_by_type = keys_damage_types_wo_u.fromkeys(list(keys_damage_types_wo_u.keys()), 0)

    scenario_svg = ''
    p_base = 0
    cumulativeProbability = 0
    nodes_base = set([])
    edges_base = set([])
    generated_scenario_node_impact = ''
    nodes_impact = set([])
    edges_impact = set([])
    generated_scenario_node_damage = {}
    nodes_damage = set([])
    edges_damage = set([])

    digraph = functools.partial(graphviz.Digraph, format='svg')

    location = location.upper()
    if location not in keys_locations:
        location = 'R'

    country = country.lower()
    Gtd_country = country.title()
    if country in countries:
        Awsd_country = countries[country]
    else:
        Awsd_country = 'Syrian Arab Republic'

    random.seed(seed_value)

    # ******************************************************************
    # Generate Location / Attack Context / Means of Attack (TTP) - Start
    # ******************************************************************

    p_base = random.uniform(0, 1)

    p_weather = random.uniform(0, 1)
    p_technology = random.uniform(0, 1)
    p_mechanical = random.uniform(0, 1)
    p_traffic = random.uniform(0, 1)
    p_technical = random.uniform(0, 1)

    cumulativeProbability = 0

    g_overall = digraph()

    incident = None
    generated_scenario_id = None

    mena_countries_list = "'" + "','".join(mena_countries) + "'"

    select_stat_str = "SELECT Incident_id_id, COUNT(*)/(SELECT COUNT(CONCAT(`Fixed_location`, '_', `Fixed_attack_context`, '_', `Fixed_means_of_attack`)) FROM `scenario_awsd_incident`,`scenario_awsd_incident_damage` WHERE `Fixed_location`='" + location + "' AND `Fixed_attack_context`<>'U' AND `Fixed_attack_context`<>'' AND `Fixed_means_of_attack`<>'U' AND `Fixed_means_of_attack`<>'') AS 'probability', `Fixed_location`, `Fixed_attack_context`, `Fixed_means_of_attack`, CONCAT(`Fixed_location`, '_', `Fixed_attack_context`, '_', `Fixed_means_of_attack`) AS 'Scenario' FROM `scenario_awsd_incident`,`scenario_awsd_incident_damage` WHERE `Fixed_location`='" + location + "' AND `Fixed_attack_context`<>'U' AND `Fixed_attack_context`<>'' AND `Fixed_means_of_attack`<>'U' AND `Fixed_means_of_attack`<>'' GROUP BY `Scenario` ORDER BY 'probability';"
    logger.error('The SQL query 1: ' + select_stat_str)

    incidents_qs = list(Awsd_incident_damage.objects.raw(select_stat_str))
    all_levels = len(incidents_qs)
    logger.error('all_levels: '+str(all_levels))
    logger.error('last_mission_score: '+str(last_mission_score))
    logger.error('missionID: ' + str(missionID))

    if missionID > 2: average_score = (last_mission_score + last_mission_score_1 + last_mission_score_2)/3
    elif missionID > 1: average_score = (last_mission_score + last_mission_score_1 ) / 2
    else: average_score = last_mission_score

    last_mission_score_2 = last_mission_score_1
    last_mission_score_1 = last_mission_score

    new_generated_missionID = 0
    if average_score < 50:
        new_generated_missionID = mission_level -1
        logger.error('average_score < 50')
    elif average_score < 60:
        new_generated_missionID = mission_level
        logger.error('average_score < 75')
    elif average_score < 90:
        new_generated_missionID = mission_level + 1
        logger.error('average_score < 95')
    else:
        new_generated_missionID = mission_level + 2
        logger.error('Else')

    if new_generated_missionID < 0:
        new_generated_missionID = 0
        logger.error('new_generated_missionID <= 0')
    if new_generated_missionID >= all_levels - 1:
        new_generated_missionID = all_levels - 1
        logger.error('new_generated_missionID >= all_levels')

    logger.error('mission_level: '+str(mission_level))
    logger.error('new_generated_missionID: ' + str(new_generated_missionID))
    mission_level = new_generated_missionID
    incident = incidents_qs[new_generated_missionID]

    generated_scenario_node_location = incident.Fixed_location.strip()
    generated_scenario_node_attack_context = incident.Fixed_attack_context.strip()
    generated_scenario_node_means_of_attack = incident.Fixed_means_of_attack.strip()

    scenario_location = keys_locations[generated_scenario_node_location]
    scenario_attack_context = keys_attack_contexts[generated_scenario_node_attack_context]
    scenario_means_of_attack = keys_means_of_attacks[generated_scenario_node_means_of_attack]

    # Get a random incident from the selected family of incidents (having the same country, location, attack_context and means_of_attack)
    select_stat_str = "SELECT * FROM `scenario_awsd_incident_damage` WHERE `Fixed_location`='" + generated_scenario_node_location + "' AND `Fixed_attack_context`='" + generated_scenario_node_attack_context + "' AND `Fixed_means_of_attack`='" + generated_scenario_node_means_of_attack + "' ORDER BY RAND(" + str(seed_value) + ")"
    logger.error('The SQL query 2: ' + select_stat_str)

    incident = (Awsd_incident_damage.objects.raw(select_stat_str))[0]
    generated_scenario_id = incident.Incident_id_id

    # Get the related damages
    incident_damage = incident #Awsd_incident_damage.objects.get(id=generated_scenario_id)

    generated_scenario_node_location = incident_damage.Fixed_location.strip()
    generated_scenario_node_attack_context = incident_damage.Fixed_attack_context.strip()
    generated_scenario_node_means_of_attack = incident_damage.Fixed_means_of_attack.strip()

    nodes_base.add(keys_locations[generated_scenario_node_location])
    nodes_base.add(keys_attack_contexts[generated_scenario_node_attack_context])
    nodes_base.add(keys_means_of_attacks[generated_scenario_node_means_of_attack])

    edges_base.add((keys_locations[generated_scenario_node_location],
                       keys_attack_contexts[generated_scenario_node_attack_context]))

    edges_base.add((keys_attack_contexts[generated_scenario_node_attack_context],
                       keys_means_of_attacks[generated_scenario_node_means_of_attack]))

    # ******************************************************************
    # Generate Location / Attack Context / Means of Attack (TTP) - End
    # ******************************************************************

    # natural event start
    the_date = '2000-' + str(current_month) + '-' + str(current_day)
    select_stat_str = "SELECT * FROM `scenario_natural_event` WHERE `Country`='" + country.title() + "' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(seed_value) + ")"
    logger.error('The SQL query 3: ' + select_stat_str)

    natural_event = (Natural_event.objects.raw(select_stat_str))
    if len(list(natural_event)) <= 0:
        select_stat_str = "SELECT * FROM `scenario_natural_event` WHERE `Country`='" + country.title() + "' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(seed_value) + ")"
        logger.error('The SQL query 3a: ' + select_stat_str)
        natural_event = (Natural_event.objects.raw(select_stat_str))
        if len(list(natural_event)) <= 0:
            select_stat_str = "SELECT * FROM `scenario_natural_event` WHERE `Country`='*' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(seed_value) + ")"
            logger.error('The SQL query 3b: ' + select_stat_str)
            natural_event = (Natural_event.objects.raw(select_stat_str))
            if len(list(natural_event)) <= 0:
                select_stat_str = "SELECT * FROM `scenario_natural_event` WHERE `Country`='*' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(seed_value) + ")"
                logger.error('The SQL query 3c: ' + select_stat_str)
                natural_event = (Natural_event.objects.raw(select_stat_str))

    if len(list(natural_event)) > 0:
        # only pick the first natural event and if its probablity falls in the generated uniform probability, otherwise no natural event
        if natural_event[0].Event_probability <= p_weather:
            generated_scenario_node_natural_event = natural_event[0].Description  # 'Storm'
            generated_scenario_node_natural_event_impact = natural_event[0].Impact  # ''

            logger.error('Natural event: ' + str(generated_scenario_node_natural_event))
            logger.error('Natural event impact: ' + str(generated_scenario_node_natural_event_impact))

            nodes_base.add(generated_scenario_node_natural_event)
            edges_base.add((keys_locations[generated_scenario_node_location],generated_scenario_node_natural_event))

            nodes_impact.add(generated_scenario_node_natural_event_impact)
            logger.error('nodes_impact @natural event: ' + str(nodes_impact))

            edges_impact.add((generated_scenario_node_natural_event, generated_scenario_node_natural_event_impact))
            # Natural Event Damages Start
            natural_event_damages_qs = Natural_event_damage.objects.filter(Natural_event_id=natural_event[0].id,Damage_type='*')
            if len(list(natural_event_damages_qs)) > 0:
                damage_probability_min = natural_event_damages_qs[0].Damage_probability_min
                damage_probability_max = natural_event_damages_qs[0].Damage_probability_max
                for Key in damage_probability_by_type_min:
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_natural_event_impact, generated_damage_types[Key]))

            natural_event_damages_qs = Natural_event_damage.objects.filter(Natural_event_id=natural_event[0].id).exclude(Damage_type='*')
            if len(list(natural_event_damages_qs)) > 0:
                for natural_event_damage in natural_event_damages_qs:
                    Key = natural_event_damage.Damage_type
                    damage_probability_min = natural_event_damage.Damage_probability_min
                    damage_probability_max = natural_event_damage.Damage_probability_max
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_natural_event_impact, generated_damage_types[Key]))
            # Natural Event Damages End
    # natural event end

    # technology event start
    select_stat_str = "SELECT * FROM `scenario_technology_event` WHERE `Country`='" + country.title() + "' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(seed_value) + ")"
    logger.error('The SQL query 4: ' + select_stat_str)

    technology_event = (Technology_event.objects.raw(select_stat_str))
    if len(list(technology_event)) <= 0:
        select_stat_str = "SELECT * FROM `scenario_technology_event` WHERE `Country`='" + country.title() + "' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
            seed_value) + ")"
        technology_event = (Technology_event.objects.raw(select_stat_str))
        if len(list(technology_event)) <= 0:
            select_stat_str = "SELECT * FROM `scenario_technology_event` WHERE `Country`='*' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
                seed_value) + ")"
            technology_event = (Technology_event.objects.raw(select_stat_str))
            if len(list(technology_event)) <= 0:
                select_stat_str = "SELECT * FROM `scenario_technology_event` WHERE `Country`='*' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
                    seed_value) + ")"
                technology_event = (Technology_event.objects.raw(select_stat_str))

    if len(list(technology_event)) > 0:
        if technology_event[0].Event_probability <= p_technology:
            generated_scenario_node_technology_event = technology_event[0].Description  # ''
            generated_scenario_node_technology_event_impact = technology_event[0].Impact  # ''

            logger.error('Technology event: ' + str(generated_scenario_node_technology_event))
            logger.error('Technology event impact: ' + str(generated_scenario_node_technology_event_impact))

            nodes_base.add(generated_scenario_node_technology_event)
            edges_base.add((keys_locations[generated_scenario_node_location], generated_scenario_node_technology_event))

            nodes_impact.add(generated_scenario_node_technology_event_impact)
            logger.error('nodes_impact @technology event: ' + str(nodes_impact))

            edges_impact.add((generated_scenario_node_technology_event, generated_scenario_node_technology_event_impact))

            # Technology Event Damages Start
            technology_event_damages_qs = Technology_event_damage.objects.filter(Technology_event_id=technology_event[0].id,Damage_type='*')
            if len(list(technology_event_damages_qs)) > 0:
                damage_probability_min = technology_event_damages_qs[0].Damage_probability_min
                damage_probability_max = technology_event_damages_qs[0].Damage_probability_max
                for Key in damage_probability_by_type_min:
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_technology_event_impact, generated_damage_types[Key]))

            technology_event_damages_qs = Technology_event_damage.objects.filter(Technology_event_id=technology_event[0].id).exclude(Damage_type='*')
            if len(list(technology_event_damages_qs)) > 0:
                for technology_event_damage in technology_event_damages_qs:
                    Key = technology_event_damage.Damage_type
                    damage_probability_min = technology_event_damage.Damage_probability_min
                    damage_probability_max = technology_event_damage.Damage_probability_max
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_technology_event_impact, generated_damage_types[Key]))
            # Technology Event Damages End
    # technology event end

    # Mechanical event start
    select_stat_str = "SELECT * FROM `scenario_mechanical_event` WHERE `Country`='" + country.title() + "' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
        seed_value) + ")"
    logger.error('The SQL query 5: ' + select_stat_str)

    mechanical_event = (Mechanical_event.objects.raw(select_stat_str))
    if len(list(mechanical_event)) <= 0:
        select_stat_str = "SELECT * FROM `scenario_mechanical_event` WHERE `Country`='" + country.title() + "' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
            seed_value) + ")"
        mechanical_event = (Mechanical_event.objects.raw(select_stat_str))
        if len(list(mechanical_event)) <= 0:
            select_stat_str = "SELECT * FROM `scenario_mechanical_event` WHERE `Country`='*' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
                seed_value) + ")"
            mechanical_event = (Mechanical_event.objects.raw(select_stat_str))
            if len(list(mechanical_event)) <= 0:
                select_stat_str = "SELECT * FROM `scenario_mechanical_event` WHERE `Country`='*' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
                    seed_value) + ")"
                mechanical_event = (Mechanical_event.objects.raw(select_stat_str))

    if len(list(mechanical_event)) > 0:
        if mechanical_event[0].Event_probability <= p_mechanical:
            generated_scenario_node_mechanical_event = mechanical_event[0].Description  # ''
            generated_scenario_node_mechanical_event_impact = mechanical_event[0].Impact  # ''

            logger.error('Mechanical event: ' + str(generated_scenario_node_mechanical_event))
            logger.error('Mechanical event impact: ' + str(generated_scenario_node_mechanical_event_impact))

            nodes_base.add(generated_scenario_node_mechanical_event)
            edges_base.add((keys_locations[generated_scenario_node_location], generated_scenario_node_mechanical_event))

            nodes_impact.add(generated_scenario_node_mechanical_event_impact)
            logger.error('nodes_impact @mechanical event: ' + str(nodes_impact))

            edges_impact.add((generated_scenario_node_mechanical_event, generated_scenario_node_mechanical_event_impact))

            # mechanical Event Damages Start
            mechanical_event_damages_qs = Mechanical_event_damage.objects.filter(Mechanical_event_id=mechanical_event[0].id,Damage_type='*')
            if len(list(mechanical_event_damages_qs)) > 0:
                damage_probability_min = mechanical_event_damages_qs[0].Damage_probability_min
                damage_probability_max = mechanical_event_damages_qs[0].Damage_probability_max
                for Key in damage_probability_by_type_min:
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_mechanical_event_impact, generated_damage_types[Key]))

            mechanical_event_damages_qs = Mechanical_event_damage.objects.filter(Mechanical_event_id=mechanical_event[0].id).exclude(Damage_type='*')
            if len(list(mechanical_event_damages_qs)) > 0:
                for mechanical_event_damage in mechanical_event_damages_qs:
                    Key = mechanical_event_damage.Damage_type
                    damage_probability_min = mechanical_event_damage.Damage_probability_min
                    damage_probability_max = mechanical_event_damage.Damage_probability_max
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_mechanical_event_impact, generated_damage_types[Key]))
            # mechanical Event Damages End
    # mechanical event end

    # traffic event start
    select_stat_str = "SELECT * FROM `scenario_traffic_event` WHERE `Country`='" + country.title() + "' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
        seed_value) + ")"
    logger.error('The SQL query 6: ' + select_stat_str)

    traffic_event = (Traffic_event.objects.raw(select_stat_str))
    if len(list(traffic_event)) <= 0:
        select_stat_str = "SELECT * FROM `scenario_traffic_event` WHERE `Country`='" + country.title() + "' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
            seed_value) + ")"
        traffic_event = (Traffic_event.objects.raw(select_stat_str))
        if len(list(traffic_event)) <= 0:
            select_stat_str = "SELECT * FROM `scenario_traffic_event` WHERE `Country`='*' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
                seed_value) + ")"
            traffic_event = (Traffic_event.objects.raw(select_stat_str))
            if len(list(traffic_event)) <= 0:
                select_stat_str = "SELECT * FROM `scenario_traffic_event` WHERE `Country`='*' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
                    seed_value) + ")"
                traffic_event = (Traffic_event.objects.raw(select_stat_str))

    if len(list(traffic_event)) > 0:
        if traffic_event[0].Event_probability <= p_traffic:
            generated_scenario_node_traffic_event = traffic_event[0].Description  # ''
            generated_scenario_node_traffic_event_impact = traffic_event[0].Impact  # ''

            logger.error('Traffic event: ' + str(generated_scenario_node_traffic_event))
            logger.error('Traffic event impact: ' + str(generated_scenario_node_traffic_event_impact))

            nodes_base.add(generated_scenario_node_traffic_event)
            edges_base.add((keys_locations[generated_scenario_node_location],generated_scenario_node_traffic_event))

            nodes_impact.add(generated_scenario_node_traffic_event_impact)
            logger.error('nodes_impact @traffic event: ' + str(nodes_impact))

            edges_impact.add((generated_scenario_node_traffic_event, generated_scenario_node_traffic_event_impact))
            # traffic Event Damages Start
            traffic_event_damages_qs = Traffic_event_damage.objects.filter(Traffic_event_id=traffic_event[0].id,Damage_type='*')
            if len(list(traffic_event_damages_qs)) > 0:
                damage_probability_min = traffic_event_damages_qs[0].Damage_probability_min
                damage_probability_max = traffic_event_damages_qs[0].Damage_probability_max
                for Key in damage_probability_by_type_min:
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_traffic_event_impact, generated_damage_types[Key]))

            traffic_event_damages_qs = Traffic_event_damage.objects.filter(Traffic_event_id=traffic_event[0].id).exclude(Damage_type='*')
            if len(list(traffic_event_damages_qs)) > 0:
                for traffic_event_damage in traffic_event_damages_qs:
                    Key = traffic_event_damage.Damage_type
                    damage_probability_min = traffic_event_damage.Damage_probability_min
                    damage_probability_max = traffic_event_damage.Damage_probability_max
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_traffic_event_impact, generated_damage_types[Key]))
            # traffic Event Damages End
    # traffic event end

    # technical event start
    select_stat_str = "SELECT * FROM `scenario_technical_event` WHERE `Country`='" + country.title() + "' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
        seed_value) + ")"
    logger.error('The SQL query 7: ' + select_stat_str)

    technical_event = (Technical_event.objects.raw(select_stat_str))
    if len(list(technical_event)) <= 0:
        select_stat_str = "SELECT * FROM `scenario_technical_event` WHERE `Country`='" + country.title() + "' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
            seed_value) + ")"
        technical_event = (Technical_event.objects.raw(select_stat_str))
        if len(list(technical_event)) <= 0:
            select_stat_str = "SELECT * FROM `scenario_technical_event` WHERE `Country`='*' AND `Location`='" + generated_scenario_node_location + "' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
                seed_value) + ")"
            technical_event = (Technical_event.objects.raw(select_stat_str))
            if len(list(technical_event)) <= 0:
                select_stat_str = "SELECT * FROM `scenario_technical_event` WHERE `Country`='*' AND `Location`='*' AND ((DATE_FORMAT(`From_date`, '%%m-%%d') <= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') >= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') < DATE_FORMAT(`To_date`, '%%m-%%d')) OR (DATE_FORMAT(`From_date`, '%%m-%%d') >= DATE_FORMAT( '" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`To_date`, '%%m-%%d') <= DATE_FORMAT('" + the_date + "', '%%m-%%d') AND DATE_FORMAT(`From_date`, '%%m-%%d') > DATE_FORMAT(`To_date`, '%%m-%%d')) ) ORDER BY RAND(" + str(
                    seed_value) + ")"
                technical_event = (Technical_event.objects.raw(select_stat_str))

    if len(list(technical_event)) > 0:
        if technical_event[0].Event_probability <= p_technical:
            generated_scenario_node_technical_event = technical_event[0].Description  # ''
            generated_scenario_node_technical_event_impact = technical_event[0].Impact  # ''

            logger.error('Technical event: ' + str(generated_scenario_node_technical_event))
            logger.error('Technical event impact: ' + str(generated_scenario_node_technical_event_impact))

            nodes_base.add(generated_scenario_node_technical_event)
            edges_base.add((keys_locations[generated_scenario_node_location],generated_scenario_node_technical_event))

            nodes_impact.add(generated_scenario_node_technical_event_impact)
            logger.error('nodes_impact @technical event: ' + str(nodes_impact))

            edges_impact.add(
                (generated_scenario_node_technical_event, generated_scenario_node_technical_event_impact))
            # technical Event Damages Start
            technical_event_damages_qs = Technical_event_damage.objects.filter(Technical_event_id=technical_event[0].id,Damage_type='*')
            if len(list(technical_event_damages_qs)) > 0:
                damage_probability_min = technical_event_damages_qs[0].Damage_probability_min
                damage_probability_max = technical_event_damages_qs[0].Damage_probability_max
                for Key in damage_probability_by_type_min:
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_technical_event_impact, generated_damage_types[Key]))

            technical_event_damages_qs = Technical_event_damage.objects.filter(Technical_event_id=technical_event[0].id).exclude(Damage_type='*')
            if len(list(technical_event_damages_qs)) > 0:
                for technical_event_damage in technical_event_damages_qs:
                    Key = technical_event_damage.Damage_type
                    damage_probability_min = technical_event_damage.Damage_probability_min
                    damage_probability_max = technical_event_damage.Damage_probability_max
                    if damage_probability_by_type_min[Key] < damage_probability_min: damage_probability_by_type_min[Key] = damage_probability_min
                    if damage_probability_by_type_max[Key] < damage_probability_max: damage_probability_by_type_max[Key] = damage_probability_max

                    if damage_probability_max > 0:
                        generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                        #if not generated_damage_types[Key] in nodes_damage:
                        nodes_damage.add(generated_damage_types[Key])
                        edges_damage.add((generated_scenario_node_technical_event_impact, generated_damage_types[Key]))

            logger.error('nodes_damage @technical event: ' + str(nodes_damage))
            logger.error('edges_damage @technical event: ' + str(edges_damage))
            # technical Event Damages End
    # technical event end


    # ******************************************************************
    # Generate Impact - Start
    # ******************************************************************
    possible_impacts = Impact.objects.filter(Location=generated_scenario_node_location,
                                             Attack_context=generated_scenario_node_attack_context,
                                             Means_of_attack=generated_scenario_node_means_of_attack)
    if not possible_impacts:
        possible_impacts = Impact.objects.filter(Location=generated_scenario_node_location,
                                                 Attack_context=generated_scenario_node_attack_context,
                                                 Means_of_attack='*')
        if not possible_impacts:
            possible_impacts = Impact.objects.filter(Location=generated_scenario_node_location, Attack_context='*',
                                                     Means_of_attack='*')
            if not possible_impacts:
                possible_impacts = Impact.objects.filter(Location='*', Attack_context='*', Means_of_attack='*')

    p_impact = random.uniform(0, 1)

    impact = None
    generated_impact_id = None
    cumulativeProbability = 0

    for impact in possible_impacts:
        cumulativeProbability = cumulativeProbability + impact.Impact_probability
        if p_impact <= cumulativeProbability:
            generated_scenario_node_impact = impact.Impact
            generated_impact_id = impact.id
            cumulativeProbability = 0
            break

    nodes_impact.add(generated_scenario_node_impact)
    logger.error('nodes_impact @security event: ' + str(nodes_impact))

    edges_impact.add((keys_means_of_attacks[generated_scenario_node_means_of_attack], generated_scenario_node_impact))
    # ******************************************************************
    # Generate Impact - End
    # ******************************************************************


    # ******************************************************************
    # Generate Damage - Start
    # ******************************************************************
    # initilaise damage random numbers with the * value
    # damage_w is wildcard damage (unspecified type of damage).
    # this will be used whenever certain type of damage is present in scenario,
    # however there is no recordeed values for it in the database
    damage_w = None

    try:
        damage_w = Damage.objects.get(Impact_id=generated_impact_id, Damage_type='*')
        damage_w = {
            'Damage_probability_min': damage_w.Damage_probability_min,
            'Damage_probability_max': damage_w.Damage_probability_max,
        }
    except Damage.DoesNotExist:
        damage_w = {
            'Damage_probability_min': 0,
            'Damage_probability_max': 1,
        }
    # ******************************************************************
    # Decide the damage values per damage type - Start
    # ******************************************************************

    # damage_x refers to a specific type of damage.
    # this will be used whenever certain type of damage is present in scenario,
    # however there is no recordeed values for it in the database

    damage_x = None
    if incident.Total_kidnapped > 0:
        Key = 'K'
        # nodes_damage.add(generated_damage_types[Key])
        # edges_damage.add((generated_scenario_node_impact, generated_damage_types[Key]))
        try:
            damage_x = Damage.objects.get(Impact_id=generated_impact_id, Damage_type=Key)
            if damage_probability_by_type_min[Key] < damage_x.Damage_probability_min: damage_probability_by_type_min[Key] = damage_x.Damage_probability_min
            if damage_probability_by_type_max[Key] < damage_x.Damage_probability_max: damage_probability_by_type_max[Key] = damage_x.Damage_probability_max
            if damage_x.Damage_probability_max > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
        except Damage.DoesNotExist:
            if damage_probability_by_type_min[Key] < damage_w['Damage_probability_min']: damage_probability_by_type_min[Key] = damage_w['Damage_probability_min']
            if damage_probability_by_type_max[Key] < damage_w['Damage_probability_max']: damage_probability_by_type_max[Key] = damage_w['Damage_probability_max']
            if damage_w['Damage_probability_max'] > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
    if incident.Total_wounded > 0:
        Key = 'W'
        try:
            damage_x = Damage.objects.get(Impact_id=generated_impact_id, Damage_type=Key)
            if damage_probability_by_type_min[Key] < damage_x.Damage_probability_min: damage_probability_by_type_min[
                Key] = damage_x.Damage_probability_min
            if damage_probability_by_type_max[Key] < damage_x.Damage_probability_max: damage_probability_by_type_max[
                Key] = damage_x.Damage_probability_max
            if damage_x.Damage_probability_max > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
        except Damage.DoesNotExist:
            if damage_probability_by_type_min[Key] < damage_w['Damage_probability_min']: damage_probability_by_type_min[Key] = damage_w['Damage_probability_min']
            if damage_probability_by_type_max[Key] < damage_w['Damage_probability_max']: damage_probability_by_type_max[Key] = damage_w['Damage_probability_max']
            if damage_w['Damage_probability_max'] > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
    if incident_damage.RSA > 0:
        Key = 'RSA'
        try:
            damage_x = Damage.objects.get(Impact_id=generated_impact_id, Damage_type=Key)
            if damage_probability_by_type_min[Key] < damage_x.Damage_probability_min: damage_probability_by_type_min[
                Key] = damage_x.Damage_probability_min
            if damage_probability_by_type_max[Key] < damage_x.Damage_probability_max: damage_probability_by_type_max[
                Key] = damage_x.Damage_probability_max
            if damage_x.Damage_probability_max > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
        except Damage.DoesNotExist:
            if damage_probability_by_type_min[Key] < damage_w['Damage_probability_min']: damage_probability_by_type_min[Key] = damage_w['Damage_probability_min']
            if damage_probability_by_type_max[Key] < damage_w['Damage_probability_max']: damage_probability_by_type_max[Key] = damage_w['Damage_probability_max']
            if damage_w['Damage_probability_max'] > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
    if incident.Total_killed > 0:
        Key = 'KK'
        try:
            damage_x = Damage.objects.get(Impact_id=generated_impact_id, Damage_type=Key)
            if damage_probability_by_type_min[Key] < damage_x.Damage_probability_min: damage_probability_by_type_min[
                Key] = damage_x.Damage_probability_min
            if damage_probability_by_type_max[Key] < damage_x.Damage_probability_max: damage_probability_by_type_max[
                Key] = damage_x.Damage_probability_max
            if damage_x.Damage_probability_max > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
        except Damage.DoesNotExist:
            if damage_probability_by_type_min[Key] < damage_w['Damage_probability_min']: damage_probability_by_type_min[Key] = damage_w['Damage_probability_min']
            if damage_probability_by_type_max[Key] < damage_w['Damage_probability_max']: damage_probability_by_type_max[Key] = damage_w['Damage_probability_max']
            if damage_w['Damage_probability_max'] > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
    if incident_damage.V == 1:
        Key = 'V'
        try:
            damage_x = Damage.objects.get(Impact_id=generated_impact_id, Damage_type=Key)
            if damage_probability_by_type_min[Key] < damage_x.Damage_probability_min: damage_probability_by_type_min[
                Key] = damage_x.Damage_probability_min
            if damage_probability_by_type_max[Key] < damage_x.Damage_probability_max: damage_probability_by_type_max[
                Key] = damage_x.Damage_probability_max
            if damage_x.Damage_probability_max > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
        except Damage.DoesNotExist:
            if damage_probability_by_type_min[Key] < damage_w['Damage_probability_min']: damage_probability_by_type_min[Key] = damage_w['Damage_probability_min']
            if damage_probability_by_type_max[Key] < damage_w['Damage_probability_max']: damage_probability_by_type_max[Key] = damage_w['Damage_probability_max']
            if damage_w['Damage_probability_max'] > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
    if incident_damage.E == 1:
        Key = 'E'
        try:
            damage_x = Damage.objects.get(Impact_id=generated_impact_id, Damage_type=Key)
            if damage_probability_by_type_min[Key] < damage_x.Damage_probability_min: damage_probability_by_type_min[
                Key] = damage_x.Damage_probability_min
            if damage_probability_by_type_max[Key] < damage_x.Damage_probability_max: damage_probability_by_type_max[
                Key] = damage_x.Damage_probability_max
            if damage_x.Damage_probability_max > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
        except Damage.DoesNotExist:
            if damage_probability_by_type_min[Key] < damage_w['Damage_probability_min']: damage_probability_by_type_min[Key] = damage_w['Damage_probability_min']
            if damage_probability_by_type_max[Key] < damage_w['Damage_probability_max']: damage_probability_by_type_max[Key] = damage_w['Damage_probability_max']
            if damage_w['Damage_probability_max'] > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
    if incident_damage.C == 1:
        Key = 'C'
        try:
            damage_x = Damage.objects.get(Impact_id=generated_impact_id, Damage_type=Key)
            if damage_probability_by_type_min[Key] < damage_x.Damage_probability_min: damage_probability_by_type_min[
                Key] = damage_x.Damage_probability_min
            if damage_probability_by_type_max[Key] < damage_x.Damage_probability_max: damage_probability_by_type_max[
                Key] = damage_x.Damage_probability_max
            if damage_x.Damage_probability_max > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
        except Damage.DoesNotExist:
            if damage_probability_by_type_min[Key] < damage_w['Damage_probability_min']: damage_probability_by_type_min[Key] = damage_w['Damage_probability_min']
            if damage_probability_by_type_max[Key] < damage_w['Damage_probability_max']: damage_probability_by_type_max[Key] = damage_w['Damage_probability_max']
            if damage_w['Damage_probability_max'] > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
    if incident_damage.B == 1:
        Key = 'B'
        try:
            damage_x = Damage.objects.get(Impact_id=generated_impact_id, Damage_type=Key)
            if damage_probability_by_type_min[Key] < damage_x.Damage_probability_min: damage_probability_by_type_min[
                Key] = damage_x.Damage_probability_min
            if damage_probability_by_type_max[Key] < damage_x.Damage_probability_max: damage_probability_by_type_max[
                Key] = damage_x.Damage_probability_max
            if damage_x.Damage_probability_max > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))
        except Damage.DoesNotExist:
            if damage_probability_by_type_min[Key] < damage_w['Damage_probability_min']: damage_probability_by_type_min[Key] = damage_w['Damage_probability_min']
            if damage_probability_by_type_max[Key] < damage_w['Damage_probability_max']: damage_probability_by_type_max[Key] = damage_w['Damage_probability_max']
            if damage_w['Damage_probability_max'] > 0:
                generated_damage_types[Key] = keys_damage_types_wo_u[Key]
                generated_scenario_node_damage[Key] = generated_damage_types[Key]
                nodes_damage.add(generated_scenario_node_damage[Key])
                # here we connect the damage types with the impact, we need to connect the generated_scenario_node_natural_event with the corrsponding damage types too.........
                edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage[Key]))

    if 'K' in generated_damage_types:
        damage_probability_by_type['K'] = random.uniform(damage_probability_by_type_min['K'], damage_probability_by_type_max['K'])
    else:
        damage_probability_by_type['K'] = 0
    if 'W' in generated_damage_types:
        damage_probability_by_type['W'] = random.uniform(damage_probability_by_type_min['W'], damage_probability_by_type_max['W'])
    else:
        damage_probability_by_type['W'] = 0
    if 'RSA' in generated_damage_types:
        damage_probability_by_type['RSA'] = random.uniform(damage_probability_by_type_min['RSA'], damage_probability_by_type_max['RSA'])
    else:
        damage_probability_by_type['RSA'] = 0
    if 'KK' in generated_damage_types:
        ############
        # how does p_krsaw affect KK --> min and max
        ############
        # intersection of K and RSA and W
        p_k_rsa_w = random.uniform(0, min(damage_probability_by_type['K'], damage_probability_by_type['W'], damage_probability_by_type['RSA']))
        # intersection of K and RSA
        p_k_rsa = random.uniform(0, min(damage_probability_by_type['K'], damage_probability_by_type['RSA']))
        # intersection of K and W
        p_k_w = random.uniform(0, min(damage_probability_by_type['K'], damage_probability_by_type['W']))
        # intersection of RSA and W
        p_rsa_w = random.uniform(0, min(damage_probability_by_type['RSA'], damage_probability_by_type['W']))
        # union of K and RSA and W
        p_krsaw = damage_probability_by_type['K'] + damage_probability_by_type['RSA'] + damage_probability_by_type['W'] + p_k_rsa_w - p_k_rsa - p_k_w - p_rsa_w
        if p_krsaw == 0:
            damage_probability_by_type['KK'] = random.uniform(damage_probability_by_type_min['KK'], damage_probability_by_type_max['KK'])
        else:
            damage_probability_by_type['KK'] = max(1 - p_krsaw, 0)  # what is left but not negative
    else:
        damage_probability_by_type['KK'] = 0
    if 'V' in generated_damage_types:
        damage_probability_by_type['V'] = random.uniform(damage_probability_by_type_min['V'], damage_probability_by_type_max['V'])
    else:
        damage_probability_by_type['V'] = 0
    if 'E' in generated_damage_types:
        damage_probability_by_type['E'] = random.uniform(damage_probability_by_type_min['E'], damage_probability_by_type_max['E'])
    else:
        damage_probability_by_type['E'] = 0
    if 'C' in generated_damage_types:
        damage_probability_by_type['C'] = random.uniform(damage_probability_by_type_min['C'], damage_probability_by_type_max['C'])
    else:
        damage_probability_by_type['C'] = 0
    if 'B' in generated_damage_types:
        damage_probability_by_type['B'] = random.uniform(damage_probability_by_type_min['B'], damage_probability_by_type_max['B'])
    else:
        damage_probability_by_type['B'] = 0
    # ******************************************************************
    # Decide the damage values per damage type - End
    # ******************************************************************


    if all(x == 0 for x in list(damage_probability_by_type.values())):
        generated_scenario_node_damage['*'] = 'No damage'
        nodes_damage.add(generated_scenario_node_damage['*'])
        edges_damage.add((generated_scenario_node_impact, generated_scenario_node_damage['*']))
    # ******************************************************************
    # Generate Damage - End
    # ******************************************************************


    # ******************************************************************
    # Generate Overall Graph - Start
    # ******************************************************************
    with g_overall.subgraph(name='clusterBase') as g_base:
        add_nodes(g_base, nodes_base)
        add_edges(g_base, edges_base)
        apply_styles(g_base, styles_base)

    with g_overall.subgraph(name='clusterImpact') as g_impact:
        logger.error('nodes_impact @ the end: ' + str(nodes_impact))
        add_nodes(g_impact, nodes_impact)
        apply_styles(g_impact, styles_impact)

    add_edges(g_overall, edges_impact)

    with g_overall.subgraph(name='clusterDamage') as g_damage:
        add_nodes(g_damage, nodes_damage)
        apply_styles(g_damage, styles_damage)

    add_edges(g_overall, edges_damage)

    apply_styles(g_overall, styles_overall)

    scenario_svg = g_overall.pipe(format='svg')
    scenario_svg = str(scenario_svg)
    svg_s_pos = scenario_svg.find('<svg')
    svg_e_pos = scenario_svg.find('</svg>') + 6
    scenario_svg = scenario_svg[svg_s_pos:svg_e_pos]

    # ******************************************************************
    # Generate Overall Graph - End
    # ******************************************************************


    # ******************************************************************
    # Find all SOPs and Policies related to the current situation (Scenario Unit)- Start
    # ******************************************************************
    sops_policies_qs = Sop_policy.objects.filter(Location=generated_scenario_node_location,
                                              Attack_context=generated_scenario_node_attack_context,
                                              Means_of_attack=generated_scenario_node_means_of_attack)
    if not sops_policies_qs :
        sops_policies_qs = Sop_policy.objects.filter(Location=generated_scenario_node_location,
                                                  Attack_context=generated_scenario_node_attack_context,
                                                  Means_of_attack='*')
        if not sops_policies_qs :
            sops_policies_qs = Sop_policy.objects.filter(Location=generated_scenario_node_location,
                                                      Attack_context='*',
                                                      Means_of_attack='*')
            if not sops_policies_qs :
                sops_policies_qs = Sop_policy.objects.filter(Location='*',
                                                          Attack_context='*',
                                                          Means_of_attack='*')

    sops_policies_precautionary_strategic = []
    sops_policies_precautionary_tactical = []
    sops_policies_precautionary_operational = []

    sops_policies_adaptive_strategic = []
    sops_policies_adaptive_tactical = []
    sops_policies_adaptive_operational = []

    total_damage_mitigation_fraction = keys_damage_types_wo_u.fromkeys(list(keys_damage_types_wo_u.keys()),
                                                                      0)  # {'KK': 0, 'K': 0, 'W': 0, 'RSA': 0, 'B': 0, 'V': 0, 'C': 0, 'E': 0}

    sops_policies_list = []

    # For each SOP or Policy found related to the current situation ...
    for sop_policy in sops_policies_qs:
        # Find all damage types mitigated by this SOP/Policy
        sop_policy_damage_mitigations_qs = Sop_policy_damage_mitigation.objects.filter(Sop_policy_id=sop_policy.id)
        sops_policies_list.append({
            'id': sop_policy.id,
            'Measure_description': sop_policy.Measure_family+" > "+sop_policy.Measure_type+" > "+sop_policy.Measure_description,
            'Prerequesit_sop_policy': sop_policy.Prerequesit_sop_policy,
            'Ds_level': sop_policy.Ds_level,
            'Implementation_stage': sop_policy.Implementation_stage,
            'Damage_mitigation_fraction_by_type': keys_damage_types_wo_u.fromkeys(list(keys_damage_types_wo_u.keys()), 0),
        })

        # For each damage type mitigated by this SOP or Policy ...
        for sop_policy_damage_mitigation in sop_policy_damage_mitigations_qs:
            if sop_policy_damage_mitigation.Damage_type is not '*':
                # sum all mitigation fractions per damage type (based on damage type)
                total_damage_mitigation_fraction[
                    sop_policy_damage_mitigation.Damage_type] += sop_policy_damage_mitigation.Damage_mitigation_fraction
                # edit the last added object
                sops_policies_list[-1]['Damage_mitigation_fraction_by_type'][
                    sop_policy_damage_mitigation.Damage_type] = sop_policy_damage_mitigation.Damage_mitigation_fraction
            else:
                for key in total_damage_mitigation_fraction:
                    # sum all mitigation fractions per damage type (based on damage type)
                    total_damage_mitigation_fraction[key] += sop_policy_damage_mitigation.Damage_mitigation_fraction
                    # edit the last added object
                    sops_policies_list[-1]['Damage_mitigation_fraction_by_type'][
                        key] = sop_policy_damage_mitigation.Damage_mitigation_fraction

    # Create the checkbox for SOPs and Policies
    # increase the total so that mitigation is not 100%
    for key in total_damage_mitigation_fraction:
        total_damage_mitigation_fraction[key] *= 1 + random.uniform(0, 1)

    for sop_policy in sops_policies_list:
        if sop_policy['Ds_level'] == 'S' and sop_policy['Implementation_stage'] == 'P':
            sops_policies_precautionary_strategic.append(sop_policy)
        if sop_policy['Ds_level'] == 'T' and sop_policy['Implementation_stage'] == 'P':
            sops_policies_precautionary_tactical.append(sop_policy)
        if sop_policy['Ds_level'] == 'O' and sop_policy['Implementation_stage'] == 'P':
            sops_policies_precautionary_operational.append(sop_policy)
        if sop_policy['Ds_level'] == 'S' and sop_policy['Implementation_stage'] == 'A':
            sops_policies_adaptive_strategic.append(sop_policy)
        if sop_policy['Ds_level'] == 'T' and sop_policy['Implementation_stage'] == 'A':
            sops_policies_adaptive_tactical.append(sop_policy)
        if sop_policy['Ds_level'] == 'O' and sop_policy['Implementation_stage'] == 'A':
            sops_policies_adaptive_operational.append(sop_policy)

    sops_policies['sops_policies_precautionary_strategic'] = sops_policies_precautionary_strategic
    sops_policies['sops_policies_precautionary_tactical'] = sops_policies_precautionary_tactical
    sops_policies['sops_policies_precautionary_operational'] = sops_policies_precautionary_operational
    sops_policies['sops_policies_adaptive_strategic'] = sops_policies_adaptive_strategic
    sops_policies['sops_policies_adaptive_tactical'] = sops_policies_adaptive_tactical
    sops_policies['sops_policies_adaptive_operational'] = sops_policies_adaptive_operational
    scenario_total_damage_mitigation_fraction_by_type = total_damage_mitigation_fraction

    # ******************************************************************
    # find sops and policies - End
    # ******************************************************************


    # ******************************************************************
    # Find city/ies and attacker - Start
    # ******************************************************************
    city_A = {'city_name': '', 'lat': 0, 'lng': 0, 'get_bbox': [0, 0, 0, 0], }
    city_B = {'city_name': '', 'lat': 0, 'lng': 0, 'get_bbox': [0, 0, 0, 0], }
    zoom = 11
    size = float(str(180.0 / (2 ** zoom + 1)))

    select_stat_str = "SELECT * FROM `scenario_city_attacker` WHERE `Country`='" + country.title() + "' ORDER BY RAND(" + str(seed_value) + ")"
    logger.error('The SQL query 8: ' + select_stat_str)

    cities = City_location.objects.raw(select_stat_str)

    i = 0
    for city in cities:
        i += 1
        try:
            n = city.City.strip()
            x = float(city.Latitude)
            y = float(city.Longitude)

            if ((x and y and n) is not "") and ((x and y and n) is not None) and "unknown" not in n.lower():
                city_A['city_name'] = n
                city_A['lat'] = x
                city_A['lng'] = y
                city_A['get_bbox'] = [y - size, x - size, y + size, x + size]
                scenario_attackers_group_name = city.Gname
                break
        except ValueError:
            pass

    scenario_cities = [city_A]

    # if location is Road, then we need another city (destination)
    if location == 'R':
        city_B['city_name'] = n = cities[i].City.strip()
        city_B['lat'] = x = float(cities[i].Latitude)
        city_B['lng'] = y = float(cities[i].Longitude)
        city_B['get_bbox'] = [y - size, x - size, y + size, x + size]

        for city in cities[i:]:
            i += 1
            if ((x and y and n) is not "") and ((x and y and n) is not None) and "unknown" not in n.lower().strip() and cities[i].City.lower().strip() is not city_A['city_name'].lower().strip():
                city_B['city_name'] = n = cities[i].City.strip()
                city_B['lat'] = x = float(cities[i].Latitude)
                city_B['lng'] = y = float(cities[i].Longitude)
                city_B['get_bbox'] = [y - size, x - size, y + size, x + size]
                break

        for city in cities[i:]:
            try:
                n = city.City.strip()
                x = float(city.Latitude)
                y = float(city.Longitude)

                if ((x and y and n) is not "") and ((x and y and n) is not None) and "unknown" not in n.lower().strip():
                    d = dis_bet_cities(x, city_A['lat'], y, city_A['lng'])
                    logger.error('distance between cities:' + str(d))
                    if 300 < d < 1000:
                        city_B['city_name'] = n
                        city_B['lat'] = x
                        city_B['lng'] = y
                        city_B['get_bbox'] = [y - size, x - size, y + size, x + size]
                        break
            except ValueError:
                pass

        scenario_cities.append(city_B)
    # ******************************************************************
    # Find city/ies and attacker - End
    # ******************************************************************


    return scenario_location, scenario_attack_context, scenario_means_of_attack, scenario_attackers_group_name, scenario_cities, scenario_total_damage_mitigation_fraction_by_type, sops_policies, scenario_svg, damage_probability_by_type, mission_level, all_levels, last_mission_score_1, last_mission_score_2
    # Main function - End