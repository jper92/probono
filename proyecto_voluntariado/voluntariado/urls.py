from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('voluntariado.views',
    url(r'^nuevaorg/$', 'ingreso_organizacion'),
    url(r'^nuevovoluntario/$', 'ingreso_voluntario'),
    url(r'^nuevaempresa/$', 'ingreso_empresa'),
    url(r'^voluntario/(\d+)/$', 'volunteer_profile'),
    url(r'^(voluntario)/(\d+)/buscar_empleo/$', 'match_search'),
    url(r'^(ong)/\d+/buscar_voluntario/puesto/(\d+)/$', 'match_search'),
)
