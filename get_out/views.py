from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, render

from atlas_api.location import Location

from get_out import forms

import json

def index(request):    
    form = forms.LocationSearchForm() 
    defaults = {"bird":5, "fish":0, "land_animal":5,"plant":5, "tree":5}
    things = [{'image':'/static/img/{0}.png'.format(x), 'description':'{0}'.format(x), 'default':y} for x, y in defaults.items()]
    return render(request, 'templates/index.html', {
        'form': form,
        'things':things
    })

def list_view(request):
    location = None
    species_weight = None
    #retrieve the location    
    location = request.REQUEST.get('location', 'wilsons promontory')
    #and the weights
    species_weight = {x : int(request.REQUEST.get(x, 5)) for x in ("bird", "plant", "tree")}    
    #don't include fish unless the user really wants it
    species_weight['fish'] = int(request.REQUEST.get('fish', 0))
    #land_animal maps to other
    species_weight['other'] = int(request.REQUEST.get('land_animal', 5))
    return render_to_response('templates/list.html', {'things': Location(location).ranked_species(10, species_weight)}, 
        context_instance=RequestContext(request))

def species(request):
		name = request.GET.get("name")
		species = [species.as_json() for species in Location(name).species]
		return HttpResponse(json.dumps(species), mimetype="application/json")
