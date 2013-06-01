from django.template import RequestContext, loader
from django.http import HttpResponse

def index(request):
    template = loader.get_template('templates/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

