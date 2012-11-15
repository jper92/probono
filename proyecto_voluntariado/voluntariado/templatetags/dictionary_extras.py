#!/usr/bin/python
# -*- encoding: UTF-8 -*-

from django import template
register = template.Library()

@register.filter(name='access')
def access(value, arg):
	return value[arg]

@register.filter(name='pvs')
def pvs(voluntario, value):
	if value == 0:
		return voluntario+' está esparando su aprobación para participar en el proyecto.'
	elif value == 1:
		return 'Esperando a que '+voluntario+' acepte trabajar en este proyecto.'
	elif value == 2:
		return voluntario+' está actualmente trabajando en el proyecto.'
	elif value == 3:
		return voluntario+' ha finalizado satisfactoriamente su trabajo.'
	elif value == 4:
		return voluntario+' ha finalizado insatisfactoriamente su trabajo.'
