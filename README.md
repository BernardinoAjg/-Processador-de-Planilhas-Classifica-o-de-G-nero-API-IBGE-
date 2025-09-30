# 🇧🇷 Processador de Planilhas: Classificação de Gênero (API IBGE)

<p align="center">
<img src="https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
<img src="https://img.shields.io/badge/Status-Estável-brightgreen.svg?style=for-the-badge" alt="Status Badge">
<img src="https://img.shields.io/badge/Tecnologia-Pandas_|_IBGE-red?style=for-the-badge" alt="Tecnologia Badge">
</p>

## Este projeto implementa um sistema robusto e modularizado em Python para processamento em lote de planilhas. Seu objetivo é enriquecer dados cadastrais, classificando o gênero dos indivíduos por meio da consulta à API de Nomes do Censo do IBGE. 
O sistema foi desenhado para garantir a integridade dos dados, contornando problemas como erros de certificado SSL e a formatação incorreta de datas no Excel (problema 00:00:00).


## Instrução de Instalação

### Pre requisistos

```Python (Versão 3.x):``` O sistema foi desenvolvido em Python. Recomenda-se usar uma versão 3.7 ou superior para garantir a compatibilidade com todas as bibliotecas e suas funcionalidades mais recentes.

## Setup

### Passo 1: Organização Inicial (Setup de Pastas)

Embora o código lide com a criação da pasta de saída, organize seu diretório inicial.

1. Crie um diretório para o seu projeto e navegue até ele:
```
Bash

mkdir Projeto_Classificador_IBGE
cd Projeto_Classificador_IBGE
```
2. Dentro dele, crie a pasta que receberá seus arquivos de entrada:
```
Bash

mkdir planilhas_originais
```
  (A pasta de saída será criada automaticamente pelo script.)

### Passo 2: Criação e Ativação do Ambiente Virtual

É uma boa prática isolar as bibliotecas do projeto para evitar conflitos com outros projetos Python na sua máquina.

1. Crie o Ambiente Virtual:
```
Bash

python -m venv venv

```   
2. Ative o Ambiente Virtual:

Windows (CMD/PowerShell)	  ```.\venv\Scripts\activate```

macOS / Linux            	  ```source venv/bin/activate```


Seu terminal deve mostrar ```(venv)``` no início da linha de comando, indicando que o ambiente está ativo.

### Passo 3: Instalação das Dependências

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias.


```
Bash

(venv) $ pip install pandas requests openpyxl xlsxwriter
```

```pandas```	A ferramenta principal para leitura, manipulação e transformação de todos os dados da planilha (Excel e CSV).

```requests```	Essencial para fazer as consultas HTTP à API do IBGE (classifier.py).

```openpyxl```	Necessário para o Pandas poder ler os arquivos .xlsx.

```xlsxwriter```	CRUCIAL: Usado para escrever o arquivo Excel de saída. É o que permite forçar o formato de Texto nas colunas de data (impedindo o 00:00:00).

Passo 4: Configuração Final (```config.py```)

