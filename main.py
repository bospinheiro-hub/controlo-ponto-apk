import os
import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.image import Image

class PontoApp(App):
    def build(self):
        if platform == 'android':
            from android.storage import app_storage_details
            self.data_dir = app_storage_details().filesDir
        else:
            self.data_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.db_path = os.path.join(self.data_dir, "offline_ponto.json")
        self.config_path = os.path.join(self.data_dir, "config_rede.json")
        self.backup_path = os.path.join(self.data_dir, "historico_seguro.json")
        self.estado_path = os.path.join(self.data_dir, "fluxo_botoes.json")
        self.logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        
        self.servidor_ip, self.servidor_porta, self.colaborador_nome, self.pin_mestre = self.carregar_configuracoes()
        self.historico_botoes = self.carregar_estado_botoes()

        self.layout_principal = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        with self.layout_principal.canvas.before:
            Color(0.118, 0.118, 0.180, 1) # #1e1e2e
            self.bg_rect = RoundedRectangle(size=self.layout_principal.size, pos=self.layout_principal.pos)
        self.layout_principal.bind(size=self._update_rect, pos=self._update_rect)

        # BARRA DE TOPO
        barra_topo = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        btn_config = Button(text="⚙", font_size='26sp', size_hint_x=None, width='50dp', background_normal='', background_color=(0,0,0,0), color=(0.65, 0.68, 0.78, 1))
        btn_config.bind(on_press=self.validar_acesso_admin)
        barra_topo.add_widget(btn_config)
        
        btn_limpar = Button(text="🗑️ Limpar", font_size='14sp', size_hint_x=None, width='90dp', background_normal='', background_color=(0,0,0,0), color=(0.91, 0.62, 0.67, 1))
        btn_limpar.bind(on_press=self.solicitar_limpeza_historico)
        
        barra_topo.add_widget(Label())
        barra_topo.add_widget(btn_limpar)
        self.layout_principal.add_widget(barra_topo)

        # LOGÓTIPO TRANSPARENTE NATIVO DO ANDROID
        if os.path.exists(self.logo_path):
            area_logo = Image(source=self.logo_path, size_hint_y=None, height='100dp', allow_stretch=True)
            self.layout_principal.add_widget(area_logo)
        else:
            lbl_titulo = Label(text="PAINEL DE PONTO DIGITAL", font_size='18sp', bold=True, color=(0.80, 0.84, 0.95, 1), size_hint_y=None, height='40dp')
            self.layout_principal.add_widget(lbl_titulo)

        self.lbl_user = Label(text=f"Colaborador: {self.colaborador_nome}", font_size='16sp', bold=True, color=(0.80, 0.84, 0.95, 1), size_hint_y=None, height='30dp')
        self.layout_principal.add_widget(self.lbl_user)

        self.passos = [
            {"id": "Entrada_1", "texto_p": "1. ENTRADA MANHÃ", "texto_s": "Início de dia", "tipo": "Entrada"},
            {"id": "Saida_1", "texto_p": "2. SAÍDA ALMOÇO", "texto_s": "Pausa para refeição", "tipo": "Saída"},
            {"id": "Entrada_2", "texto_p": "3. ENTRADA ALMOÇO", "texto_s": "Regresso ao trabalho", "tipo": "Entrada"},
            {"id": "Saida_2", "texto_p": "4. FIM DO DIA", "texto_s": "Encerramento diário", "tipo": "Saída"}
        ]

        self.botoes_ui = {}
        self.labels_ui = {}
        self.criar_interface_botoes()
        self.atualizar_bloqueios_sequenciais()

        Clock.schedule_once(lambda dt: self.sincronizar_dados_offline(), 2)
        return self.layout_principal
    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def criar_interface_botoes(self):
        for passo in self.passos:
            p_id = passo["id"]
            box_passo = BoxLayout(orientation='vertical', spacing=2, size_hint_y=None, height='90dp')
            
            btn = Button(text=passo["texto_p"], font_size='16sp', bold=True, background_normal='', color=(0.11, 0.11, 0.18, 1))
            btn.bind(on_press=lambda inst, pid=p_id: self.clique_passo(pid))
            box_passo.add_widget(btn)
            self.botoes_ui[p_id] = btn
            
            lbl = Label(text=passo["texto_s"], font_size='12sp', color=(0.42, 0.44, 0.55, 1))
            box_passo.add_widget(lbl)
            self.labels_ui[p_id] = lbl
            
            self.layout_principal.add_widget(box_passo)

    def atualizar_bloqueios_sequenciais(self):
        for passo in self.passos:
            p_id = passo["id"]
            hora_gravada = self.historico_botoes.get(p_id)
            if hora_gravada:
                self.botoes_ui[p_id].disabled = True
                self.botoes_ui[p_id].background_color = (0.95, 0.54, 0.65, 1)
                self.labels_ui[p_id].text = f"Registado às: {hora_gravada}"
                self.labels_ui[p_id].color = (0.95, 0.54, 0.65, 1)
            else:
                self.botoes_ui[p_id].disabled = True
                self.botoes_ui[p_id].background_color = (0.27, 0.28, 0.35, 1)
                self.labels_ui[p_id].text = "Bloqueado"
                self.labels_ui[p_id].color = (0.42, 0.44, 0.55, 1)

        e1, s1, e2, s2 = [self.historico_botoes.get(p["id"]) for p in self.passos]

        if not e1:
            self.activar_ui_botao("Entrada_1", "Disponível para registo")
        elif e1 and not s1 and not e2 and not s2:
            self.activar_ui_botao("Saida_1", "Disponível para Almoço")
            self.activar_ui_botao("Saida_2", "Disponível para Fim de dia direto")
        elif s1 and not e2:
            self.activar_ui_botao("Entrada_2", "Disponível para Regresso")
        elif e2 and not s2:
            self.activar_ui_botao("Saida_2", "Disponível para Fim do Dia")

    def activar_ui_botao(self, p_id, texto_status):
        self.botoes_ui[p_id].disabled = False
        self.botoes_ui[p_id].background_color = (0.65, 0.89, 0.63, 1)
        self.labels_ui[p_id].text = texto_status
        self.labels_ui[p_id].color = (0.65, 0.89, 0.63, 1)

    def clique_passo(self, passo_id):
        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M:%S")
        timestamp_completo = agora.strftime("%Y-%m-%d %H:%M:%S")
        tipo_registo = next(p["tipo"] for p in self.passos if p["id"] == passo_id)

        self.historico_botoes[passo_id] = hora_formatada
        self.salvar_estado_botoes()

        registo = {"timestamp": timestamp_completo, "tipo": tipo_registo, "nome": self.colaborador_nome}
        self.guardar_localmente(registo)
        self.guardar_no_historico_seguro(registo)

        if passo_id == "Saida_2":
            self.exibir_popup_mensagem("Ponto Encerrado", "Dia terminado. O ponto é reiniciado, obrigado e bom descanso!")
            self.historico_botoes = {}
            self.salvar_estado_botoes()

        self.atualizar_bloqueios_sequenciais()
        self.sincronizar_dados_offline()
    def guardar_localmente(self, registo):
        dados = {"registos": []}
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                try: dados = json.load(f)
                except: pass
        dados["registos"].append(registo)
        with open(self.db_path, "w") as f: json.dump(dados, f, indent=4)

    def guardar_no_historico_seguro(self, registo):
        dados = {"historico": []}
        if os.path.exists(self.backup_path):
            with open(self.backup_path, "r") as f:
                try: dados = json.load(f)
                except: pass
        dados["historico"].append(registo)
        with open(self.backup_path, "w") as f: json.dump(dados, f, indent=4)

    def solicitar_limpeza_historico(self, instance):
        if not os.path.exists(self.backup_path):
            self.exibir_popup_mensagem("Limpar Memória", "O seu livro de ponto já está completamente vazio.")
            return
        with open(self.backup_path, "r") as f:
            try:
                dados = json.load(f)
                historico = dados.get("historico", [])
            except: historico = []
            
        if not historico:
            self.exibir_popup_mensagem("Limpar Memória", "O seu livro de ponto já está completamente vazio.")
            return

        p_data = historico[0]["timestamp"]
        u_data = historico[-1]["timestamp"]

        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=f"Isto vai apagar o seu livro de ponto de\n{p_data}\na\n{u_data}.\n\nInserir PIN de administrador:", halign='center'))
        pin_in = TextInput(password=True, multiline=False, halign='center', size_hint_y=None, height='40dp')
        box.add_widget(pin_in)
        btn = Button(text="Confirmar Limpeza", size_hint_y=None, height='45dp', background_color=(0.95, 0.54, 0.65, 1))
        box.add_widget(btn)
        popup = Popup(title="AVISO CRÍTICO", content=box, size_hint=(0.9, 0.6))
        
        def confirmar(inst):
            if pin_in.text.strip() == self.pin_mestre:
                if os.path.exists(self.backup_path): os.remove(self.backup_path)
                popup.dismiss()
                self.exibir_popup_mensagem("Sucesso", "A memória do livro de ponto foi limpa!")
        btn.bind(on_press=confirmar)
        popup.open()

    def carregar_configuracoes(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                try:
                    config = json.load(f)
                    return config.get("ip", "127.0.0.1"), config.get("porta", "5000"), config.get("nome", "Novo Colaborador"), config.get("pin_mestre", "1234")
                except: pass
        return "127.0.0.1", "5000", "Sem Nome", "1234"

    def salvar_configuracoes(self, novo_ip, nova_porta, novo_nome, novo_pin):
        with open(self.config_path, "w") as f:
            json.dump({"ip": novo_ip, "porta": nova_porta, "nome": novo_nome, "pin_mestre": novo}, f, indent=4)
        self.servidor_ip, self.servidor_porta, self.colaborador_nome, self.pin_mestre = novo_ip, nova_porta, novo_nome, novo
        self.lbl_user.text = f"Colaborador: {self.colaborador_nome}"

    def carregar_estado_botoes(self):
        if os.path.exists(self.estado_path):
            with open(self.estado_path, "r") as f:
                try: return json.load(f)
                except: pass
        return {}

    def salvar_estado_botoes(self):
        with open(self.estado_path, "w") as f: json.dump(self.historico_botoes, f, indent=4)

    def sincronizar_dados_offline(self):
        if not os.path.exists(self.db_path): return
        with open(self.db_path, "r") as f:
            try: dados = json.load(f)
            except: return
        if not dados.get("registos"): return
        url = f"http://{self.servidor_ip}:{self.servidor_porta}/ponto"
        UrlRequest(url, req_body=json.dumps(dados), req_headers={'Content-type': 'application/json'}, on_success=self.on_sinc_sucesso, timeout=4)

    def on_sinc_sucesso(self, req, res):
        with open(self.db_path, "w") as f: json.dump({"registos": []}, f)

    def validar_acesso_admin(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text="Inserir PIN de administrador:"))
        pin_in = TextInput(password=True, multiline=False, halign='center', size_hint_y=None, height='40dp')
        box.add_widget(pin_in)
        btn = Button(text="Validar", size_hint_y=None, height='40dp')
        box.add_widget(btn)
        popup = Popup(title="Acesso Restrito", content=box, size_hint=(0.8, 0.4))
        
        def verificar(inst):
            if pin_in.text.strip() == self.pin_mestre:
                popup.dismiss()
                self.abrir_painel_config()
        btn.bind(on_press=verify := verificar)
        popup.open()

    def abrir_painel_config(self):
        box = BoxLayout(orientation='vertical', padding=10, spacing=5)
        inputs = {}
        campos = [("nome", "Nome de Colaborador:", self.colaborador_nome), ("pin", "Novo PIN de administrador:", self.pin_mestre), ("ip", "IP Servidor:", self.servidor_ip), ("porta", "Porta:", self.servidor_porta)]
        
        for key, label, val in campos:
            box.add_widget(Label(text=label, size_hint_y=None, height='20dp'))
            inp = TextInput(text=val, multiline=False, halign='center', size_hint_y=None, height='35dp')
            box.add_widget(inp)
            inputs[key] = inp
            
        btn_g = Button(text="GRAVAR", size_hint_y=None, height='40dp', bold=True)
        box.add_widget(btn_g)
        popup = Popup(title="Painel Patrão", content=box, size_hint=(0.9, 0.8))
        
        def salvar(inst):
            self.salvar_configuracoes(inputs["ip"].text.strip(), inputs["porta"].text.strip(), inputs["nome"].text.strip(), inputs["pin"].text.strip())
            popup.dismiss()
            self.sincronizar_dados_offline()
        btn_g.bind(on_press=salvar)
        popup.open()

    def exibir_popup_mensagem(self, titulo, mensagem):
        box = BoxLayout(orientation='vertical', padding=10)
        box.add_widget(Label(text=mensagem, halign='center', valign='middle'))
        popup = Popup(title=titulo, content=box, size_hint=(0.85, 0.4))
        popup.open()

if __name__ == '__main__':
    PontoApp().run()
