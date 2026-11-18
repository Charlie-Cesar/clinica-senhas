"""As filas de uma especialidade médica."""

from collections import deque

from clinica.config import CATEGORIAS
from clinica.senha import Senha


class FilaEspecialidade:
    """Guarda as filas de UMA especialidade: uma fila FIFO para cada categoria."""

    def __init__(self, sigla):
        self.sigla = sigla  # ex.: "CG"

        # Uma fila FIFO (deque) para cada categoria.
        # self.filas["N"] é a fila dos normais e self.filas["P"] a dos preferenciais.
        self.filas = {"N": deque(), "P": deque()}

        # Contadores separados por categoria: N001, N002... e P001, P002...
        self.contadores = {"N": 0, "P": 0}

    def emitir(self, categoria):
        """Gera a próxima senha da categoria e coloca no FIM da fila (inserção)."""
        if categoria not in CATEGORIAS:
            raise ValueError(f"Categoria inválida: {categoria}. Use N ou P.")

        self.contadores[categoria] += 1
        senha = Senha(self.sigla, categoria, self.contadores[categoria])
        self.filas[categoria].append(senha)
        return senha


# Este bloco só roda quando o arquivo é executado direto
# (python -m clinica.fila_especialidade), e não quando ele é importado.
if __name__ == "__main__":
    cardiologia = FilaEspecialidade("CA")

    for categoria in ["N", "N", "P", "N", "P"]:
        senha = cardiologia.emitir(categoria)
        print("Senha emitida:", senha)

    print("Fila normal:      ", [str(s) for s in cardiologia.filas["N"]])
    print("Fila preferencial:", [str(s) for s in cardiologia.filas["P"]])

    try:
        cardiologia.emitir("X")
    except ValueError as erro:
        print("Erro tratado:", erro)
