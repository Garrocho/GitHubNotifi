# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

"""
Modulo responsável por realizar as requisições com a api do GitHub.
"""

import requests


class Notificacao:

	nome_usuario = None
	acao = None
	nome_repositorio = None

	def __init__(self, nome_usuario, acao, nome_repositorio):
		self.nome_usuario = nome_usuario
		self.acao = acao
		self.nome_repositorio = nome_repositorio

	def obter_notificacao(self):
		return '{0} {1} {2}'.format(self.nome_usuario, self.acao, self.nome_repositorio)


def obter_notificacoes(nome_usuario):
	resposta = requests.get('https://api.github.com/users/{0}/received_events'.format(nome_usuario))
	res_json = resposta.json()
	notificacoes = []
	for r in res_json:
		nome_usuario = r['actor']['login']
		try:
			acao = r['payload']['action']
		except:
			acao = 'forked'
		nome_repositorio = r['repo']['name']
		notificacao = Notificacao(nome_usuario, acao, nome_repositorio)
		notificacoes.append(notificacao)
	return notificacoes


if __name__ == '__main__':
	obter_notificacoes('CharlesGarrocho')