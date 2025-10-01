import os
from typing import List

# CONFIGURAÇÕES E CONSTANTES 

# URL base da API do IBGE para consulta de nomes
IBGE_API_BASE_URL = "https://servicodados.ibge.gov.br/api/v2/censos/nomes"

# Timeout para a requisição da API (em segundos)
REQUEST_TIMEOUT = 10

# 1. CAMINHO COMPLETO PARA A PASTA COM SEUS ARQUIVOS ORIGINAIS
# ATENÇÃO: Substitua o caminho dos arquivos originais!
PASTA_PLANILHAS_ORIGINAIS = r'C:\Users\bdbernardino\Documents\Projeto_Mudança_Sexo\PlanilhasParaProcessar' 

# 2. NOME EXATO DA COLUNA QUE CONTÉM O NOME COMPLETO
NOME_COLUNA_ENTRADA = 'NM_BENEF:' 

# ATENÇÃO: SUBSTITUA COM OS NOMES EXATOS DAS SUAS COLUNAS DE DATA
COLUNAS_PARA_FORMATAR_DATA: list[str] = [
    'DT_INCL:',
    'DT_NASC:',
]

# 3. CONFIGURAÇÃO DA PASTA DE SAÍDA
# O nome da subpasta que será criada dentro da PASTA_PLANILHAS_ORIGINAIS para salvar os resultados
PASTA_SAIDA_NOME = 'Planilhas_Transformadas'

# 4. PREFIXO DO ARQUIVO DE SAÍDA
PREFIXO_SAIDA = 'Tratado_'

# Caminho completo para a pasta onde os arquivos processados serão salvos
PASTA_PLANILHAS_SAIDA = os.path.join(PASTA_PLANILHAS_ORIGINAIS, PASTA_SAIDA_NOME)