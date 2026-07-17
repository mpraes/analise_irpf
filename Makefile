# Makefile para o projeto de Análise do IRPF

.PHONY: setup perfil dicionarios clean

setup:
	@echo "Instalando dependências necessárias com uv..."
	uv add pandas pypdf

perfil:
	@echo "Gerando relatórios de perfil na pasta 'relatorios'..."
	uv run python src/gerar_perfis.py

dicionarios:
	@echo "Gerando dicionários HTML extraídos dos PDFs..."
	uv run python src/gerar_dicionarios.py

clean:
	@echo "Limpando relatórios gerados..."
	rm -rf relatorios/*_perfil.html
	rm -rf relatorios/index.html
	rm -rf relatorios/dicionarios
