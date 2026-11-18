"""Configurações fixas do sistema."""

# Especialidades atendidas pela clínica: sigla -> nome completo.
# A sigla entra no código da senha (ex.: CG-N001), o que evita
# confundir a N001 da Cardiologia com a N001 da Ortopedia.
ESPECIALIDADES = {
    "CG": "Clínica Geral",
    "CA": "Cardiologia",
    "OR": "Ortopedia",
}

# Categorias de atendimento: letra -> nome completo.
CATEGORIAS = {
    "N": "Normal",
    "P": "Preferencial",
}
