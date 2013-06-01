from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

from atlas_api.location import Location

import json

def index(request):
    template = loader.get_template('templates/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def list_view(request):
    return render_to_response('templates/list.html', {'things': [1,2,3]}, context_instance=RequestContext(request))

def species(request):
		name = request.GET.get("name")
		species = [species.as_json() for species in Location(name).species]
		return HttpResponse(json.dumps(species), mimetype="application/json")
