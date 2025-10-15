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