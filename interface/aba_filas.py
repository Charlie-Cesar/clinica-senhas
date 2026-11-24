"""Aba de gerenciamento das filas: mostra quem espera e chama o próximo."""

import tkinter as tk
from tkinter import messagebox, ttk

from clinica.config import CATEGORIAS
from clinica.fila_especialidade import FilaVazia
from interface.opcoes import OPCOES_ESPECIALIDADES, sigla_da_opcao


class AbaFilas(ttk.Frame):
    """Mostra a fila de uma especialidade na ordem prevista e chama o próximo."""

    TITULO = "Filas e Chamada"

    def __init__(self, master, app):
        super().__init__(master, padding=20)
        self.app = app

        # Já começa com a primeira especialidade escolhida
        self.especialidade = tk.StringVar(value=OPCOES_ESPECIALIDADES[0])

        # --- Linha de cima: escolha da especialidade + botão de chamar ---
        topo = ttk.Frame(self)
        topo.pack(fill="x")
        ttk.Label(topo, text="Especialidade:", font=("Segoe UI", 11, "bold")).pack(side="left")
        combo = ttk.Combobox(topo, textvariable=self.especialidade, values=OPCOES_ESPECIALIDADES,
                             state="readonly", width=28)
        combo.pack(side="left", padx=8)
        # Evento: quando o usuário troca a especialidade, a tabela é recarregada
        combo.bind("<<ComboboxSelected>>", self.ao_trocar_especialidade)
        ttk.Button(topo, text="Chamar próximo", command=self.chamar).pack(side="right")

        # --- Contagem ---
        self.rotulo_contagem = ttk.Label(self, text="", font=("Segoe UI", 11))
        self.rotulo_contagem.pack(anchor="w", pady=(14, 6))

        # --- Tabela com a ordem prevista de atendimento ---
        colunas = ("posicao", "senha", "categoria", "espera")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=12)
        titulos = {"posicao": "Posição", "senha": "Senha", "categoria": "Categoria",
                   "espera": "Espera estimada"}
        for coluna in colunas:
            self.tabela.heading(coluna, text=titulos[coluna])
            self.tabela.column(coluna, anchor="center", width=140)
        self.tabela.pack(fill="both", expand=True)

        # --- Resultado da última chamada feita por esta aba ---
        self.rotulo_chamada = ttk.Label(self, text="", font=("Segoe UI", 14, "bold"),
                                        foreground="#1f4e79")
        self.rotulo_chamada.pack(pady=(12, 0))

    def ao_trocar_especialidade(self, evento):
        self.atualizar()

    def chamar(self):
        """Chamado pelo botão "Chamar próximo" (evento)."""
        sigla = sigla_da_opcao(self.especialidade.get())
        try:
            senha = self.app.clinica.chamar_proximo(sigla)
        except FilaVazia as erro:
            # Exceção tratada: avisa em vez de travar o programa
            messagebox.showinfo("Fila vazia", str(erro))
            return

        self.rotulo_chamada.config(
            text=f"Chamando: {senha.codigo()}  ({CATEGORIAS[senha.categoria]})")
        self.app.atualizar_tudo()

    def atualizar(self):
        """Recarrega a contagem e a tabela com os dados atuais do gerenciador."""
        sigla = sigla_da_opcao(self.especialidade.get())
        por_categoria = self.app.clinica.aguardando_por_categoria(sigla)
        self.rotulo_contagem.config(
            text=f"Aguardando: {self.app.clinica.aguardando(sigla)}   "
                 f"(Preferenciais: {por_categoria['P']}  |  Normais: {por_categoria['N']})")

        # Apaga as linhas antigas e escreve tudo de novo
        self.tabela.delete(*self.tabela.get_children())
        for posicao, (senha, minutos) in enumerate(self.app.clinica.ordem_com_tempo(sigla), start=1):
            self.tabela.insert("", "end", values=(
                f"{posicao}º", senha.codigo(), CATEGORIAS[senha.categoria], f"{minutos} min"))
