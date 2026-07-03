[app]
title = Controlo de Ponto
package.name = controloponto
package.domain = org.empresa
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*

version = 1.0

# REMOVIDAS AS VERSÕES FIXAS: O Buildozer vai usar o Python nativo automaticamente
requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

# Permissões do Android
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Configurações do SDK estáveis
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True
