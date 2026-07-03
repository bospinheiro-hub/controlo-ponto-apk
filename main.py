import os
import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform

# Mude para o IP fixo real do seu computador servidor Windows
SERVIDOR_URL = "http://192.168.1" 

class PontoApp(App):
    def build(self):
        if platform == 'android':
            from android.storage import app_storage_details
            self.data_dir = app_storage_details().filesDir
        else:
            self.data_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.db_path = os.path.join(self.data_dir, "offline_ponto.json")
        self.estado_atual = self.carregar_estado()

        layout = BoxLayout(orientation='vertical', padding=30)
        self.btn_ponto = Button(font_size='24sp', background_normal='')
        self.btn_ponto.bind(on_press=self.registar_ponto)
        
        self.atualizar_botao_ui()
        layout.add_widget(self.btn_ponto)
        
        self.sincronizar_dados_offline()
        return layout

    def carregar_estado(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                try:
                    dados = json.load(f)
                    if dados.get("registos"):
                        ultimo_tipo = dados["registos"][-1]["tipo"]
                        return "Saída" if ultimo_tipo == "Entrada" else "Entrada"
                except:
                    pass
        return "Entrada"

    def atualizar_botao_ui(self):
        if self.estado_atual == "Entrada":
            self.btn_ponto.text = "REGISTAR ENTRADA"
            self.btn_ponto.background_color = (0.1, 0.7, 0.3, 1)
        else:
            self.btn_ponto.text = "REGISTAR SAÍDA"
            self.btn_ponto.background_color = (0.9, 0.2, 0.2, 1)

    def registar_ponto(self, instance):
        self.btn_ponto.disabled = True 
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registo = {"timestamp": timestamp, "tipo": self.estado_atual}
        
        self.guardar_localmente(registo)
        self.estado_atual = "Saída" if self.estado_atual == "Entrada" else "Entrada"
        self.atualizar_botao_ui()
        self.btn_ponto.disabled = False
        
        self.sincronizar_dados_offline()

    def guardar_localmente(self, registo):
        dados = {"registos": []}
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                try:
                    dados = json.load(f)
                except:
                    pass
        dados["registos"].append(registo)
        with open(self.db_path, "w") as f:
            json.dump(dados, f, indent=4)

    def sincronizar_dados_offline(self):
        if not os.path.exists(self.db_path):
            return
        with open(self.db_path, "r") as f:
            try:
                dados = json.load(f)
            except:
                return
        if not dados.get("registos"):
            return

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        UrlRequest(
            SERVIDOR_URL,
            req_body=json.dumps(dados),
            req_headers=headers,
            on_success=self.on_envio_sucesso,
            on_failure=self.on_envio_falha,
            on_error=self.on_envio_falha,
            timeout=5
        )

    def on_envio_sucesso(self, request, result):
        if os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({"registos": []}, f)

    def on_envio_falha(self, request, error):
        pass

if __name__ == '__main__':
    PontoApp().run()
