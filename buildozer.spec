[app]
title = Controlo de Ponto
package.name = controloponto
package.domain = org.empresa
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 1.0

# Adicionado openssl para permitir comunicações de rede estáveis no Android
requirements = python3,kivy,requests,openssl,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

# Permissões nativas para validar Wi-Fi e aceder à Internet
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True
