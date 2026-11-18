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

# Política de prioridade (alternada): quantos preferenciais são chamados
# seguidos antes de chamar 1 normal. Com 2, a ordem fica P, P, N, P, P, N...
# Assim o preferencial tem prioridade, mas o normal não espera para sempre.
PREFERENCIAIS_POR_NORMAL = 2
