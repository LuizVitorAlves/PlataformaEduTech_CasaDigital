#!/home/alves/edutech/venv/bin/python

import csv
import os
import sys

def obter_quantidade(nome_entidade, padrao):
    while True:
        try:
            if sys.stdin.isatty():
                entrada = input(f"Quantos {nome_entidade} deseja gerar (Padrão: {padrao})? ")
            else:
                entrada = ""
            if not entrada:
                return padrao
            quantidade = int(entrada)
            if quantidade < 0:
                print("A quantidade deve ser não-negativa. Usando o padrão.")
                return padrao
            return quantidade
        except ValueError:
            print("Entrada inválida. Usando o padrão.")
            return padrao

def exportar_para_csv(data, nome_arquivo):
    if not data:
        print(f"Alerta: Não há dados para exportar em {nome_arquivo}.")
        return
    os.makedirs('data', exist_ok=True)
    fieldnames = list(data[0].keys())
    caminho_arquivo = f'./data/{nome_arquivo}.csv'
    try:
        with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"  -> Exportado: {len(data)} registros para {caminho_arquivo}")
    except Exception as e:
        print(f"ERRO ao exportar {nome_arquivo}: {e}")
