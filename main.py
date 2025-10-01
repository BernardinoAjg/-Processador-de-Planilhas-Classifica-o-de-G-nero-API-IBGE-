import pandas as pd
import os
import glob
from typing import List

# Importa as constantes e a função de classificação dos outros módulos
from config import (
    PASTA_PLANILHAS_ORIGINAIS, 
    PASTA_PLANILHAS_SAIDA, 
    NOME_COLUNA_ENTRADA,
    PREFIXO_SAIDA,
    COLUNAS_PARA_FORMATAR_DATA
)
from classifier import classify_gender


# FUNÇÕES AUXILIARES DE FORMATAÇÃO DE DADOS

def _format_cell_date(cell_value, output_format: str):
    """Função auxiliar para aplicar a formatação a uma célula individual."""
    if pd.isna(cell_value):
        return cell_value
        
    try:
        # 1. Tenta converter o valor para string
        value_str = str(cell_value).strip()
        if not value_str:
            return cell_value
        
        # 2. Tenta a conversão robusta para datetime
        date_obj = pd.to_datetime(value_str, errors='coerce', infer_datetime_format=True)
        
        # 3. Formata para string de saída se a conversão foi bem-sucedida
        if pd.notna(date_obj):
            return date_obj.strftime(output_format)
        
        return cell_value 
        
    except Exception:
        # Captura qualquer erro de célula e permite que o loop continue
        return cell_value


def formatar_colunas_data(df: pd.DataFrame, colunas_de_data: List[str]) -> pd.DataFrame:
    """
    Formata colunas de data para 'dd/mm/aaaa' aplicando a lógica célula por célula 
    e forçando o formato final de string.
    """
    
    # FORMATO DESEJADO FINAL: DIA/MÊS/ANO
    FORMATO_SAIDA = '%d/%m/%Y' 

    for coluna in colunas_de_data:
        if coluna in df.columns:
            try:
                print(f"   🔧 Tentando formatar coluna '{coluna}'...")
                
                # Aplica a função de formatação célula por célula (robusto contra dados sujos).
                df[coluna] = df[coluna].apply(
                    lambda x: _format_cell_date(x, FORMATO_SAIDA)
                )
                
                print(f"   ✅ Data: Coluna '{coluna}' formatada com sucesso.")

            except Exception as e:
                # Se o erro for generalizado na coluna, ele será capturado aqui.
                print(f"   ⚠️ Aviso: Falha crítica ao formatar a coluna '{coluna}'. A coluna foi ignorada. Erro: {e}")
                
    return df

# =========================================================================
# === FUNÇÃO PRINCIPAL DE PROCESSAMENTO ===
# =========================================================================

def processar_planilhas_em_lote():
    """
    Busca e processa todos os arquivos na pasta configurada, aplicando a 
    classificação de gênero e salvando em uma pasta de saída separada.
    """
    
    # 0. CONFIGURAÇÃO E CRIAÇÃO DA PASTA DE SAÍDA
    try:
        if not os.path.exists(PASTA_PLANILHAS_SAIDA):
            os.makedirs(PASTA_PLANILHAS_SAIDA)
            print(f"✅ Pasta de saída criada: {PASTA_PLANILHAS_SAIDA}")
    except OSError as e:
        print(f"❌ ERRO: Não foi possível criar a pasta de saída '{PASTA_PLANILHAS_SAIDA}': {e}")
        return

    # 1. ENCONTRA OS ARQUIVOS NA PASTA ORIGINAL
    arquivos_excel = glob.glob(os.path.join(PASTA_PLANILHAS_ORIGINAIS, '*.xlsx')) + \
                     glob.glob(os.path.join(PASTA_PLANILHAS_ORIGINAIS, '*.xls'))
    arquivos_csv = glob.glob(os.path.join(PASTA_PLANILHAS_ORIGINAIS, '*.csv'))
    arquivos_para_processar = arquivos_excel + arquivos_csv
    
    if not arquivos_para_processar:
        print(f"⚠️ Atenção: Nenhum arquivo encontrado em: {PASTA_PLANILHAS_ORIGINAIS}")
        return

    print(f"Iniciando o processamento de {len(arquivos_para_processar)} arquivo(s)...")

    # 2. LOOP DE PROCESSAMENTO
    for caminho_completo in arquivos_para_processar:
        nome_arquivo = os.path.basename(caminho_completo)
        print(f"\n- Processando: {nome_arquivo}")

        try: 
            # LEITURA (header=1 para pular a linha em branco)
            if nome_arquivo.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(caminho_completo, header=1) 
            elif nome_arquivo.endswith('.csv'):
                # Assumindo separador ';' e encoding 'utf-8'. Ajuste se necessário.
                df = pd.read_csv(caminho_completo, sep=';', encoding='utf-8', header=1) 
            else:
                continue

            # VALIDAÇÃO
            if NOME_COLUNA_ENTRADA not in df.columns:
                print(f"   ❌ ERRO: Coluna '{NOME_COLUNA_ENTRADA}' não encontrada. Ignorando arquivo.")
                continue
            
            # PASSO 1: FORMATAR AS DATAS (aplica dd/mm/aaaa)
            df = formatar_colunas_data(df, COLUNAS_PARA_FORMATAR_DATA)
                
            # PASSO 2: APLICAÇÃO DO CLASSIFICADOR DE GÊNERO
            df['Gênero Classificado'] = df[NOME_COLUNA_ENTRADA].apply(classify_gender)

            # 3. ESCRITA NA PASTA DE SAÍDA (Lógica para forçar formato TEXTO no Excel)
            nome_base, extensao = os.path.splitext(nome_arquivo)
            novo_nome_arquivo = f'{PREFIXO_SAIDA}{nome_base}{extensao}'
            novo_caminho = os.path.join(PASTA_PLANILHAS_SAIDA, novo_nome_arquivo)

            if extensao in ('.xlsx', '.xls'):
                # === LÓGICA DE ESCRITA CORRIGIDA PARA EXCEL COM FORMATO TEXTO ===
                writer = pd.ExcelWriter(novo_caminho, engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                
                workbook  = writer.book
                worksheet = writer.sheets['Sheet1']
                
                # Define o formato de texto: '@' é o formato de texto simples do Excel
                text_format = workbook.add_format({'num_format': '@'})

                # Aplica o formato de texto às colunas de data
                for coluna in COLUNAS_PARA_FORMATAR_DATA:
                    if coluna in df.columns:
                        try:
                            col_index = df.columns.get_loc(coluna)
                            # Aplica o formato de texto à coluna inteira
                            worksheet.set_column(col_index, col_index, None, text_format) 
                        except KeyError:
                             pass 
                        
                writer.close()
                
            elif extensao == '.csv':
                df.to_csv(novo_caminho, index=False, sep=';', encoding='utf-8')
                
            print(f"   ✅ Sucesso! Salvo como: {novo_nome_arquivo}")

        except Exception as e:
            print(f"   ❌ ERRO fatal ao processar {nome_arquivo}: {e}")
            
    print("\n--- Processamento em lote concluído! ---")

# =========================================================================
# === EXECUÇÃO DO SCRIPT ===
# =========================================================================

if __name__ == '__main__':
    processar_planilhas_em_lote()