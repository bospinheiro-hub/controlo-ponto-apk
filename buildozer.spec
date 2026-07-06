[app]
title = Sistema de Ponto Pro
package.name = pontosistemanovo
package.domain = org.empresanova.sistema
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 2.0

requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# JFORÇA A COMPILAÇÃO PURA DE 64 BITS MODERNA (API 34 + NDK 26b + ARM64)
android.api = 34
android.minapi = 26
android.ndk_api = 26
android.ndk = 26b
android.private_storage = True
android.archs = arm64-v8a

android.allow_backup = True
android.accept_sdk_license = True
p4a.branch = master
