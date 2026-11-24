"""Painel de atendimento: o "telão" da sala de espera."""

import tkinter as tk
from tkinter import ttk

from clinica.config import CATEGORIAS, ESPECIALIDADES

FUNDO = "#102a43"  # cor de fundo do telão


class AbaPainel(ttk.Frame):
    """Mostra a última senha chamada e as senhas em espera de cada especialidade."""

    TITULO = "Painel de Atendimento"

    def __init__(self, master, app):
        super().__init__(master, padding=10)
        self.app = app

        # --- Telão com a última senha chamada ---
        tela = tk.Frame(self, bg=FUNDO)
        tela.pack(fill="x")
        tk.Label(tela, text="ÚLTIMA SENHA CHAMADA", bg=FUNDO, fg="#9fb3c8",
                 font=("Segoe UI", 12, "bold")).pack(pady=(14, 0))
        self.rotulo_senha = tk.Label(tela, text="", bg=FUNDO, fg="white",
                                     font=("Segoe UI", 54, "bold"))
        self.rotulo_senha.pack()
        self.rotulo_info = tk.Label(tela, text="", bg=FUNDO, fg="#f0b429", font=("Segoe UI", 16))
        self.rotulo_info.pack(pady=(0, 14))

        # --- Total aguardando ---
        self.rotulo_total = ttk.Label(self, text="", font=("Segoe UI", 12, "bold"))
        self.rotulo_total.pack(pady=(10, 6))

        # --- Uma coluna por especialidade com as senhas em espera ---
        colunas = ttk.Frame(self)
        colunas.pack(fill="both", expand=True)
        self.colunas = {}  # sigla -> (rótulo do título, lista de senhas)
        for sigla, nome in ESPECIALIDADES.items():
            caixa = ttk.Frame(colunas, padding=5)
            caixa.pack(side="left", fill="both", expand=True)
            titulo = ttk.Label(caixa, text=nome, font=("Segoe UI", 11, "bold"))
            titulo.pack()
            lista = tk.Listbox(caixa, height=8, font=("Consolas", 12), justify="center")
            lista.pack(fill="both", expand=True)
            self.colunas[sigla] = (titulo, lista)

    def atualizar(self):
        """Redesenha o painel com os dados atuais do gerenciador."""
        ultima = self.app.clinica.ultima_chamada
        if ultima is None:
            self.rotulo_senha.config(text="---")
            self.rotulo_info.config(text="Nenhuma senha chamada ainda")
        else:
            self.rotulo_senha.config(text=ultima.codigo())
            self.rotulo_info.config(
                text=f"{ESPECIALIDADES[ultima.especialidade]}  •  {CATEGORIAS[ultima.categoria]}")

        self.rotulo_total.config(text=f"Total de pacientes aguardando: {self.app.clinica.aguardando()}")

        for sigla, (titulo, lista) in self.colunas.items():
            titulo.config(text=f"{ESPECIALIDADES[sigla]} ({self.app.clinica.aguardando(sigla)})")
            lista.delete(0, "end")
            for senha, minutos in self.app.clinica.ordem_com_tempo(sigla):
                lista.insert("end", senha.codigo())
