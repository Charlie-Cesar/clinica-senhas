"""O gerenciador da clínica: junta as filas das 3 especialidades e o histórico."""

from clinica.config import ESPECIALIDADES, TEMPO_MEDIO_ATENDIMENTO
from clinica.fila_especialidade import FilaEspecialidade, FilaVazia


class GerenciadorClinica:
    """Ponto único de acesso à lógica. A interface gráfica só conversa com esta classe."""

    def __init__(self):
        # Um objeto FilaEspecialidade para cada especialidade: {"CG": ..., "CA": ..., "OR": ...}
        self.especialidades = {}
        for sigla in ESPECIALIDADES:
            self.especialidades[sigla] = FilaEspecialidade(sigla)

        self.historico = []          # senhas já chamadas, da mais antiga para a mais nova
        self.ultima_chamada = None   # a senha chamada por último (para o painel)

    def _fila(self, sigla):
        """Devolve a FilaEspecialidade da sigla, ou dá erro se a sigla não existir."""
        if sigla not in self.especialidades:
            raise ValueError(f"Especialidade inválida: {sigla}.")
        return self.especialidades[sigla]

    def emitir_senha(self, sigla, categoria):
        """Emite uma senha N ou P na especialidade escolhida."""
        return self._fila(sigla).emitir(categoria)

    def chamar_proximo(self, sigla):
        """Chama a próxima senha da especialidade e registra no histórico.

        Se não houver ninguém esperando, o FilaVazia sobe para quem chamou.
        """
        senha = self._fila(sigla).chamar_proximo()
        self.historico.append(senha)
        self.ultima_chamada = senha
        return senha

    def aguardando(self, sigla=None):
        """Pacientes esperando numa especialidade, ou no total se a sigla não for informada."""
        if sigla is not None:
            return self._fila(sigla).aguardando()
        total = 0
        for fila in self.especialidades.values():
            total += fila.aguardando()
        return total

    def ordem_com_tempo(self, sigla):
        """Lista de (senha, minutos de espera) na ordem prevista de atendimento."""
        resultado = []
        # enumerate devolve a posição junto com cada item: 0, 1, 2...
        # A posição é exatamente quantos pacientes estão à frente.
        for a_frente, senha in enumerate(self._fila(sigla).ordem_prevista()):
            resultado.append((senha, a_frente * TEMPO_MEDIO_ATENDIMENTO))
        return resultado

    def consultar_espera(self, codigo):
        """Recebe um código (ex.: "ca-n002") e devolve (pacientes à frente, minutos)."""
        codigo = codigo.strip().upper()   # aceita espaços e letras minúsculas
        if codigo == "":
            raise ValueError("Digite o código de uma senha.")

        sigla = codigo.split("-")[0]      # "CA-N002" -> "CA"
        for senha, minutos in self.ordem_com_tempo(sigla):
            if senha.codigo() == codigo:
                return minutos // TEMPO_MEDIO_ATENDIMENTO, minutos
        raise ValueError(f"A senha {codigo} não está aguardando (não existe ou já foi chamada).")


# Demonstração: python -m clinica.gerenciador
if __name__ == "__main__":
    clinica = GerenciadorClinica()

    for sigla, categoria in [("CA", "N"), ("CA", "N"), ("CG", "P"), ("CA", "P"), ("CA", "N"), ("CA", "P")]:
        print("Emitida:", clinica.emitir_senha(sigla, categoria))

    print("\n--- Ordem prevista da Cardiologia ---")
    for senha, minutos in clinica.ordem_com_tempo("CA"):
        print(f"{senha}  ->  {minutos} min")

    a_frente, minutos = clinica.consultar_espera("ca-n002")
    print(f"\nConsulta CA-N002: {a_frente} à frente = {minutos} min")

    print("\n--- Chamando 2 da Cardiologia ---")
    print("Chamando:", clinica.chamar_proximo("CA"))
    print("Chamando:", clinica.chamar_proximo("CA"))

    a_frente, minutos = clinica.consultar_espera("CA-N002")
    print(f"Consulta CA-N002 de novo: {a_frente} à frente = {minutos} min")

    print("\nAguardando: Cardiologia =", clinica.aguardando("CA"), "| total =", clinica.aguardando())
    print("Histórico:", [str(s) for s in clinica.historico])
    print("Última chamada:", clinica.ultima_chamada)

    print("\n--- Situações de erro ---")
    try:
        clinica.chamar_proximo("OR")           # Ortopedia está vazia
    except FilaVazia as erro:
        print("Erro tratado:", erro)

    try:
        clinica.emitir_senha("XX", "N")        # especialidade que não existe
    except ValueError as erro:
        print("Erro tratado:", erro)

    try:
        clinica.consultar_espera("CA-P001")    # essa senha já foi chamada
    except ValueError as erro:
        print("Erro tratado:", erro)
