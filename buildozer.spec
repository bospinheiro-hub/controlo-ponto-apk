[app]
title = Sistema de Ponto Pro
package.name = pontosistemaunificado
package.domain = org.empresanova.unificado
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 3.0

requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# ALINHAMENTO EXATO COM O SISTEMA DO GITHUB ACTIONS
android.api = 34
android.minapi = 26
android.private_storage = True
android.ndk = 27c
android.ndk_api = 26
android.archs = arm64-v8a

android.allow_backup = True
android.accept_sdk_license = True
p4a.branch = master
