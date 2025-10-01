#  <CENTER> ✨ 🇧🇷 Processador de Planilhas: Classificação de Gênero (API IBGE) 

<p align="center">
<img src="https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
<img src="https://img.shields.io/badge/Status-Estável-brightgreen.svg?style=for-the-badge" alt="Status Badge">
<img src="https://img.shields.io/badge/Tecnologia-Pandas_|_IBGE-red?style=for-the-badge" alt="Tecnologia Badge">
</p>

<br>

## Este projeto implementa um sistema robusto e modularizado em Python para processamento em lote de planilhas. Seu objetivo é enriquecer dados cadastrais, classificando o gênero dos indivíduos por meio da consulta à API de Nomes do Censo do IBGE. <br> <br> O sistema foi desenhado para garantir a integridade dos dados, contornando problemas como erros de certificado SSL e a formatação incorreta de datas no Excel (problema 00:00:00).

<br><br><br><br>

# 🚀 Funcionalidades Principais

•	🔄 **Processamento em Lote:** Lê e processa todos os arquivos .xlsx, .xls e .csv em massa. <br>
•	🧠 **Classificação IBGE:** Classifica o gênero (M/F/I) baseando-se na Frequência Agregada de uso histórico. <br>
•	🛡️ **Estabilidade SSL:** Contorna erros de certificado comuns em ambientes com proxy, garantindo a conexão com a API. <br>
•	📅 **Formatação Garantida:** Converte datas para dd/mm/aaaa e força o Excel a salvar como texto, prevenindo o 00:00:00. <br>
•	📦 **Modularidade:** Arquitetura limpa (config, classifier, main) para fácil manutenção e escalabilidade. <br>

<br><br>

# 🏗️ Instrução de Instalação

<br>

## 🛠️ **Pre requisistos**

```Python (Versão 3.x)``` O sistema foi desenvolvido em Python. Recomenda-se usar uma versão 3.7 ou superior para garantir a compatibilidade com todas as bibliotecas e suas funcionalidades mais recentes.

<br>

# ⚙️ Setup

### **Passo 1: Organização Inicial (Setup de Pastas)**

Embora o código lide com a criação da pasta de saída, organize seu diretório inicial.

1. Crie um diretório para o seu projeto e navegue até ele:
```
Bash

mkdir Projeto_Classificador_IBGE
cd Projeto_Classificador_IBGE
```

<br>

2. Dentro dele, crie a pasta que receberá seus arquivos de entrada:
```
Bash

mkdir planilhas_originais
```
 💬 (A pasta de saída será criada automaticamente pelo script.)

<br>

### **Passo 2: Criação e Ativação do Ambiente Virtual**

É uma boa prática isolar as bibliotecas do projeto para evitar conflitos com outros projetos Python na sua máquina.

1. Crie o Ambiente Virtual:
```
Bash

python -m venv venv
```
<br>

2. Ative o Ambiente Virtual:

| Sistema operaciona | <CENTER> Bash | 
| --- | --- |
| Windows (CMD/PowerShell) | ```.\venv\Scripts\activate``` |
| macOS ou Linux | ```source venv/bin/activate``` | 

<br>

 💬 Seu terminal deve mostrar ```(venv)``` no início da linha de comando, indicando que o ambiente está ativo.

<br>

### **Passo 3: Instalação das Dependências**

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias.

```
Bash

(venv) $ pip install pandas requests openpyxl xlsxwriter
```

```pandas```	A ferramenta principal para leitura, manipulação e transformação de todos os dados da planilha (Excel e CSV).

```requests```	Essencial para fazer as consultas HTTP à API do IBGE (classifier.py).

```openpyxl```	Necessário para o Pandas poder ler os arquivos .xlsx.

```xlsxwriter```	CRUCIAL: Usado para escrever o arquivo Excel de saída. É o que permite forçar o formato de Texto nas colunas de data (impedindo o 00:00:00).

<br>

### **Passo 4: Configuração Final (```config.py```)**

Antes de executar, você deve ajustar o arquivo ```config.py``` para mapear os caminhos e nomes de colunas corretos, de acordo com seus dados.

* Mova os arquivos do seu projeto (```main.py, classifier.py, config.py```) para o diretório raiz (```Projeto_Classificador_IBGE```).

* Edite ```config.py``` e aponte ```PASTA_PLANILHAS_ORIGINAIS``` para o seu novo diretório ```planilhas_originais/```.

<br>

💬 O arquivo config.py serve como o centro de controle do seu projeto. Você só precisa editar o valor das strings (o texto entre aspas) para que o sistema saiba onde procurar os dados e quais colunas analisar.

<br>

### ❓ **Quais variáveis devo editar no ```config.py```?**
Aqui estão as três variáveis que você deve ajustar:


**1. Caminhos de Diretórios**<br>
Você precisa informar ao script a localização dos seus dados brutos.

```
Python

 Mude este caminho para o local EXATO onde você colocou a pasta "planilhas_originais"
PASTA_PLANILHAS_ORIGINAIS = r'C:\Users\SeuNome\Projeto_Classificador_IBGE\planilhas_originais' 


 Esta pasta será criada automaticamente DENTRO do diretório acima, mas você pode mudar o nome
PASTA_SAIDA_NOME = 'planilhas_transformadas' 
```

* Dica: Usar o prefixo r' (raw string) antes do caminho no Windows (r'C:\...') é uma boa prática para evitar problemas com barras invertidas.

<br>

**2. Coluna de Entrada (Nome Completo)**
O script precisa saber qual coluna contém o nome completo que ele deve enviar para a API do IBGE. O nome deve ser EXATO (sensível a espaços e maiúsculas).

```
Python

 Altere para o nome exato da coluna que contém os nomes que você quer classificar.
 Exemplo: 'NM_BENEF:' (conforme o seu caso)
NOME_COLUNA_ENTRADA = 'NM_BENEF:'
```

<br>

**3. Colunas de Data para Formatação**

Liste todos os nomes de colunas que contêm datas e precisam ser convertidas para o formato ```dd/mm/aaaa``` e salvas como Texto no Excel.

```
Python

 Liste todas as colunas que precisam ser forçadas ao formato dd/mm/aaaa (Texto)
COLUNAS_PARA_FORMATAR_DATA: List[str] = [
    'DT_NASC:', 
    'DT_INCL:', 
    # Adicione qualquer outra coluna de data aqui, ex: 'DT_CADASTRO'
]
```
Após salvar o config.py com esses valores ajustados, o sistema estará totalmente mapeado para o seu ambiente e pronto para ser executado com python -m main.

<br>

### **Passo 5: ▶️ Execução**
Com o ambiente ativo e a configuração feita, você executa o sistema como um módulo:
 <br>
```
Bash

(venv) $ python -m main
```
<br>
