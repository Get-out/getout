from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, render

from atlas_api.location import Location

from get_out import forms

import json

def index(request):    
    form = forms.LocationSearchForm() 
    things = [({'image':'/static/img/{0}.png'.format(x), 'description':'{0}'.format(x)}) for x in ("birds", "fish", "other_fauna","plants", "trees")]
    return render(request, 'templates/index.html', {
        'form': form,
        'things':things
    })

def list_view(request):
    location = request.GET.get('location', 'wilsons promontory')
    return render_to_response('templates/list.html', {'things': Location(location).ranked_species}, context_instance=RequestContext(request))

def species(request):
		name = request.GET.get("name")
		species = [species.as_json() for species in Location(name).species]
		return HttpResponse(json.dumps(species), mimetype="application/json")
