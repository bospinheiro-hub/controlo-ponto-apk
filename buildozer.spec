[app]
title = Sistema de Ponto Pro
package.name = pontosistemaantigo
package.domain = org.empresanova.antigo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 1.0

# REQUISITOS LEVES: Perfeitos para o Android 8.5 e inferiores
requirements = python3==3.9.9,kivy==2.1.0,requests,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# COMPATIBILIDADE RETROATIVA TRANCADA
android.api = 28
android.minapi = 21
android.ndk = 23b
android.ndk_api = 21
android.private_storage = True

# ARQUITETURA DUPLA: Garante suporte a chips de 32 bits antigos e 64 bits
android.archs = armeabi-v7a, arm64-v8a

android.allow_backup = True
android.accept_sdk_license = True

# CORREÇÃO DO ERRO: Ativa a ramificação moderna de downloads com suporte AAB
p4a.branch = master
