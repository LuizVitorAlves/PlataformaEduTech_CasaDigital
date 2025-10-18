DB_NAME = edutech_db
DB_USER = postgres

PYTHON_VENV = ./venv/bin/python
GENERATOR = python/gerador_dados.py

DATA_FILES = data/*.csv
CACHE_DIRS = python/__pycache__

.PHONY: all data clean setup sql db-create consultas

all: data
	@echo "✨ Execução principal concluída. Use 'make clean' para limpar os arquivos CSV."

data:
	@echo "--- 🚀 INICIANDO GERAÇÃO DE DADOS EDUTECH ---"
	$(PYTHON_VENV) $(GENERATOR)
	@echo "--- ✅ CSVs gerados na pasta data/ ---"

# EXECUTAR CONSULTAS
consultas:
	@echo "--- 📊 EXECUTANDO CONSULTAS (sql/consultas.sql) ---"
	psql -U $(DB_USER) -d $(DB_NAME) -f sql/consultas.sql
	@echo "--- ✅ FIM DO RELATÓRIO SQL ---"

# AUTOMAÇÃO SQL COMPLETA
sql: data db-create
	@echo "--- 🔄 CARREGANDO SCHEMA E DADOS NO POSTGRES ---"
	psql -U $(DB_USER) -d $(DB_NAME) -f sql/schema.sql
	psql -U $(DB_USER) -d $(DB_NAME) -f sql/dados.sql
	@echo "--- ✅ Banco de Dados $(DB_NAME) populado com sucesso! ---"

db-create:
	@echo "--- ♻️ RECRIAÇÃO DO BANCO DE DADOS $(DB_NAME) ---"
	-psql -U $(DB_USER) -c "DROP DATABASE IF EXISTS $(DB_NAME) WITH (FORCE)" postgres
	psql -U $(DB_USER) -c "CREATE DATABASE $(DB_NAME)" postgres
	@echo "--- ✅ Banco $(DB_NAME) criado. ---"


# LIMPEZA E SETUP
clean:
	@echo "--- 🗑️ INICIANDO LIMPEZA DO PROJETO ---"
	rm -f $(DATA_FILES)
	find . -name "__pycache__" -type d -exec rm -rf {} +
	
	@echo "--- ✅ Limpeza Concluída! ---"

setup:
	@echo "--- ⚙️ CONFIGURANDO AMBIENTE ---"
	@if [ ! -d "venv" ]; then \
		echo "  -> Criando ambiente virtual..."; \
		python3 -m venv venv; \
	fi
	./venv/bin/pip install faker pandas
	@echo "--- ✅ Setup Concluído. Use 'source venv/bin/activate' ---"