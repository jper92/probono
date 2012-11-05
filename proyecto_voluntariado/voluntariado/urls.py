from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('voluntariado.views',
	url(r'^main/$', 'main_view'),
	url(r'^intereses/(\d+)/$','new_interest'),
	url(r'^nuevaorg/$', 'ingreso_ong'),
	url(r'^nuevovoluntario/$', 'ingreso_voluntario'),
	url(r'^nuevaempresa/$', 'ingreso_empresa'),
	url(r'^voluntario/(\d+)/$', 'volunteer_profile'),
	url(r'^(voluntario)/(\d+)/buscar_empleo/$', 'match_search'),
	url(r'^empresa/(\d+)/$', 'ong_profile'), #TODO perfil de empresa
	url(r'^(empresa)/(\d+)/buscar_empleo/$', 'match_search'),
	url(r'^ong/(\d+)/$', 'ong_profile'),
	url(r'^(ong)/\d+/buscar_voluntario/puesto/(\d+)/$', 'match_search'),
	url(r'^ong/(\d+)/nuevoproyecto/$', 'nuevo_proyecto'),
	url(r'^proyecto/(\d+)/$', 'proyecto'),
)
