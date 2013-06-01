from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    template = loader.get_template('templates/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def list_view(request):
    return render_to_response('templates/list.html', {'things': [1,2,3]}, context_instance=RequestContext(request))