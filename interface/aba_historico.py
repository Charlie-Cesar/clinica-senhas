"""Aba do histórico de atendimentos (senhas já chamadas)."""

from tkinter import ttk

from clinica.config import CATEGORIAS, ESPECIALIDADES


class AbaHistorico(ttk.Frame):
    """Lista todas as senhas chamadas, da mais recente para a mais antiga."""

    TITULO = "Histórico"

    def __init__(self, master, app):
        super().__init__(master, padding=20)
        self.app = app

        self.rotulo_total = ttk.Label(self, text="", font=("Segoe UI", 11, "bold"))
        self.rotulo_total.pack(anchor="w", pady=(0, 8))

        colunas = ("ordem", "senha", "especialidade", "categoria", "emitida", "chamada")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=14)
        titulos = {"ordem": "Nº", "senha": "Senha", "especialidade": "Especialidade",
                   "categoria": "Categoria", "emitida": "Emitida às", "chamada": "Chamada às"}
        larguras = {"ordem": 50, "senha": 100, "especialidade": 150,
                    "categoria": 110, "emitida": 100, "chamada": 100}
        for coluna in colunas:
            self.tabela.heading(coluna, text=titulos[coluna])
            self.tabela.column(coluna, anchor="center", width=larguras[coluna])
        self.tabela.pack(fill="both", expand=True)

    def atualizar(self):
        historico = self.app.clinica.historico
        self.rotulo_total.config(text=f"Pacientes atendidos: {len(historico)}")

        self.tabela.delete(*self.tabela.get_children())
        # reversed: a chamada mais recente aparece no topo da tabela
        for numero, senha in reversed(list(enumerate(historico, start=1))):
            self.tabela.insert("", "end", values=(
                numero,
                senha.codigo(),
                ESPECIALIDADES[senha.especialidade],
                CATEGORIAS[senha.categoria],
                senha.emitida_em.strftime("%H:%M:%S"),   # hora no formato 14:05:32
                senha.chamada_em.strftime("%H:%M:%S"),
            ))
