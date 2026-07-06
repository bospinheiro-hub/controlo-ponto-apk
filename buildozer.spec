[app]
title = Sistema de Ponto Pro
package.name = pontosistemapro
package.domain = org.empresanova.ponto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 1.0

requirements = python3,kivy,requests,openssl,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# CALIBRAGEM ESTREITA PARA PASSAR NOS TELEMÓVEIS ATUAIS
android.api = 34
android.minapi = 26
android.ndk_api = 26
android.ndk = 26b
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
p4a.branch = master
