import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from config import IBGE_API_BASE_URL, REQUEST_TIMEOUT


# CONFIGURAÇÃO DE AMBIENTE

# Desativa avisos de insegurança no console ao usar verify=False.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# FUNÇÕES DE CLASSIFICAÇÃO

def _fetch_frequencia(nome: str, sexo_sigla: str) -> int:
    """
    Realiza a requisição ao IBGE e retorna a frequência total para um dado sexo.
    """
    url = f"{IBGE_API_BASE_URL}/{nome}?sexo={sexo_sigla}"
    
    try:
        # verify=False é crucial para contornar o erro de certificado SSL
        response = requests.get(url, verify=False, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        dados = response.json()
        
        if dados and 'res' in dados[0]:
            # Soma a frequência em todos os períodos
            return sum(item.get('frequencia', 0) for item in dados[0]['res'])
            
    except requests.exceptions.HTTPError as e:
        # Erros HTTP, exceto 404 (nome não encontrado), são logados
        if response.status_code != 404:
             print(f"Erro HTTP {response.status_code} ao consultar '{nome}': {e}")
    except requests.exceptions.Timeout:
        print(f"Tempo limite excedido ao consultar '{nome}' ({sexo_sigla}).")
    except Exception as e:
        print(f"Erro inesperado na requisição para '{nome}' ({sexo_sigla}): {e}")
        
    return 0


def classify_gender(nome_completo: str) -> str:
    """
    Função principal de classificação de gênero.
    Compara as frequências Masculina e Feminina do IBGE.
    """
    
    if nome_completo is None or str(nome_completo).strip() == '':
        return 'I' 
        
    try:
        # Limpeza e extração do primeiro nome
        primeiro_nome = str(nome_completo).strip().split(' ')[0]
        
        # Coleta as frequências (duas requisições)
        freq_f = _fetch_frequencia(primeiro_nome, 'f')
        freq_m = _fetch_frequencia(primeiro_nome, 'm')

        # Classificação
        if freq_f > freq_m and freq_f > 0:
            return 'F'
        elif freq_m > freq_f and freq_m > 0:
            return 'M'
        else:
            return 'I' # Indefinido/Ambíguo
            
    except Exception as e:
        # Erro inesperado no fluxo de classificação
        print(f"Erro inesperado durante a classificação de '{nome_completo}': {e}")
        return 'E'