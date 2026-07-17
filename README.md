# 📊 Projeto de Análise de Dados do IRPF

Este projeto tem como objetivo realizar análises profundas, rigorosas e acessíveis sobre os Grandes Números do IRPF (Imposto de Renda da Pessoa Física). O foco é explorar a progressividade, o perfil dos declarantes, e apoiar o debate público e legislativo com dados concretos.

Para um entendimento profundo da metodologia, KPIs, e contexto jornalístico/legislativo, veja o documento [CONTEXTO.md](CONTEXTO.md). E para verificar o panorama recente de discussões sobre o IR, confira [NOTICIAS.md](docs/NOTICIAS.md).

## 📂 Estrutura de Diretórios

O repositório está organizado da seguinte forma:

```text
├── CONTEXTO.md         # Diretrizes, metodologias e objetivos do projeto
├── README.md           # Este arquivo
├── Makefile            # Comandos automatizados para setup e relatórios
├── data/
│   ├── csv_arquivos/   # Base de dados tabular (CSVs) oficiais do IRPF
│   └── dicionario_dados/ # PDFs descrevendo os metadados e esquemas
├── docs/
│   └── NOTICIAS.md     # Levantamento de narrativas e dúvidas do noticiário
├── relatorios/         # (Gerado automaticamente)
│   ├── dados/          # Relatórios de perfil interativos (HTML) de cada CSV
│   └── dicionarios/    # Extratos HTML dos PDFs de metadados
└── src/
    ├── gerar_perfis.py       # Script gerador dos relatórios tabulares
    └── gerar_dicionarios.py  # Script extrator dos PDFs de dicionário
```

## 🚀 Instalação e Configuração

Nós gerenciamos os pacotes utilizando a ferramenta **[uv](https://github.com/astral-sh/uv)** por ser mais rápida e lidar muito bem com ambientes virtuais nativos (evitando conflitos de PEP 668 no sistema operacional).

Para instalar as dependências necessárias (`pandas` e `pypdf`):

```bash
make setup
```

## ⚙️ Como Utilizar

Após o setup, a geração dos relatórios exploratórios é totalmente automatizada. Os scripts vão processar tanto os arquivos `.csv` quanto os dicionários em `.pdf` e criar pequenos websites navegáveis.

### 1. Gerar Relatórios de Perfil dos Dados
Para gerar uma análise descritiva rica, tipos de colunas, estatísticas e amostras de cada CSV:
```bash
make perfil
```
> Os relatórios gerados estarão em `relatorios/dados/index.html`.

### 2. Gerar Relatórios de Dicionários (Metadados)
Para converter a documentação em PDF em páginas HTML de fácil acesso e leitura:
```bash
make dicionarios
```
> Os relatórios gerados estarão em `relatorios/dicionarios/index.html`.

### 3. Limpeza
Para deletar os arquivos HTML gerados e limpar as pastas:
```bash
make clean
```

## 🗺️ Navegação

Os arquivos index (`relatorios/dados/index.html` e `relatorios/dicionarios/index.html`) conversam entre si, atuando como um menu centralizado interativo. Através deles ou dos próprios arquivos individuais gerados, é possível alternar rapidamente entre explorar o dicionário (entendimento de negócio) e o perfil da base de dados propriamente dita.
