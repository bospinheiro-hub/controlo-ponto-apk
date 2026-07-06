[app]
title = Sistema de Ponto Pro
package.name = pontosistemanovo
package.domain = org.empresanova.sistema
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 2.0

# REQUISITOS SEGUROS: Removidas bibliotecas duplicadas de SSL que baralhavam o Android
requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# CALIBRAGEM TOTAL PARA ANDROID MODERNOS
android.api = 34
android.minapi = 26
android.ndk_api = 26
android.ndk = 26b
android.private_storage = True
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
p4a.branch = master
