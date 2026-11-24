"""Testes automáticos da lógica das filas.

Rodar (na pasta do projeto):  python -m unittest discover -s tests -v
"""

import unittest

from clinica.fila_especialidade import FilaVazia
from clinica.gerenciador import GerenciadorClinica


def codigos(senhas):
    """Transforma uma lista de senhas numa lista de códigos, para comparar fácil."""
    return [senha.codigo() for senha in senhas]


class TestEmissao(unittest.TestCase):

    def setUp(self):
        # Roda antes de CADA teste: todo teste começa com uma clínica nova e vazia
        self.clinica = GerenciadorClinica()

    def test_numeracao_separada_por_categoria(self):
        emitidas = [self.clinica.emitir_senha("CA", c) for c in ["N", "N", "P", "N"]]
        self.assertEqual(codigos(emitidas), ["CA-N001", "CA-N002", "CA-P001", "CA-N003"])

    def test_numeracao_independente_por_especialidade(self):
        self.clinica.emitir_senha("CA", "N")
        senha_cg = self.clinica.emitir_senha("CG", "N")
        self.assertEqual(senha_cg.codigo(), "CG-N001")

    def test_categoria_invalida_gera_erro(self):
        with self.assertRaises(ValueError):
            self.clinica.emitir_senha("CA", "X")

    def test_especialidade_invalida_gera_erro(self):
        with self.assertRaises(ValueError):
            self.clinica.emitir_senha("XX", "N")


class TestChamada(unittest.TestCase):

    def setUp(self):
        self.clinica = GerenciadorClinica()

    def chamar(self, sigla, vezes):
        return codigos([self.clinica.chamar_proximo(sigla) for _ in range(vezes)])

    def test_fifo_dentro_da_mesma_categoria(self):
        for _ in range(3):
            self.clinica.emitir_senha("CG", "N")
        self.assertEqual(self.chamar("CG", 3), ["CG-N001", "CG-N002", "CG-N003"])

    def test_preferencial_passa_na_frente_de_normal_que_chegou_antes(self):
        self.clinica.emitir_senha("CA", "N")   # chegou primeiro
        self.clinica.emitir_senha("CA", "P")   # chegou depois
        self.assertEqual(self.chamar("CA", 1), ["CA-P001"])

    def test_politica_2_preferenciais_para_1_normal(self):
        for c in ["N", "N", "P", "P", "P", "P"]:
            self.clinica.emitir_senha("OR", c)
        self.assertEqual(
            self.chamar("OR", 6),
            ["OR-P001", "OR-P002", "OR-N001", "OR-P003", "OR-P004", "OR-N002"],
        )

    def test_fila_vazia_gera_erro_tratavel(self):
        with self.assertRaises(FilaVazia):
            self.clinica.chamar_proximo("CG")

    def test_chamada_vai_para_historico_e_ultima_chamada(self):
        self.clinica.emitir_senha("CA", "N")
        self.clinica.emitir_senha("CG", "P")
        self.chamar("CA", 1)
        self.chamar("CG", 1)
        self.assertEqual(codigos(self.clinica.historico), ["CA-N001", "CG-P001"])
        self.assertEqual(self.clinica.ultima_chamada.codigo(), "CG-P001")

    def test_aguardando_diminui_ao_chamar(self):
        for c in ["N", "P", "N"]:
            self.clinica.emitir_senha("CA", c)
        self.assertEqual(self.clinica.aguardando("CA"), 3)
        self.chamar("CA", 1)
        self.assertEqual(self.clinica.aguardando("CA"), 2)

    def test_aguardando_por_categoria(self):
        for c in ["N", "P", "N"]:
            self.clinica.emitir_senha("CA", c)
        self.assertEqual(self.clinica.aguardando_por_categoria("CA"), {"N": 2, "P": 1})


class TestTempoDeEspera(unittest.TestCase):

    def setUp(self):
        self.clinica = GerenciadorClinica()
        # Ordem prevista na Cardiologia: P001, P002, N001, N002
        for c in ["N", "N", "P", "P"]:
            self.clinica.emitir_senha("CA", c)

    def test_tempo_e_pacientes_a_frente_vezes_30(self):
        self.assertEqual(self.clinica.consultar_espera("CA-N002"), (3, 90))
        self.assertEqual(self.clinica.consultar_espera("CA-P001"), (0, 0))

    def test_consulta_aceita_minusculas_e_espacos(self):
        self.assertEqual(self.clinica.consultar_espera("  ca-n001 "), (2, 60))

    def test_tempo_atualiza_depois_de_chamar(self):
        self.clinica.chamar_proximo("CA")
        self.assertEqual(self.clinica.consultar_espera("CA-N002"), (2, 60))

    def test_ordem_prevista_nao_tira_ninguem_da_fila(self):
        self.clinica.ordem_com_tempo("CA")
        self.assertEqual(self.clinica.aguardando("CA"), 4)

    def test_senha_ja_chamada_gera_erro(self):
        self.clinica.chamar_proximo("CA")   # chama CA-P001
        with self.assertRaises(ValueError):
            self.clinica.consultar_espera("CA-P001")

    def test_consulta_vazia_gera_erro(self):
        with self.assertRaises(ValueError):
            self.clinica.consultar_espera("   ")


if __name__ == "__main__":
    unittest.main()
