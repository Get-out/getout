from django.shortcuts import render_to_response, render
from django.http import HttpResponse

from atlas_api.species_list import SpeciesList

from get_out import forms

import json

DEFAULT_TYPE_WEIGHTS = {"bird":5, "fish":0, "land_animal":5, "plant":5, "tree":5}
def things_list_from_request(req):
    location = req.REQUEST.get('location', 'wilsons promontory')
    page_amount = req.REQUEST.get('per_page', 10)
    species_weights = {k:v for k, v in req.REQUEST.items() if k in DEFAULT_TYPE_WEIGHTS}
    return SpeciesList(location, species_weights).retreive(page_amount)

########################
###   VIEWS
########################

def index(request):
    """Give us an index page with sliders for the different kinds of things to look for"""
    form = forms.LocationSearchForm()
    things = [
	{'type':typ, 'default':dflt, 'path':'img/{}.png'.format(typ)}
	for typ, dflt in DEFAULT_TYPE_WEIGHTS.items()
    ]
    return render(request, 'templates/index.html', {'form': form, 'things':things})

def list_view(request):
    """Give us a list of animals for a location for humans"""
    File = 'templates/list.html'
    extra = {}

    try:
        extra['things'] = things_list_from_request(request)
    except Location404:
        extra['things'] = []
        extra['bad_location'] = True

    return render_to_response(File, extra)

########################
###   JSON
########################

def species(request):
    """Give us a list of species for a location for computers"""
    things = [species.as_json() for species in things_list_from_request(request)]
    return HttpResponse(json.dumps(things), mimetype="application/json")

