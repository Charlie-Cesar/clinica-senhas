"""As filas de uma especialidade médica."""

from collections import deque
from datetime import datetime

from clinica.config import CATEGORIAS, PREFERENCIAIS_POR_NORMAL
from clinica.senha import Senha


class FilaVazia(Exception):
    """Erro usado quando alguém tenta chamar uma senha e não há ninguém esperando."""


class FilaEspecialidade:
    """Guarda as filas de UMA especialidade: uma fila FIFO para cada categoria."""

    def __init__(self, sigla):
        self.sigla = sigla  # ex.: "CG"

        # Uma fila FIFO (deque) para cada categoria.
        # self.filas["N"] é a fila dos normais e self.filas["P"] a dos preferenciais.
        self.filas = {"N": deque(), "P": deque()}

        # Contadores separados por categoria: N001, N002... e P001, P002...
        self.contadores = {"N": 0, "P": 0}

        # Quantos preferenciais foram chamados desde o último normal.
        # É o que permite aplicar a política 2:1.
        self.preferenciais_seguidos = 0

    def emitir(self, categoria):
        """Gera a próxima senha da categoria e coloca no FIM da fila (inserção)."""
        if categoria not in CATEGORIAS:
            raise ValueError(f"Categoria inválida: {categoria}. Use N ou P.")

        self.contadores[categoria] += 1
        senha = Senha(self.sigla, categoria, self.contadores[categoria])
        self.filas[categoria].append(senha)
        return senha

    def _categoria_da_vez(self, tem_preferencial, tem_normal, preferenciais_seguidos):
        """Aplica a política de prioridade: diz de qual fila sai o próximo.

        Devolve "P", "N" ou None (quando as duas filas estão vazias).
        Recebe tudo por parâmetro, sem mexer nas filas, para poder ser
        reaproveitada depois no cálculo da ordem prevista.
        """
        if not tem_preferencial and not tem_normal:
            return None
        if not tem_normal:          # só tem preferencial esperando
            return "P"
        if not tem_preferencial:    # só tem normal esperando
            return "N"
        # As duas filas têm gente: preferencial até completar o limite seguido
        if preferenciais_seguidos < PREFERENCIAIS_POR_NORMAL:
            return "P"
        return "N"

    def chamar_proximo(self):
        """Tira a próxima senha da fila certa (remoção) e devolve ela."""
        categoria = self._categoria_da_vez(
            len(self.filas["P"]) > 0,
            len(self.filas["N"]) > 0,
            self.preferenciais_seguidos,
        )
        if categoria is None:
            raise FilaVazia("Não há pacientes aguardando nesta especialidade.")

        senha = self.filas[categoria].popleft()  # FIFO: sai o primeiro que entrou
        senha.chamada_em = datetime.now()

        # Atualiza a contagem usada pela política 2:1
        if categoria == "P":
            self.preferenciais_seguidos += 1
        else:
            self.preferenciais_seguidos = 0

        return senha

    def aguardando(self):
        """Quantos pacientes estão esperando nesta especialidade (as duas filas)."""
        return len(self.filas["N"]) + len(self.filas["P"])

    def ordem_prevista(self):
        """Lista as senhas na ordem em que serão chamadas, SEM tirar ninguém das filas.

        Simula várias chamadas seguidas usando a mesma política do
        chamar_proximo(), mas só "anda" por cópias das filas.
        """
        preferenciais = list(self.filas["P"])  # cópias: as filas reais não mudam
        normais = list(self.filas["N"])
        seguidos = self.preferenciais_seguidos

        ordem = []
        p = 0  # quantos preferenciais já entraram na simulação
        n = 0  # quantos normais já entraram na simulação
        while True:
            categoria = self._categoria_da_vez(p < len(preferenciais), n < len(normais), seguidos)
            if categoria is None:  # acabaram as duas filas
                break
            if categoria == "P":
                ordem.append(preferenciais[p])
                p += 1
                seguidos += 1
            else:
                ordem.append(normais[n])
                n += 1
                seguidos = 0
        return ordem


# Este bloco só roda quando o arquivo é executado direto
# (python -m clinica.fila_especialidade), e não quando ele é importado.
if __name__ == "__main__":
    cardiologia = FilaEspecialidade("CA")

    print("--- Emissão (ordem de chegada) ---")
    for categoria in ["N", "N", "P", "N", "P", "P"]:
        print("Senha emitida:", cardiologia.emitir(categoria))

    print("--- Chamada (política 2:1) ---")
    for i in range(7):
        try:
            print("Chamando:", cardiologia.chamar_proximo())
        except FilaVazia as erro:
            print("Erro tratado:", erro)
