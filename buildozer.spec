[app]
title = Controlo de Ponto
package.name = controloponto
package.domain = org.empresa
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests,urllib3,certifi

orientation = portrait
fullscreen = 1

# Permissões do Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
