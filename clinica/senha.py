"""Representa uma senha de atendimento."""

from datetime import datetime


class Senha:
    """Uma senha de atendimento, como CG-N001."""

    def __init__(self, especialidade, categoria, numero):
        self.especialidade = especialidade  # sigla, ex.: "CG"
        self.categoria = categoria          # "N" (normal) ou "P" (preferencial)
        self.numero = numero                # 1, 2, 3... (separado por categoria)
        self.emitida_em = datetime.now()    # hora em que a senha foi emitida
        self.chamada_em = None              # preenchida quando a senha for chamada

    def codigo(self):
        """Devolve o código que aparece para o paciente, ex.: CG-N001."""
        # :03d = número com 3 dígitos, completando com zeros à esquerda (1 -> 001)
        return f"{self.especialidade}-{self.categoria}{self.numero:03d}"

    def __str__(self):
        # Define o que aparece quando a senha é usada num print()
        return self.codigo()
