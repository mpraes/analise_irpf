import os
import glob

# Tentaremos importar o pypdf, se falhar, o script pedirá para instalar.
try:
    from pypdf import PdfReader
except ImportError:
    print("Erro: A biblioteca 'pypdf' não está instalada.")
    print("Por favor, rode 'uv add pypdf' ou 'make setup' se o Makefile foi atualizado.")
    exit(1)

def gerar_dicionarios(input_dir, output_dir):
    """
    Lê os PDFs da pasta de dicionário de dados e gera páginas HTML formatadas 
    com o texto extraído, além de um índice centralizado.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"Nenhum arquivo PDF encontrado em {input_dir}")
        return

    print(f"Encontrados {len(pdf_files)} arquivos PDF para processar.")
    dicionarios_gerados = []
    
    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        name, _ = os.path.splitext(filename)
        output_file = os.path.join(output_dir, f"{name}_dicionario.html")
        
        print(f"Extraindo dados de: {filename}...")
        
        try:
            reader = PdfReader(pdf_file)
            text_content = ""
            for i, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    text_content += f"--- PÁGINA {i+1} ---\n\n" + extracted + "\n\n"
                    
            # Sanitização simples para HTML
            text_content = text_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Metadados - {name}</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{ padding: 20px; }}
                    h1, h2 {{ margin-top: 20px; }}
                    /* Usa font monospace e pre-wrap para manter a formatação do PDF o máximo possível */
                    pre {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; white-space: pre-wrap; font-family: monospace; font-size: 14px; line-height: 1.5; }}
                    .header-actions {{ margin-bottom: 20px; display: flex; gap: 10px; }}
                </style>
            </head>
            <body>
                <div class="container-fluid">
                    <div class="header-actions">
                        <a href="index.html" class="btn btn-outline-secondary">&larr; Voltar para o Menu de Dicionários</a>
                        <a href="../dados/index.html" class="btn btn-outline-primary">Ver Relatórios de Dados</a>
                    </div>
                    <h1 class="text-success">Dicionário de Dados: {name}</h1>
                    <hr>
                    
                    <div class="card shadow-sm">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">Conteúdo Extraído do PDF</h5>
                        </div>
                        <div class="card-body">
                            <pre>{text_content}</pre>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            dicionarios_gerados.append({
                "nome": name,
                "arquivo": f"{name}_dicionario.html"
            })
            
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}\n")

    # Geração do arquivo centralizado index.html para os dicionários
    if dicionarios_gerados:
        index_file = os.path.join(output_dir, "index.html")
        dicionarios_gerados = sorted(dicionarios_gerados, key=lambda x: x["nome"])
        
        links_html = ""
        for r in dicionarios_gerados:
            links_html += f'<li class="list-group-item"><a href="{r["arquivo"]}" class="text-decoration-none text-success fw-bold">{r["nome"]}</a></li>\n'
            
        index_html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Índice de Dicionários - Análise IRPF</title>
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
                    <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                        <h1 class="h3 mb-0">Índice de Dicionários (Metadados) - IRPF</h1>
                        <a href="../dados/index.html" class="btn btn-sm btn-light text-success">Ir para Relatórios de Dados</a>
                    </div>
                    <div class="card-body">
                        <p class="text-muted">Selecione um dos dicionários de metadados abaixo para visualizar as explicações e schemas das variáveis:</p>
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
        print(f"Sucesso! Menu de Dicionários gerado em: {index_file}")
        print(f"=======================================================")

if __name__ == "__main__":
    # Caminhos relativos a partir do root do projeto
    INPUT_DICT_DIR = os.path.join("data", "dicionario_dados")
    # Para não misturar com os relatórios CSV, vamos jogar em uma subpasta
    OUTPUT_DICT_DIR = os.path.join("relatorios", "dicionarios")
    
    print("Iniciando extração dos PDFs...")
    gerar_dicionarios(INPUT_DICT_DIR, OUTPUT_DICT_DIR)
