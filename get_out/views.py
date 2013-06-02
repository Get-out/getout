from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse

from atlas_api.species_list import SpeciesList
from atlas_api.location import Location404

from urllib import urlencode
from get_out import forms

import json

DEFAULT_TYPE_WEIGHTS = {"bird":5, "fish":0, "land_animal":5, "plant":5, "tree":5}

class Options(object):
    def __init__(self, location, per_page, simple_names, species_weights):
        self.location = location
        self.per_page = per_page
        self.simple_names = simple_names
        self.species_weights = species_weights

    def urlparams(self):
        params = dict(location=self.location, per_page=self.per_page, simple_names=self.simple_names)
        params.update(self.species_weights)
        return params

def options_from_request(req):
    """Get us some parameters from the request GET and POST"""
    location = req.REQUEST.get('location', 'wilsons promontory')
    per_page = req.REQUEST.get('per_page', 10)
    simple_names = bool(req.REQUEST.get('simple_names', True))
    species_weights = {k:v for k, v in req.REQUEST.items() if k in DEFAULT_TYPE_WEIGHTS}
    return Options(location, per_page, species_weights, simple_names)

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
    options = options_from_request(request)
    response = redirect('list')
    response['Location'] += '?{}'.format(urlencode(options.urlparams()))
    return response

def list_view(request):
    """Give us a list of animals for a location for humans"""
    File = 'templates/list.html'
    extra = {'not_found_image':staticfiles_storage.url('img/not-found.gif')}

    try:
        options = options_from_request(request)
        extra['things'] = SpeciesList(options.location, options.species_weights).retreive(options.per_page)
        extra['options'] = options
    except Location404:
        extra['things'] = []
        extra['bad_location'] = True

    return render_to_response(File, extra)

########################
###   JSON
########################

def species(request):
    """Give us a list of species for a location for computers"""
    options = options_from_request(request)
    things = SpeciesList(options.location, options.species_weights).retreive(options.per_page)
    things_json = [species.as_json() for species in things]
    return HttpResponse(json.dumps(things_json), mimetype="application/json")

