[app]
title = Controlo de Ponto
package.name = controloponto
package.domain = org.empresa
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Inclui apenas o estritamente necessário para o script rodar
requirements = python3,kivy,requests

orientation = portrait
fullscreen = 1

# Permissões limpas
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Versões estáveis e compatíveis com a nuvem do GitHub
android.api = 33
android.minapi = 21
android.ndk_api = 21

# Compilar Apenas para ARM 64-bit (Padrão de 99% dos telemóveis Android modernos)
# Isto reduz o tempo de compilação para metade e evita erros de linkagem (NDK)
android.archs = arm64-v8a

android.allow_backup = True
