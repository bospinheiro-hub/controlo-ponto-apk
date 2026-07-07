[app]
title = Sistema de Ponto Pro
package.name = pontosistemaunificado
package.domain = org.empresanova.unificado
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 3.0

# REQUISITOS LIMPOS: Apenas o python3 e o kivy nativos. A rede é gerida pelo UrlRequest embutido.
requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# CALIBRAGEM ESTÁVEL PARA ANDROID 14 E 15
android.api = 34
android.minapi = 26
android.private_storage = True
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
p4a.branch = master
