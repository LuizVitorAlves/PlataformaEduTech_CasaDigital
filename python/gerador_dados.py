#!/home/alves/edutech/venv/bin/python

import csv
import random
import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
from utils import obter_quantidade, exportar_para_csv

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

def gerar_cursos(quantidade, instrutores_ids, categorias_ids):
    cursos = []
    niveis = ['iniciante', 'intermediario', 'avancado']
    
    for i in range(1, quantidade + 1):
        preco = Decimal(fake.pydecimal(left_digits=3, right_digits=2, min_value=49.90, max_value=499.90)).quantize(Decimal('0.01'))
        
        cursos.append({
            'id': i,
            'titulo': f'{random.choice(["Masterclass", "Curso Completo", "Guia Essencial"])} de {fake.catch_phrase()}',
            'descricao': fake.paragraph(nb_sentences=5),
            'categoria_id': random.choice(categorias_ids),
            'instrutor_id': random.choice(instrutores_ids),
            'preco': str(preco),
            'carga_horaria': random.choice([10, 20, 40, 60, 80, 100]),
            'nivel': random.choice(niveis),
            'data_criacao': gerar_data_historica()
        })
    return cursos

def gerar_modulos_e_aulas(dados_cursos):
    modulos = []
    aulas = []
    modulo_id_counter = 1
    aula_id_counter = 1
    tipos_aula = ['video', 'texto', 'quiz']
    for curso in dados_cursos:
        num_modulos = random.randint(2, 5)
        for ordem_modulo in range(1, num_modulos + 1):
            modulos.append({
                'id': modulo_id_counter,
                'curso_id': curso['id'],
                'titulo': f'Módulo {ordem_modulo}: {fake.catch_phrase()}',
                'ordem': ordem_modulo,
                'descricao': fake.text(max_nb_chars=150)
            })
            num_aulas = random.randint(4, 10) 
            for ordem_aula in range(1, num_aulas + 1):
                aulas.append({
                    'id': aula_id_counter,
                    'modulo_id': modulo_id_counter,
                    'titulo': f'Aula {ordem_aula}: {fake.bs()}',
                    'ordem': ordem_aula,
                    'duracao_minutos': random.randint(5, 60) if random.random() < 0.8 else 0,
                    'tipo': random.choice(tipos_aula)
                })
                aula_id_counter += 1
                
            modulo_id_counter += 1
    
    return modulos, aulas

def gerar_pedidos_e_pagamentos(dados_alunos, dados_cursos, dados_cupons, num_pedidos):
    pedidos = []
    pagamentos = []
    
    pedido_id_counter = 1
    pagamento_id_counter = 1
    
    alunos_ids = [a['id'] for a in dados_alunos]
    cupons_ids = [c['id'] for c in dados_cupons]
    
    status_transacao = ['aprovado', 'falhou', 'pendente']
    pesos_transacao = [70, 20, 10]
    metodos_pagamento = ['debito', 'credito', 'pix']

    for i in range(1, num_pedidos + 1):
        aluno_fk = random.choice(alunos_ids)
        data_pedido = fake.date_time_between(start_date=DATA_MIN_GLOBAL, end_date=DATA_MAX_GLOBAL)
        valor_bruto = Decimal('0.00')
        cursos_do_pedido = []
        candidatos = random.sample(dados_cursos, min(random.randint(1, 3), len(dados_cursos)))
        for curso_candidato in candidatos:
            preco_curso = Decimal(str(curso_candidato['preco'])) 
            if valor_bruto + preco_curso <= Decimal('999.99'):
                cursos_do_pedido.append(curso_candidato)
                valor_bruto += preco_curso
        if not cursos_do_pedido: 
            continue
        cupom_fk = None
        valor_desconto = Decimal('0.00')
        if random.random() < 0.20 and cupons_ids:
            cupom_fk = random.choice(cupons_ids)
            valor_desconto = (valor_bruto * Decimal('0.20')).quantize(Decimal('0.01'))
        valor_final = valor_bruto - valor_desconto
        pedido = {
            'id': pedido_id_counter,
            'aluno_id': aluno_fk,
            'data_pedido': data_pedido.isoformat(),
            'cupom_id': cupom_fk,
            'valor_bruto': str(valor_bruto),
            'valor_desconto_aplicado': str(valor_desconto),
            'valor_final': str(valor_final),
            'status_pedido': 'pendente_pagamento',
            'cursos_comprados': [{'id': c['id'], 'preco': c['preco']} for c in cursos_do_pedido]
        }
        pedidos.append(pedido)
        status_pg = random.choices(status_transacao, weights=pesos_transacao, k=1)[0]
        pagamento = {
            'id': pagamento_id_counter,
            'pedido_id': pedido_id_counter,
            'metodo_pagamento': random.choice(metodos_pagamento),
            'id_transacao_gateway': str(fake.uuid4()),
            'valor_pago': str(valor_final),
            'data_pagamento': (data_pedido + timedelta(minutes=random.randint(5, 60))).isoformat(),
            'status_transacao': status_pg
        }
        pagamentos.append(pagamento)
        if status_pg == 'aprovado':
            pedido['status_pedido'] = 'pago' 
        pedido_id_counter += 1
        pagamento_id_counter += 1
    return pedidos, pagamentos

def gerar_matriculas(dados_pedidos):
    matriculas = []
    matricula_id_counter = 1
    
    pedidos_pagos = [p for p in dados_pedidos if p['status_pedido'] == 'pago']

    for pedido in pedidos_pagos:
        data_pedido_dt = datetime.fromisoformat(pedido['data_pedido'])
        data_matricula = (data_pedido_dt + timedelta(minutes=random.randint(65, 120))).isoformat()
        for curso in pedido['cursos_comprados']: 
            matriculas.append({
                'id': matricula_id_counter,
                'aluno_id': pedido['aluno_id'],
                'curso_id': curso['id'],
                'pedido_id': pedido['id'],
                'data_matricula': data_matricula,
                'data_conclusao': None, 
                'status': 'ativa'
            })
            matricula_id_counter += 1
    return matriculas

def gerar_categorias():
    nomes = ['Programação', 'Design', 'Dados', 'DevOps', 'Negócios', 'Marketing']
    categorias = []
    for i, nome in enumerate(nomes, start=1):
        categorias.append({
            'id': i,
            'nome': nome,
            'descricao': fake.sentence(nb_words=10)
        })
    return categorias

def gerar_progresso_aulas(dados_matriculas, dados_aulas):
    progresso = []
    progresso_id = 1
    aulas_por_curso = {}
    for aula in dados_aulas:
        aulas_por_curso.setdefault(aula['modulo_id'], []).append(aula)

    for matricula in dados_matriculas:
        aulas_escolhidas = random.sample(dados_aulas, random.randint(0, len(dados_aulas)))
        for aula in aulas_escolhidas:
            concluida = random.random() < 0.7
            progresso.append({
                'id': progresso_id,
                'matricula_id': matricula['id'],
                'aula_id': aula['id'],
                'concluida': concluida,
                'data_conclusao': gerar_data_historica() if concluida else None,
                'tempo_assistido_minutos': random.randint(0, aula['duracao_minutos']) if concluida else 0
            })
            progresso_id += 1
    return progresso

def gerar_avaliacoes(dados_matriculas, dados_cursos):
    avaliacoes = []
    avaliacao_id = 1
    for matricula in dados_matriculas:
        if random.random() < 0.6:
            avaliacoes.append({
                'id': avaliacao_id,
                'matricula_id': matricula['id'],
                'curso_id': matricula['curso_id'],
                'nota': random.randint(3, 5),
                'comentario': fake.sentence(nb_words=15),
                'data_avaliacao': gerar_data_historica()
            })
            avaliacao_id += 1
    return avaliacoes
