# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

"""
Modulo responsável por realizar as requisições com a api do GitHub.
"""

import settings
from json import loads
from requests import get
from os import path, makedirs


class Notificacao:
	"""
	Classe responsável por tratar adicionar notificações.
	"""
	id_notificacao = None
	nome_usuario = None
	acao = None
	repositorio = None

	def __init__(self, id_notificacao, nome_usuario, acao, repositorio):
		self.id_notificacao = id_notificacao
		self.nome_usuario = nome_usuario
		self.acao = acao
		self.repositorio = repositorio

	def obter_notificacao(self):
		return '{0} {1} {2}'.format(self.nome_usuario, self.acao, self.repositorio)


def obter_notificacoes(nome_usuario):
	"""
	Realiza as requisições a api do github para obter as notificações de uma determinada conta.
	"""
	notificacoes = []
	novo_diretorio = False
	try:
		resposta = get('https://api.github.com/users/{0}/received_events'.format(nome_usuario))
		res_json = resposta.json()
		for r in res_json:
			if not (path.exists('{0}/cache/{1}.json'.format(settings.path_media, r['id']))):
				tipo = r['type']
				id_notificacao = r['id']
				nome_usuario = r['actor']['login']
				if tipo == 'FollowEvent':
					acao = 'started following'
					repositorio = r['payload']['target']['login']
				if tipo == 'CreateEvent':
					acao = 'created repository'
					repositorio = r['repo']['name']
				if tipo == 'WatchEvent':
					acao = 'starred'
					repositorio = r['repo']['name']
				elif tipo == 'ForkEvent':
					acao = 'forked'
					repositorio = r['repo']['name']
				notificacao = Notificacao(id_notificacao, nome_usuario, acao, repositorio)
				notificacoes.append(notificacao)
				grava_notificacao(notificacao)
	except:
		return None
	return notificacoes


def grava_notificacao(notificacao):
	"""
	abre o arquivo cache e salva uma determinada notificação a partir de um id.
	"""
	dados = '{\"id\": \"' + notificacao.id_notificacao + '\",' + '\"nome_usuario\": ' + '\"' + notificacao.nome_usuario + '\",' + '\"acao\": ' + '\"' + notificacao.acao + '\",' + '\"repositorio\": ' + '\"' + notificacao.repositorio+ '\"}'
	arq = open('{0}/cache/{1}.json'.format(settings.path_media, notificacao.id_notificacao), 'w')
	arq.write(dados)
	arq.close()


def verifica_diretorio(diretorio):
	"""
	Verifica se um diretorio existe, se não, cria o diretório e retorna True.
	"""
	if not path.exists(diretorio):
		makedirs(diretorio)
		return True
	return False


def verifica_usuario():
	"""
	Verifica se uma conta de usuário está configurada no arquivo user na pasta login.
	"""
	verifica_diretorio('{0}/login'.format(settings.path_media))
	if not path.exists('{0}/login/user.json'.format(settings.path_media)):
		arq = open('{0}/login/user.json'.format(settings.path_media), 'w')
		arq.close()
	else:
		arq = open('{0}/login/user.json'.format(settings.path_media)).read()
		if len(arq) != 0:
			arq_json = loads(arq)
			if len(arq_json) != 0:
				return arq_json[0]
	return 'Nenhuma Conta'
