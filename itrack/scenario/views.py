from django.shortcuts import render
from django.http import HttpResponse

from .models import Mission_default

import random
import sys
from datetime import datetime
import json
from django.http import JsonResponse

from scenario.scenario_module import generate_scenario_module

# import the logging library
    import logging

countries = ['syria','iraq','yemen',]

locations = ['H','OC','PS','P','R','C',]

days_31 = [1, 3, 5, 7, 8, 10, 12]
days_30 = [4, 6, 9, 11]
days_29 = [2]

#Views - Start

#Scenario View - Start
def scenario_gen(request):
    logger = logging.getLogger(__name__)

    teamID = int(request.GET.get('teamID', 0))
    missionID = int(request.GET.get('missionID', 0))
    mission_level = int(request.GET.get('mission_level', 0))

    logger.error('views mission_level: '+str(mission_level))

    last_mission_score = int(request.GET.get('last_mission_score', 0))
    last_mission_score_1 = int(request.GET.get('last_mission_score_1', 0))
    last_mission_score_2 = int(request.GET.get('last_mission_score_2', 0))
    seed_value = int(request.GET.get('seed_value', random.randrange(sys.maxsize)))
    random.seed(seed_value)
    next_seed_value = random.randrange(sys.maxsize)
    location = str(request.GET.get('location')).upper()
    if location not in locations: location = random.choice(locations)
    country = str(request.GET.get('country')).lower()
    if country not in countries: country = random.choice(countries)
    current_day = int(request.GET.get('day', datetime.now().day))
    current_month = int(request.GET.get('month', datetime.now().month))

    if current_month < 1:current_month = 1
    if current_month > 12: current_month = 12

    if current_day < 1: current_day = 1
    if (current_day > 29) and (current_month in days_29): current_day = 29
    if (current_day > 30) and (current_month in days_30): current_day = 30
    if (current_day > 31) and (current_month in days_31): current_day = 31

    context = {}
    #sops_policies, scenario_svg, p_base, p_impact, damage_probability_by_type, generated_scenario_id, testVar, mission_level, last_mission_score_1, last_mission_score_2 = generate_scenario_module(missionID, mission_level, last_mission_score, last_mission_score_1, last_mission_score_2, seed_value, country, location, current_day, current_month)
    scenario_location, scenario_attack_context, scenario_means_of_attack, scenario_attackers_group_name, scenario_cities, scenario_total_damage_mitigation_fraction_by_type, sops_policies, scenario_svg, damage_probability_by_type, mission_level, all_levels, last_mission_score_1, last_mission_score_2  = generate_scenario_module(missionID, mission_level, last_mission_score, last_mission_score_1, last_mission_score_2, seed_value, country, location, current_day, current_month)

    context['teamID'] = teamID
    context['missionID'] = missionID
    context['mission_level'] = mission_level
    context['all_levels'] = all_levels
    context['last_mission_score_1'] = last_mission_score_1
    context['last_mission_score_2'] = last_mission_score_2
    context['seed_value'] = seed_value
    context['next_seed_value'] = next_seed_value
    context['scenario_svg'] = scenario_svg
    context['sops_policies'] = sops_policies

    context['damage_probability_by_type'] = damage_probability_by_type

    context['scenario_location'] = scenario_location
    context['scenario_attack_context'] = scenario_attack_context
    context['scenario_means_of_attack'] = scenario_means_of_attack
    context['scenario_attackers_group_name'] = scenario_attackers_group_name
    context['scenario_cities'] = scenario_cities
    context['scenario_total_damage_mitigation_fraction_by_type'] = scenario_total_damage_mitigation_fraction_by_type

    #return HttpResponse(json.dumps(context),content_type="application/json")
    #return HttpResponse(context, content_type="application/json")
    return JsonResponse(context)
#Scenario View - End


#Scenario View - Start
def scenario_api(request):
    logger = logging.getLogger(__name__)

    last_mission_level = int(request.GET.get('last_mission_level', 0))

    logger.error('views last_mission_level: '+str(last_mission_level))

    mean_score = int(request.GET.get('mean_score', 0))
    seed_value = int(request.GET.get('seed_value', random.randrange(sys.maxsize)))
    #### random.seed(seed_value)
    #### next_seed_value = random.randrange(sys.maxsize)
    location = str(request.GET.get('location')).upper()
    if location not in locations: location = random.choice(locations)
    country = str(request.GET.get('country')).lower()
    if country not in countries: country = random.choice(countries)
    current_day = int(request.GET.get('day', datetime.now().day))
    current_month = int(request.GET.get('month', datetime.now().month))

    if current_month < 1:current_month = 1
    if current_month > 12: current_month = 12

    if current_day < 1: current_day = 1
    if (current_day > 29) and (current_month in days_29): current_day = 29
    if (current_day > 30) and (current_month in days_30): current_day = 30
    if (current_day > 31) and (current_month in days_31): current_day = 31

    context = {}
    #sops_policies, scenario_svg, p_base, p_impact, damage_probability_by_type, generated_scenario_id, testVar, mission_level, last_mission_score_1, last_mission_score_2 = generate_scenario_module(missionID, mission_level, last_mission_score, last_mission_score_1, last_mission_score_2, seed_value, country, location, current_day, current_month)
    scenario_location, scenario_attack_context, scenario_means_of_attack, scenario_attackers_group_name, scenario_cities, scenario_total_damage_mitigation_fraction_by_type, sops_policies, scenario_svg, damage_probability_by_type, mission_level, all_levels, last_mission_score_1, last_mission_score_2  = generate_scenario_module(0, last_mission_level, mean_score, mean_score, mean_score, seed_value, country, location, current_day, current_month)

    context['seed_value'] = seed_value
    context['mission_level'] = mission_level
    context['all_levels'] = all_levels
    #### context['next_seed_value'] = next_seed_value
    context['scenario_location'] = scenario_location
    context['scenario_attack_context'] = scenario_attack_context
    context['scenario_means_of_attack'] = scenario_means_of_attack
    context['scenario_attackers_group_name'] = scenario_attackers_group_name
    context['scenario_cities'] = scenario_cities
    context['damage_probability_by_type'] = damage_probability_by_type
    context['sops_policies'] = sops_policies
    #### context['scenario_total_damage_mitigation_fraction_by_type'] = scenario_total_damage_mitigation_fraction_by_type

    return HttpResponse(json.dumps(context),content_type="application/json")
    #return HttpResponse(context, content_type="application/json")
    #return JsonResponse(context)
#Scenario View - End


#Index View - Start
def index(request):
    logger = logging.getLogger(__name__)

    general_seed_value = int(request.GET.get('seed_value', random.randrange(sys.maxsize)))
    random.seed(general_seed_value)

    next_seed_value = []

    location = str(request.GET.get('location')).upper()
    logger.error('views location: '+str(location))

    location = location.split(',')
    logger.error('views location: '+str(location))

    country = str(request.GET.get('country')).lower()
    country = country.split(',')

    if len(country) > len(location):
        teams_number = range(len(country))
        for idx in range(len(country)-len(location)):
            location.append('*')
    else:
        teams_number = range(len(location))
        for idx in range(len(location)-len(country)):
            country.append('*')

    current_day = int(request.GET.get('day', datetime.now().day))
    current_month = int(request.GET.get('month', datetime.now().month))

    if current_month < 1:current_month = 1
    if current_month > 12: current_month = 12

    if current_day < 1: current_day = 1
    if (current_day > 29) and (current_month in days_29): current_day = 29
    if (current_day > 30) and (current_month in days_30): current_day = 30
    if (current_day > 31) and (current_month in days_31): current_day = 31

    json = []
    one_json = {}
    for idx in teams_number:
        if location[idx] == '*' or location[idx] not in locations: location[idx] = random.choice(locations)
        if country[idx] == '*' or country[idx] not in countries: country[idx] = random.choice(countries)
        next_seed_value.append(random.randrange(sys.maxsize))

        scenario_location, scenario_attack_context, scenario_means_of_attack, scenario_attackers_group_name, scenario_cities, scenario_total_damage_mitigation_fraction_by_type, sops_policies, scenario_svg, damage_probability_by_type, mission_level, all_levels, last_mission_score_1, last_mission_score_2 = generate_scenario_module(0, 0, 0, 0, 0, next_seed_value[idx],country[idx], location[idx], current_day, current_month)

        random.seed(next_seed_value[idx])
        next_seed_value2 = random.randrange(sys.maxsize)

        one_json = {'sops_policies': sops_policies,
                    'scenario_svg': scenario_svg,
                    'damage_probability_by_type': damage_probability_by_type,
                    'teamID': idx,
                    'missionID': 0,
                    'mission_level': 0,
                    'all_levels': all_levels,
                    'last_mission_score_1': 0,
                    'last_mission_score_2': 0,
                    'seed_value': next_seed_value[idx],
                    'next_seed_value': next_seed_value2,
                    'scenario_location': scenario_location,
                    'scenario_attack_context': scenario_attack_context,
                    'scenario_means_of_attack': scenario_means_of_attack,
                    'scenario_attackers_group_name': scenario_attackers_group_name,
                    'scenario_cities': scenario_cities,
                    'scenario_total_damage_mitigation_fraction_by_type': scenario_total_damage_mitigation_fraction_by_type,
                    }
        json.append(one_json)

    context = { 'general_seed_value': general_seed_value,
                'current_day': current_day,
                'current_month': current_month,
                'team': teams_number,
                'location': location,
                'country': country,
                'next_seed_value': next_seed_value,
                'json': json,
                }

    return render(request, 'scenario/index.html', context)
#Index View - End

#Views - End