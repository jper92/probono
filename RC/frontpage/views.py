from django.http import *
from django.shortcuts import render_to_response
from django.template import *
# messages
from models import Interesados
from forms import InteresadosForm

def contact(request):
    if request.method == 'POST':
        form = InteresadosForm(request.POST)
        if form.is_valid():
            interesado = form.save()
    else:
        form = InteresadosForm()
    return render_to_response('frontpage.html', {'form': form}, context_instance=RequestContext(request))
