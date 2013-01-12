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
		return '%s está esperando su aprobación para participar en el proyecto.' % (str(voluntario))
	elif value == 1:
		return 'Esperando a que %s acepte trabajar en este proyecto.' % (str(voluntario))
	elif value == 2:
		return '%s está actualmente trabajando en el proyecto.' % (str(voluntario))
	elif value == 3:
		return '%s ha finalizado satisfactoriamente su trabajo.' % (str(voluntario))
	elif value == 4:
		return '%s ha finalizado insatisfactoriamente su trabajo.' % (str(voluntario))
