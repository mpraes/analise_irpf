import os
import glob
import pandas as pd
import io

def gerar_perfis(input_dir, output_dir, dict_dir):
    """
    Lê todos os arquivos CSV em input_dir e gera um relatório de perfil em HTML 
    no diretório output_dir. Ao final, gera um index.html com links para todos.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista todos os arquivos CSV no diretório de entrada
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    if not csv_files:
        print(f"Nenhum arquivo CSV encontrado em {input_dir}")
        return

    print(f"Encontrados {len(csv_files)} arquivos CSV para processar.")
    
    relatorios_gerados = []
    
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        name, _ = os.path.splitext(filename)
        output_file = os.path.join(output_dir, f"{name}_perfil.html")
        
        # O nome do arquivo no sistema operacional às vezes pode precisar ser tratado,
        # mas aqui nós apenas precisamos garantir que o nome seja guardado corretamente
        relatorios_gerados.append({
            "nome": name,
            "arquivo": f"{name}_perfil.html"
        })
        
        if os.path.exists(output_file):
            print(f"O relatório para {name} já existe. Pulando a geração do CSV...")
            continue
            
        print(f"Gerando perfil para: {filename}...")
        try:
            # Tenta ler como UTF-8 primeiro para evitar os problemas de "FormulÃ¡rio"
            try:
                df = pd.read_csv(csv_file, sep=';', encoding='utf-8', low_memory=False)
            except UnicodeDecodeError:
                # Fallback para latin1 caso o arquivo não seja utf-8 válido
                df = pd.read_csv(csv_file, sep=';', encoding='latin1', low_memory=False)
            
            # Se for carregado apenas em uma coluna, tentar com separador padrão de vírgula
            if len(df.columns) == 1:
                try:
                    df = pd.read_csv(csv_file, encoding='utf-8', low_memory=False)
                except UnicodeDecodeError:
                    df = pd.read_csv(csv_file, encoding='latin1', low_memory=False)
                
            # Coletar informações do DataFrame (df.info())
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            
            # Gerar estatísticas descritivas
            describe_html = df.describe(include='all').to_html(classes="table table-striped table-bordered")
            
            # Cabeçalho da tabela
            head_html = df.head(10).to_html(classes="table table-striped table-bordered")
            
            # Montando um HTML simples e bonito com Bootstrap
            html_content = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Perfil de Dados - {name}</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{ padding: 20px; }}
                    h1, h2, h3 {{ margin-top: 30px; }}
                    pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                    .header-actions {{ margin-bottom: 20px; display: flex; gap: 10px; }}
                </style>
            </head>
            <body>
                <div class="container-fluid">
                    <div class="header-actions">
                        <a href="index.html" class="btn btn-outline-secondary">&larr; Voltar para o Menu de Dados</a>
                        <a href="../dicionarios/index.html" class="btn btn-outline-success">Ver Dicionários de Metadados</a>
                    </div>
                    <h1 class="text-primary">Perfil Exploratório - {name}</h1>
                    <hr>
                    
                    <h2>1. Visão Geral</h2>
                    <ul>
                        <li><strong>Total de Linhas:</strong> {df.shape[0]}</li>
                        <li><strong>Total de Colunas:</strong> {df.shape[1]}</li>
                    </ul>
                    
                    <h2>2. Estrutura dos Dados (Info)</h2>
                    <pre>{info_str}</pre>
                    
                    <h2>3. Estatísticas Descritivas</h2>
                    <div class="table-responsive">
                        {describe_html}
                    </div>
                    
                    <h2>4. Amostra de Dados (Primeiras 10 linhas)</h2>
                    <div class="table-responsive">
                        {head_html}
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Escreve o arquivo explicitamente como utf-8
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            print(f"Sucesso: Relatório salvo em {output_file}\n")
            
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}\n")

    # Geração do arquivo centralizado index.html
    if relatorios_gerados:
        index_file = os.path.join(output_dir, "index.html")
        
        # Ordena a lista de relatórios alfabeticamente para ficar mais bonito
        relatorios_gerados = sorted(relatorios_gerados, key=lambda x: x["nome"])
        
        links_html = ""
        for r in relatorios_gerados:
            links_html += f'<li class="list-group-item"><a href="{r["arquivo"]}" class="text-decoration-none">{r["nome"]}</a></li>\n'
            
        index_html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Índice de Relatórios - Análise IRPF</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ padding: 30px; background-color: #f4f6f9; }}
                .card {{ max-width: 800px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                h1 {{ margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                        <h1 class="h3 mb-0">Índice de Relatórios de Perfil - IRPF</h1>
                        <a href="../dicionarios/index.html" class="btn btn-sm btn-light text-primary">Ir para Dicionários de Dados</a>
                    </div>
                    <div class="card-body">
                        <p class="text-muted">Selecione um dos relatórios exploratórios abaixo para visualizar as métricas, esquemas e dados de exemplo:</p>
                        <ul class="list-group list-group-flush">
                            {links_html}
                        </ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
            
        print(f"\n=======================================================")
        print(f"Sucesso! Menu centralizado gerado em: {index_file}")
        print(f"=======================================================")

if __name__ == "__main__":
    # Caminhos relativos a partir do root do projeto
    INPUT_CSV_DIR = os.path.join("data", "csv_arquivos")
    DICT_DIR = os.path.join("data", "dicionario_dados")
    OUTPUT_REPORT_DIR = os.path.join("relatorios", "dados")
    
    print("Iniciando geração de relatórios de perfil usando Pandas...")
    gerar_perfis(INPUT_CSV_DIR, OUTPUT_REPORT_DIR, DICT_DIR)
