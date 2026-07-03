[app]
title = Controlo de Ponto
package.name = controloponto
package.domain = org.empresa
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = tests/*, venv/*, *.pyc, build/*, .pytest_cache/*
version = 1.0

# Bibliotecas essenciais e estáveis para a aplicação não crashar ao usar a rede
requirements = python3,kivy,requests,openssl,urllib3,certifi,charset-normalizer,idna
# Força o Buildozer a descarregar a versão correta do instalador sem falhar caminhos
p4a.branch = master

orientation = portrait
fullscreen = 1

# Permissões do Android para aceder à rede Wi-Fi da empresa
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# Configurações do SDK compatíveis com o Java 17 do GitHub Actions
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True

# Força o Buildozer a aceitar os termos da Google automaticamente na nuvem
android.accept_sdk_license = True
