#!/usr/bin/python
# -*- encoding: UTF-8 -*-

import datetime
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import *
from django.db.models import Q

from models import Organizacion, Voluntario, VoluntariosAplicando
from forms import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from linkedin import hola, requestToken, getAccess


# Vistas básicas
def about(request):
	return render_to_response('about.html',{}, context_instance=RequestContext(request))
def contact_us(request):
	return render_to_response('contact.html',{}, context_instance=RequestContext(request))


# Estos 2 metodos indican a la view ingreso_organizacion si se trata de ONG o de empresa
def ingreso_ong(request):
	return ingreso_organizacion(request, True)
def ingreso_empresa(request):
	return ingreso_organizacion(request, False)


#  name: ingreso_organizacion
#  @param request, es_ong: bool
def ingreso_organizacion(request, es_ong):

	if request.method == 'POST':	# Intenta crear un usuario, si algo no es validado se eliminan todos los cambios
		# Si se elige agregar un nuevo interes
		if 'nuevointeres' in request.POST:
			form = FormInteres(request.POST)
			try:
				interes = Intereses(nombre= form.data['nombre_i'], descripcion = form.data['descripcion_i'], es_favorito= form.data['es_favorito'])
				interes.save()
				return render_to_response('new_org.html', {'form': FormularioONG(request.POST), 'interes': FormInteres(), 'title':'Nueva ONG' if es_ong else 'Nueva empresa'}, context_instance=RequestContext(request))
			except:
				return render_to_response('new_org.html', {'form': FormularioONG(request.POST),'interes': FormInteres(), 'title':'Nueva ONG' if es_ong else 'Nueva empresa', 'error':'Error: No se pudo guardar el interes'}, context_instance=RequestContext(request))

		# Aquí se asume que se guardara una nueva organización.
		form = FormularioONG(request.POST, request.FILES)
		try:
			user = User.objects.get(username=form['username'].value())
		# si hubo error, no existe el usuario y se tiene libertad de crearlo
		except:
			user = User.objects.create_user(form['username'].value(), form['correo'].value(), form['password'].value())
			org = Organizacion(user = user, es_empresa = not es_ong, expira = datetime.datetime.now() + datetime.timedelta(days=30))
			form = FormularioONG(request.POST, request.FILES, instance = org)
			if form.is_valid():
				interesado = form.save()
				#return redirect('/voluntario/' + str(vol.user_id))
				return redirect('/main/')
			else:
				user.delete()
				return render_to_response('new_org.html',{'form':form, 'interes': FormInteres(), 'title':'Nueva ONG' if es_ong else 'Nueva empresa', 'error': 'Error. No se pudo crear el usuario'}, context_instance=RequestContext(request))
		# si no hubo error, el usuario ya existe, por lo que no se le permite agregarlo
		return render_to_response('new_org.html',{'form':form, 'interes': FormInteres(), 'title':'Nueva ONG' if es_ong else 'Nueva empresa', 'error': form['username'].value() + ' ya existe'}, context_instance=RequestContext(request))
	else:
		form = FormularioONG()
	return render_to_response('new_org.html', {'form': form, 'interes': FormInteres(), 'title':'Nueva ONG' if es_ong else 'Nueva empresa'}, context_instance=RequestContext(request))


# Perfil de ong
def ong_profile(request, id_ong):
	ong = Organizacion.objects.get(user=id_ong)
	return render_to_response('ong_profile.html', {'ong':ong }, context_instance=RequestContext(request))


# Vista ingreso voluntario
def ingreso_voluntario(request):
	if request.method == 'POST':	# Intenta crear un usuario, si algo no es validado se eliminan todos los cambios
		# Si se elige agregar un nuevo interes
		if 'nuevointeres' in request.POST:
			form = FormInteres(request.POST)
			try:
				interes = Intereses(nombre=form.data['nombre_i'], descripcion=form.data['descripcion_i'], es_favorito = form.data['es_favorito'])
				interes.save()
				return render_to_response('new_volunteer.html', {'form': FormularioVoluntario(request.POST),'interes': FormInteres(), 'title':'Nuevo Voluntario'}, context_instance=RequestContext(request))
			except:
				return render_to_response('new_volunteer.html', {'form': FormularioVoluntario(request.POST),'interes': FormInteres(), 'title':'Nuevo Voluntario', 'error':'Error: No se pudo guardar el interes'}, context_instance=RequestContext(request))

		# Aqui se asume que se guardara un nuevo voluntario.
		form = FormularioVoluntario(request.POST)
		try:
			user = User.objects.get(username=form['username'].value())
		# si hubo error, no existe el usuario y se tiene libertad de crearlo
		except:
			user = User.objects.create_user(form['username'].value(), form['correo'].value(), form['password'].value())
			vol = Voluntario(user = user, evaluacion = 0, puntos = 0)
			form = FormularioVoluntario(request.POST, request.FILES, instance = vol)
			if form.is_valid():
				interesado = form.save()
				#return redirect('/voluntario/' + str(vol.user_id))
				return redirect('/main/')
			else:
				user.delete()
				return render_to_response('new_volunteer.html',{'form':form, 'interes': FormInteres(), 'title':'Nuevo voluntario', 'error': 'Error, no se pudo crear el usuario'}, context_instance=RequestContext(request))
		# si no hubo error, el usuario ya existe, por lo que no se le permite agregarlo
		return render_to_response('new_volunteer.html',{'form':form, 'interes': FormInteres(), 'title':'Nuevo voluntario', 'error': form['username'].value() + ' ya existe'}, context_instance=RequestContext(request))
	else:
		form = FormularioVoluntario()
	return render_to_response('new_volunteer.html', {'form': form, 'interes': FormInteres(), 'title':'Nuevo voluntario'}, context_instance=RequestContext(request))


# Perfil de voluntario
def volunteer_profile(request, id_voluntario):
	vol = Voluntario.objects.get(user=id_voluntario)
	return render_to_response('volunteer_profile.html', {'vol': vol, 'current': datetime.datetime.now().year - vol.nacimiento.year }, context_instance=RequestContext(request))


# Ingreso de nuevo proyecto
def nuevo_proyecto(request):
	if request.user.is_authenticated():
		ong = Organizacion.objects.get(user=request.user)
		if request.method == 'POST':
			form = FormularioProyecto(request.POST)
			#print form
			if form.is_valid():
				proyecto = form.save(commit = True)
				return HttpResponseRedirect('/home/ong/'+str(proyecto.id))
		else:
			form = FormularioProyecto(initial={'organizacion':ong.correo})
		return render_to_response('nuevo_proyecto.html', {'form':form}, context_instance=RequestContext(request))
	else:
		return redirect('/main/')

# Perfil del proyecto
def proyecto(request, id_proy):
	if request.user.is_authenticated():
		proyecto = Proyecto.objects.get(id=id_proy)
		escolaridad = {'p':'Primaria','b':'Básicos','d':'Diversificado','u':'Universitario','m':'Maestría/Doctorado','n':'Ninguna'}
		return render_to_response('proyecto.html', {'proyecto':proyecto, 'esc':escolaridad}, context_instance=RequestContext(request))
	else:
		return redirect('/main/')


# Ingreso de Puesto
def nuevo_puesto(request, id_proy):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = FormularioPuesto(request.POST)
			if form.is_valid():
				puesto = form.save()
				return HttpResponseRedirect('../../../puesto/'+str(puesto.id))
		else:
			form = FormularioPuesto(initial={'proyecto':id_proy})
		return render_to_response('nuevo_puesto.html', {'form':form}, context_instance=RequestContext(request))
	else:
		return redirect('/main/')

# Perfil de puesto
def puesto(request, id_puesto):
	if request.user.is_authenticated():
		puesto = Puesto.objects.get(id=id_puesto)
		escolaridad = {'p':'Primaria','b':'Básicos','d':'Diversificado','u':'Universitario','m':'Maestría/Doctorado','n':'Ninguna'}
		return render_to_response('puesto.html', {'puesto':puesto, 'esc':escolaridad}, context_instance=RequestContext(request))
	else:
		return redirect('/main/')


# Motor de búsquedas de puestos
def busqueda_vol(request):
	if request.user.is_authenticated():
		vol = Voluntario.objects.get(user=request.user)
		especialidades = vol.especialidades.all()
		favoritos = vol.favoritos.all()
		q = Q()
		for f in favoritos:
			q.add(Q(favoritos=f),Q.OR)
		for e in especialidades:
			q.add(Q(especialidades=e),Q.OR)
		
		lista = Puesto.objects.filter(q)
		return render_to_response('match_search.html',{'tipo':'voluntario','obj':vol,'lista':lista}, context_instance=RequestContext(request))
	else:
		return redirect('/main/')

def match_search(request, tipo, id_req):
	if request.user.is_authenticated():
		lista=[]
		lista2=[]
		id_req = int(id_req)
		obj = None
		q = Q()

		if tipo=='voluntario':
			obj = Voluntario.objects.get(user=id_req)
		elif tipo=='empresa':
			obj = Organizacion.objects.get(user=id_req)
		
		if tipo=='voluntario' or tipo=='empresa':
			especialidades = obj.especialidades.all()
			favoritos = obj.favoritos.all()
			for f in favoritos:
				q.add(Q(favoritos=f),Q.OR)
			for e in especialidades:
				q.add(Q(especialidades=e),Q.OR)
			
			lista = Puesto.objects.filter(q)

		elif tipo=='puesto':
			obj = Puesto.objects.get(id=id_req)
			especialidades = obj.especialidades.all()
			favoritos = obj.favoritos.all()
			
			for e in especialidades:
				q.add(Q(especialidades=e),Q.OR)
			for f in favoritos:
				q.add(Q(favoritos=f),Q.OR)
			
			lista = Voluntario.objects.filter(q)
			q.add(Q(es_empresa=True),Q.AND)
			lista2 = Organizacion.objects.filter(q)
			
		return render_to_response('match_search.html',{'tipo':tipo,'obj':obj,'lista':lista,'lista2':lista2}, context_instance=RequestContext(request))
	else:
		return redirect('/main/')

# vista de voluntario desde puesto
def puesto_voluntario2(request, id_puesto, id_vol):
	if request.user.is_authenticated():
		pue = Puesto.objects.get(id=id_puesto)
		vol = Voluntario.objects.get(user=id_vol)
		escolaridad = {'p':'Primaria','b':'Básicos','d':'Diversificado','u':'Universitario','m':'Maestría/Doctorado','n':'Ninguna'}
		try:
			volap = VoluntariosAplicando.objects.get(puesto=pue, voluntario=vol)
		except:
			volap = None
		if volap:
			return render_to_response('puesto_voluntario2.html', {'puesto':pue, 'voluntario':vol, 'esc':escolaridad, 'status':volap}, context_instance=RequestContext(request))
		else:
			if request.method == 'POST':
				form = FormularioVoluntarioAplicando(request.POST)
				if form.is_valid():
					puesto = form.save()
					return HttpResponseRedirect('')
			else:
				form = FormularioVoluntarioAplicando(initial={'voluntario':vol.correo, 'puesto':pue.id, 'status':1})
			return render_to_response('puesto_voluntario2.html', {'puesto':pue, 'voluntario':vol, 'esc':escolaridad, 'form':form}, context_instance=RequestContext(request))
	else:
		return redirect('/main/')

# Vista de empresa desde puesto
def puesto_empresa(request, id_puesto, id_vol):
	if request.user.is_authenticated():
		pue = Puesto.objects.get(id=id_puesto)
		emp = Organizacion.objects.get(user=id_vol)
		try:
			empap = EmpresasAplicando.objects.get(puesto=pue, empresa=emp)
		except:
			empap = None
		if empap:
			return render_to_response('puesto_empresa.html', {'puesto':pue, 'empresa':emp, 'status':empap}, context_instance=RequestContext(request))
		else:
			if request.method == 'POST':
				form = FormularioEmpresaAplicando(request.POST)
				if form.is_valid():
					puesto = form.save()
					return HttpResponseRedirect('')
			else:
				form = FormularioEmpresaAplicando(initial={'empresa':emp.correo, 'puesto':pue.id, 'status':1})
			return render_to_response('puesto_empresa.html', {'puesto':pue, 'empresa':emp, 'form':form}, context_instance=RequestContext(request))
	else:
		return redirect('/main/')


# Vista principal del proyecto, controla a dónde se redirige según el tipo de usuario.
def main_view(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password = request.POST['password'])
		if user is not None:
			login(request, user)
		else:
			return render_to_response('main.html', {'invalid':True}, context_instance=RequestContext(request))
	if request.user.is_authenticated():
		try:
			v = Voluntario.objects.get(user=request.user)
			return redirect('/home/voluntario/')
		except:
			try:
				org=Organizacion.objects.get(user=request.user)
				if (org.es_empresa):
					return redirect('/home/empresa/')
				else:
					return redirect('/home/ong/')
			except:
				logout(request)
				return redirect('/main/')
	else:
		return render_to_response('main.html',{}, context_instance=RequestContext(request))
	

# Manejo de ingreso con LinkedIn
def linkedin(request):
	if request.method == 'POST':
		response = getAccess(request.POST['pin'], request.session['tokens'])
		return HttpResponse(response)
	else:
		tokens = requestToken()
		request.session['tokens'] = tokens
		return HttpResponse("<a role='button' class='btn' href='https://api.linkedin.com/uas/oauth/authorize?oauth_token=" + tokens['oauth_token'] + "' target='_blank'>Ir a LinkedIn</a><input type='text' name='pin' placeholder='PIN de verificación' /> <button class='btn' type='button' id='pin_submit' onclick='obtener();'>Enviar</button>")


# Vista de voluntario
def home_voluntario(request):
	if request.user.is_authenticated():
		try:
			vol = Voluntario.objects.get(user=request.user)
			return render_to_response('home_volunteer.html',{'vol': vol,}, context_instance=RequestContext(request))
			#return render_to_response('main.html',{'current': None if vol==None else datetime.datetime.now().year - vol.nacimiento.year, 'vol': vol, 'user':request.user,}, context_instance=RequestContext(request))
		except:
			return redirect('/main/')
	else:
		return redirect('/main/')


# Vista ONG
def home_ong(request):
	if request.user.is_authenticated():
		try:
			ong = Organizacion.objects.get(user=request.user)
			if not ong.es_empresa:
				return render_to_response('home_ong.html',{'ong': ong,}, context_instance=RequestContext(request))
			else:
				return redirect('/main/')
			#return render_to_response('main.html',{'current': None if vol==None else datetime.datetime.now().year - vol.nacimiento.year, 'vol': vol, 'user':request.user,}, context_instance=RequestContext(request))
		except:
			return redirect('/main/')
	else:
		return redirect('/main/')


# Vista Empresa	
def home_empresa(request):
	if request.user.is_authenticated():
		try:
			ong = Organizacion.objects.get(user=request.user)
			if ong.es_empresa:
				return render_to_response('home_empresa.html',{'ong': ong,}, context_instance=RequestContext(request))
			else:
				return redirect('/main/')
			#return render_to_response('main.html',{'current': None if vol==None else datetime.datetime.now().year - vol.nacimiento.year, 'vol': vol, 'user':request.user,}, context_instance=RequestContext(request))
		except:
			return redirect('/main/')
	else:
		return redirect('/main/')


# Logout
def logout_view(request):
	logout(request)
	return redirect('/main/')

# Edición de voluntario
def edit_volunteer(request):
	if request.user.is_authenticated():
		if request.method=='POST':
			try:
				vol = Voluntario.objects.get(user=request.user)
				form = FormularioEditarVoluntario(request.POST, request.FILES, instance=vol)
				if form.is_valid():
					form.save()
					return redirect('/main/')
				else:
					return render_to_response('new_org.html',{'form': form, 'interes': FormInteres(), 'title':'Actualizar perfil', 'error': 'Error no se pudo actualizar la información'}, context_instance=RequestContext(request))
			except:
				return redirect('/main/')
		try:
			vol = Voluntario.objects.get(user=request.user)
			form = FormularioEditarVoluntario(instance=vol)
			return render_to_response('new_org.html',{'form': form, 'interes': FormInteres(), 'title':'Nuevo voluntario'}, context_instance=RequestContext(request))
		except:
			return redirect('/main/')
	else:
		return redirect('/main')


# Edición de empresa
def edit_ong(request):
	if request.user.is_authenticated():
		if request.method=='POST':
			try:
				ong = Organizacion.objects.get(user=request.user)
				form = FormularioEditarONG(request.POST, request.FILES, instance=ong)
				if form.is_valid():
					form.save()
					return redirect('/main/')
				else:
					return render_to_response('new_org.html',{'form': form, 'interes': FormInteres(), 'title':'Actualizar perfil', 'error': 'Error no se pudo actualizar la información'}, context_instance=RequestContext(request))
			except:
				return redirect('/main/')
		try:
			ong = Organizacion.objects.get(user=request.user)
			form = FormularioEditarONG(instance=ong)
			return render_to_response('new_org.html',{'form': form, 'interes': FormInteres(), 'title':'Actualizar perfil'}, context_instance=RequestContext(request))
		except:
			return redirect('/main/')
	else:
		return redirect('/main')


# Voluntario quiere buscar/consultar un puesto dado ya sea para observarlo o pedir aceptación
def puesto_voluntario(request, puesto):
	# válido si el puesto no está asociado y si el consultante es empresa/voluntario
	if request.method=='POST':
		if request.user.is_authenticated():
			try:
				p = Puesto.objects.get(pk=int(puesto))
			except:
				return redirect('/main/')
			try:
				vol = Voluntario.objects.get(user=request.user)
				asoc = VoluntariosAplicando(voluntario=vol, puesto=p,status=0,mensaje=request.POST['mensaje'])
				try:
					asoc.save()
					# Guardado exitosamente
					return render_to_response('/main/')
				except:
					# Hubo un error
					return render_to_response('puesto_voluntario.html',{'puesto': p, 'vol':vol, 'relacionado': True, 'error': True}, context_instance=RequestContext(request))
			except:
				try:
					e = Empresa.objects.get(user=request.user)
					asoc = EmpresasAplicando(empresa = e, puesto=p,status = 0, mensaje=request.POST['mensaje'])
					try:
						asoc.save()
						#Guardado
						return render_to_response('/main/')
					except:
						return render_to_response('puesto_voluntario.html',{'puesto': p, 'relacionado': True, 'error': True}, context_instance=RequestContext(request))
				except:
					logout(request)
					return redirect('/main/')
					
		else:
			# No está autenticado
			return redirect('/main/')
	# GET. Consulta de puesto.
	if request.user.is_authenticated():
		try:
			p = Puesto.objects.get(pk=int(puesto))
		except:
			return redirect('/main/')
		try:
			vol = Voluntario.objects.get(user=request.user)
			print 'aqui llego'
			print 'salio de puesto'
			try:
				VoluntariosAplicando.objects.get(voluntario=vol, puesto=p)
				# Esta relacionado puesto y voluntario
				return render_to_response('puesto_voluntario.html',{'puesto': p, 'relacionado': True}, context_instance=RequestContext(request))
			except:
				# No está relacionado
				return render_to_response('puesto_voluntario.html',{'puesto': p, 'relacionado': False}, context_instance=RequestContext(request))
		except:
			try:
				emp = Organizacion.objects.get(user=request.user)
				try:
					e = EmpresasAplicando.objects.get(empresa=e, puesto = p)
					# Esta relacionado
					return render_to_response('puesto_voluntario.html',{'puesto': p, 'relacionado': True}, context_instance=RequestContext(request))
				except:
					#No está relacionado
					return render_to_response('puesto_voluntario.html',{'puesto': p, 'relacionado': False}, context_instance=RequestContext(request))
			except:
				logout(request)
				return redirect('/main/')
	else:
		# No está autenticado
		return redirect('/main/')


def voluntario_ong(request):
	pass
