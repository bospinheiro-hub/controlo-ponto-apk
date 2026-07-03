[app]
title = Controlo de Ponto
package.name = controloponto
package.domain = org.empresa
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*

version = 1.0

# Trancar versões estáveis para evitar quebras na compilação do NDK
requirements = python3==3.10.12,kivy==2.3.0,requests==2.31.0,urllib3==1.26.15,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1

# Permissões do Android
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Configurações do SDK/NDK compatíveis com estas versões
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True
