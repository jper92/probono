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
			return render_to_response('new_mail.html', {'form': InteresadosForm(), 'success':True, }, context_instance=RequestContext(request))
		else:
			return render_to_response('new_mail.html',{'form': form, 'errors': form.errors, 'success':False}, context_instance= RequestContext(request))
	else:
		form = InteresadosForm()
	return render_to_response('new_mail.html', {'form': form, 'success':False, }, context_instance=RequestContext(request))
