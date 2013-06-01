from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse

from atlas_api.species_list import SpeciesList
from atlas_api.location import Location404

from urllib import urlencode
from get_out import forms

import json

DEFAULT_TYPE_WEIGHTS = {"bird":5, "fish":0, "land_animal":5, "plant":5, "tree":5}

def params_from_request(req):
    """Get us some parameters from the request GET and POST"""
    location = req.REQUEST.get('location', 'wilsons promontory')
    per_page = req.REQUEST.get('per_page', 10)
    species_weights = {k:v for k, v in req.REQUEST.items() if k in DEFAULT_TYPE_WEIGHTS}
    return location, per_page, species_weights

def things_list_from_request(req):
    """Get us some species from a request"""
    location, per_page, species_weights = params_from_request(req)
    return SpeciesList(location, species_weights).retreive(per_page)

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

def redirect_to_list(request):
    """Redirect to the list view"""
    location, per_page, species_weights = params_from_request(request)
    response = redirect('list')

    params = dict(location=location, per_page=per_page)
    params.update(species_weights)
    response['Location'] += '?{}'.format(urlencode(params))
    return response

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

