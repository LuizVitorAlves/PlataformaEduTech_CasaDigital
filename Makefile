PYTHON_VENV = ./venv/bin/python
GENERATOR = python/gerador_dados.py

DATA_FILES = data/*.csv
CACHE_DIRS = python/__pycache__

.PHONY: all data clean setup
all: data
	@echo "✨ Execução principal concluída. Use 'make clean' para limpar."
data:
	@echo "--- 🚀 INICIANDO GERAÇÃO DE DADOS EDUTECH ---"
	$(PYTHON_VENV) $(GENERATOR)
	@echo "--- ✅ CSVs gerados na pasta data/ ---"

clean:
	@echo "--- 🗑️ INICIANDO LIMPEZA DO PROJETO ---"
	rm -f $(DATA_FILES)
	find . -name "__pycache__" -type d -exec rm -rf {} +

setup:
	@echo "--- ⚙️ CONFIGURANDO AMBIENTE ---"
	@if [ ! -d "venv" ]; then \
		echo "  -> Criando ambiente virtual..."; \
		python3 -m venv venv; \
	fi
	./venv/bin/pip install faker pandas
	@echo "--- ✅ Setup Concluído. Use 'source venv/bin/activate' ---"