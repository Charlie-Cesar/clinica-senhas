"""Aba de consulta do tempo estimado de espera de uma senha."""

import tkinter as tk
from tkinter import messagebox, ttk

from clinica.config import TEMPO_MEDIO_ATENDIMENTO


class AbaTempo(ttk.Frame):
    """O paciente digita a senha e vê quantos estão à frente e o tempo estimado."""

    TITULO = "Tempo de Espera"

    def __init__(self, master, app):
        super().__init__(master, padding=20)
        self.app = app
        self.codigo = tk.StringVar()

        ttk.Label(self, text="Digite o código da senha (ex.: CA-N002):",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")

        linha = ttk.Frame(self)
        linha.pack(anchor="w", pady=(6, 16))
        campo = ttk.Entry(linha, textvariable=self.codigo, width=18, font=("Segoe UI", 12))
        campo.pack(side="left")
        # Evento: apertar Enter no campo tem o mesmo efeito do botão
        campo.bind("<Return>", self.ao_apertar_enter)
        ttk.Button(linha, text="Consultar", command=self.consultar).pack(side="left", padx=8)

        self.rotulo_resultado = ttk.Label(self, text="", font=("Segoe UI", 16, "bold"),
                                          foreground="#1f4e79", justify="left")
        self.rotulo_resultado.pack(anchor="w")

        ttk.Label(self, foreground="#555", justify="left", text=(
            f"Como é calculado: pacientes à frente x {TEMPO_MEDIO_ATENDIMENTO} min.\n"
            "A posição segue a política de prioridade (2 preferenciais para cada normal)\n"
            "e é atualizada sempre que uma senha é emitida ou chamada."
        )).pack(anchor="w", pady=(24, 0))

    def ao_apertar_enter(self, evento):
        self.consultar()

    def consultar(self):
        try:
            a_frente, minutos = self.app.clinica.consultar_espera(self.codigo.get())
        except ValueError as erro:
            # Entrada vazia, especialidade inexistente ou senha que não está na fila
            messagebox.showerror("Consulta inválida", str(erro))
            return

        codigo = self.codigo.get().strip().upper()
        if a_frente == 0:
            self.rotulo_resultado.config(text=f"{codigo}: você é o próximo a ser chamado!")
        else:
            self.rotulo_resultado.config(
                text=f"{codigo}: {a_frente} paciente(s) à frente\n"
                     f"Espera estimada: {minutos} min ({a_frente} x {TEMPO_MEDIO_ATENDIMENTO})")

    def atualizar(self):
        """Se já existe uma consulta na tela, refaz para o tempo nunca ficar velho."""
        if self.rotulo_resultado.cget("text") == "":
            return
        try:
            self.app.clinica.consultar_espera(self.codigo.get())
        except ValueError:
            self.rotulo_resultado.config(text="")  # a senha foi chamada: limpa o resultado
            return
        self.consultar()
