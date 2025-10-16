#!/home/alves/edutech/venv/bin/python

import csv
import random
import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker

fake = Faker('pt_BR')
DATA_MIN_GLOBAL = datetime.now() - timedelta(days=3 * 365)
DATA_MAX_GLOBAL = datetime.now()

def gerar_data_historica():
    return fake.date_time_between(start_date=DATA_MIN_GLOBAL, end_date=DATA_MAX_GLOBAL).isoformat()

def gerar_alunos(quantidade):
    alunos = []
    for i in range(1, quantidade + 1):
        nome_completo = fake.first_name() + " " + fake.last_name()
        alunos.append({
            'id': i,
            'nome': nome_completo,
            'email': fake.unique.email(),
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d'),
            'data_cadastro': gerar_data_historica()
        })
    return alunos

def gerar_instrutores(quantidade):
    instrutores = []
    especialidades = ['Backend', 'Frontend', 'Dados', 'DevOps', 'UX/UI']
    for i in range(1, quantidade + 1):
        instrutores.append({
            'id': i,
            'nome': f"{fake.first_name()} {fake.last_name()}",
            'email': f'instrutor_{i}_{fake.unique.random_int(1, 9999)}@edutech.com',
            'especialidade': random.choice(especialidades),
            'biografia': fake.text(max_nb_chars=200)
        })
    return instrutores

def gerar_cupons(quantidade):
    cupons = []
    for i in range(1, quantidade + 1):
        tipo = random.choice(['percentual', 'fixo'])
        valor = round(random.uniform(5.00, 50.00), 2) if tipo == 'fixo' else random.randint(5, 50)
        
        cupons.append({
            'id': i,
            'codigo': fake.unique.bothify(text='CPN####'),
            'tipo': tipo,
            'valor_desconto': valor,
            'data_expiracao': fake.date_time_between(start_date='now', end_date='+1y').strftime('%Y-%m-%d'),
            'uso_maximo': random.randint(10, 500),
            'usos_atuais': 0
        })
    return cupons