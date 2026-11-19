"""Aba de emissão de senhas."""

import tkinter as tk
from tkinter import messagebox, ttk

from clinica.config import CATEGORIAS, ESPECIALIDADES


class AbaEmissao(ttk.Frame):
    """O paciente escolhe a especialidade e a categoria e recebe a senha."""

    TITULO = "Emissão de Senhas"

    def __init__(self, master, app):
        super().__init__(master, padding=20)
        self.app = app  # acesso ao app.clinica e ao app.atualizar_tudo()

        # Variáveis do Tkinter: guardam o que o usuário escolheu na tela
        self.especialidade = tk.StringVar()
        self.categoria = tk.StringVar()

        # --- 1. Especialidade ---
        ttk.Label(self, text="1. Escolha a especialidade:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        # Na lista aparece "CG - Clínica Geral"; o sistema só usa a sigla (antes do " - ")
        opcoes = [f"{sigla} - {nome}" for sigla, nome in ESPECIALIDADES.items()]
        ttk.Combobox(self, textvariable=self.especialidade, values=opcoes,
                     state="readonly", width=30).pack(anchor="w", pady=(4, 16))

        # --- 2. Categoria ---
        ttk.Label(self, text="2. Escolha o tipo de atendimento:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        for letra, nome in CATEGORIAS.items():
            ttk.Radiobutton(self, text=f"{nome} ({letra})", variable=self.categoria,
                            value=letra).pack(anchor="w", pady=2)

        # --- 3. Botão ---
        ttk.Button(self, text="Emitir senha", command=self.emitir).pack(anchor="w", pady=16)

        # --- Resultado ---
        self.rotulo_senha = ttk.Label(self, text="", font=("Segoe UI", 40, "bold"), foreground="#1f4e79")
        self.rotulo_senha.pack(pady=(10, 0))
        self.rotulo_detalhes = ttk.Label(self, text="", font=("Segoe UI", 11), justify="center")
        self.rotulo_detalhes.pack()

    def emitir(self):
        """Chamado quando o botão "Emitir senha" é clicado (evento)."""
        # Validação: a interface confere se tudo foi escolhido antes de chamar a lógica
        if self.especialidade.get() == "":
            messagebox.showwarning("Atenção", "Escolha a especialidade.")
            return
        if self.categoria.get() == "":
            messagebox.showwarning("Atenção", "Escolha o tipo de atendimento (Normal ou Preferencial).")
            return

        sigla = self.especialidade.get().split(" - ")[0]
        try:
            senha = self.app.clinica.emitir_senha(sigla, self.categoria.get())
            a_frente, minutos = self.app.clinica.consultar_espera(senha.codigo())
        except ValueError as erro:
            messagebox.showerror("Operação inválida", str(erro))
            return

        self.rotulo_senha.config(text=senha.codigo())
        self.rotulo_detalhes.config(
            text=f"{ESPECIALIDADES[sigla]} - {CATEGORIAS[senha.categoria]}\n"
                 f"Pacientes à frente: {a_frente}   |   Espera estimada: {minutos} min"
        )
        self.app.atualizar_tudo()  # as outras abas passam a mostrar a senha nova

    def atualizar(self):
        """Esta aba não tem listas para recarregar; existe para seguir o padrão das outras."""
        pass
