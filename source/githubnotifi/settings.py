# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

"""
Modulo responsável pelas configuracões globais do software.
"""

from os import path

# Tempo de Intervalo das requisições a API do GitHub.
PAUSE = 62

# Endereço dos códigos fontes do projeto.
path_dados  = path.abspath(path.dirname(__file__))

# Endereço das imagens e cache do projeto.
path_media = path.normpath(path.join(path_dados, '..', 'media'))
