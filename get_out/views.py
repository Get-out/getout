from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, render

from atlas_api.location import Location

from get_out import forms

import json

def index(request):    
    form = forms.LocationSearchForm() 
    return render(request, 'templates/index.html', {
        'form': form
    })

def list_view(request):
    location = request.GET.get('location', 'wilsons promontory')
    return render_to_response('templates/list.html', {'things': Location(location).ranked_species}, context_instance=RequestContext(request))

def species(request):
		name = request.GET.get("name")
		species = [species.as_json() for species in Location(name).species]
		return HttpResponse(json.dumps(species), mimetype="application/json")
