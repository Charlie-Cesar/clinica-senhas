"""Ajudas usadas por várias abas para mostrar as especialidades."""

from clinica.config import ESPECIALIDADES

# Textos que aparecem nas listas de escolha: ["CG - Clínica Geral", "CA - Cardiologia", ...]
OPCOES_ESPECIALIDADES = [f"{sigla} - {nome}" for sigla, nome in ESPECIALIDADES.items()]


def sigla_da_opcao(texto):
    """Transforma o texto escolhido na tela na sigla usada pela lógica.

    Exemplo: "CA - Cardiologia" -> "CA"
    """
    return texto.split(" - ")[0]
