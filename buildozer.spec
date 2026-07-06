[app]
title = Sistema de Ponto Pro
package.name = pontosistemapro
package.domain = org.empresanova.ponto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 1.0

# Requisitos limpos e estáveis para evitar conflitos de compilação
requirements = python3,kivy==2.3.0,requests,openssl,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# CONFIGURAÇÃO DE SEGURANÇA E EMPACOTAMENTO PARA ANDROID 14 e 15
android.api = 34
android.minapi = 26
android.ndk_api = 26
android.ndk = 26b
android.private_storage = True

# Garante o empacotamento nativo puro exigido pelos telemóveis novos
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
p4a.branch = master
