"""Janela principal do sistema."""

import tkinter as tk
from tkinter import ttk

from clinica.gerenciador import GerenciadorClinica
from interface.aba_emissao import AbaEmissao
from interface.aba_filas import AbaFilas
from interface.aba_historico import AbaHistorico
from interface.aba_painel import AbaPainel
from interface.aba_tempo import AbaTempo


class App(tk.Tk):
    """A janela do sistema: um título no topo e as funcionalidades em abas."""

    def __init__(self):
        super().__init__()  # cria a janela do Tkinter
        self.title("Sistema de Gerenciamento de Senhas - Clínica")
        self.geometry("820x560")
        self.minsize(720, 500)

        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TNotebook.Tab", padding=(16, 6), font=("Segoe UI", 10))

        # UM único gerenciador para o sistema inteiro: todas as abas usam o mesmo.
        # Se cada aba criasse o seu, as filas ficariam separadas.
        self.clinica = GerenciadorClinica()

        # Cabeçalho com o nome do sistema
        topo = tk.Frame(self, bg="#1f4e79")
        topo.pack(fill="x")
        tk.Label(topo, text="Clínica - Gerenciamento de Senhas", bg="#1f4e79", fg="white",
                 font=("Segoe UI", 16, "bold"), pady=10).pack()

        # As abas (Notebook). Cada aba é uma classe em um arquivo próprio.
        self.abas = ttk.Notebook(self)
        self.abas.pack(fill="both", expand=True, padx=10, pady=10)

        self.lista_abas = [
            AbaEmissao(self.abas, self),
            AbaFilas(self.abas, self),
            AbaPainel(self.abas, self),
            AbaTempo(self.abas, self),
            AbaHistorico(self.abas, self),
        ]
        for aba in self.lista_abas:
            self.abas.add(aba, text=aba.TITULO)

        self.atualizar_tudo()

    def atualizar_tudo(self):
        """Pede para todas as abas mostrarem os dados mais recentes.
 
        É chamada depois de toda emissão ou chamada, para a tela nunca
        ficar desatualizada.
        """
        for aba in self.lista_abas:
            aba.atualizar()
