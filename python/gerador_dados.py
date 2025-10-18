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
            'email': nome_completo.lower().replace(' ', '.') + "@gmail.com",
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
        if not cursos_do_pedido: continue 
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
        gateway_id = str(fake.uuid4()) if status_pg == 'aprovado' else None
        pagamento = {
            'id': pagamento_id_counter,
            'pedido_id': pedido_id_counter,
            'metodo_pagamento': random.choice(metodos_pagamento),
            'id_transacao_gateway': gateway_id,
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
    
    combinacoes_unicas = set() 
    for pedido in pedidos_pagos:
        data_pedido_dt = datetime.fromisoformat(pedido['data_pedido'])
        data_matricula = (data_pedido_dt + timedelta(minutes=random.randint(65, 120))).isoformat()
        for curso in pedido['cursos_comprados']: 
            aluno_id = pedido['aluno_id']
            curso_id = curso['id']
            chave_unica = (aluno_id, curso_id)
            if chave_unica not in combinacoes_unicas:
                matriculas.append({
                    'id': matricula_id_counter,
                    'aluno_id': aluno_id,
                    'curso_id': curso_id,
                    'pedido_id': pedido['id'],
                    'data_matricula': data_matricula,
                    'data_conclusao': None, 
                    'status': 'ativa'
                })
                combinacoes_unicas.add(chave_unica)
                matricula_id_counter += 1
    return matriculas

def gerar_categorias(quantidade):
    nomes_base = ['Programação', 'Design', 'Dados', 'DevOps', 'Negócios', 'Marketing', 'Finanças', 'Idiomas', 'Culinária', 'Fotografia']
    categorias = []
    num_a_gerar = min(quantidade, len(nomes_base)) 
    for i in range(1, num_a_gerar + 1):
        categorias.append({
            'id': i,
            'nome': nomes_base[i-1], 
            'descricao': fake.sentence(nb_words=10)
        })
    return categorias

def gerar_progresso_e_avaliacoes(dados_matriculas, dados_modulos, dados_aulas):
    progresso = []
    avaliacoes = []
    progresso_id_counter = 1
    
    aulas_por_curso = {}
    curso_por_modulo = {m['id']: m['curso_id'] for m in dados_modulos}
    
    for aula in dados_aulas:
        if aula['modulo_id'] in curso_por_modulo:
            curso_id = curso_por_modulo[aula['modulo_id']]
            aulas_por_curso.setdefault(curso_id, []).append(aula)
        
    for matricula in dados_matriculas:
        curso_id = matricula['curso_id']
        aulas_validas = aulas_por_curso.get(curso_id, [])
        if not aulas_validas: continue
        taxa_conclusao = random.uniform(0.10, 1.0)
        total_aulas = len(aulas_validas)
        aulas_a_concluir = int(total_aulas * taxa_conclusao)
        for aula in random.sample(aulas_validas, aulas_a_concluir): 
            concluida = True
            data_conclusao_aula = fake.date_time_between(
                start_date=datetime.fromisoformat(matricula['data_matricula']), 
                end_date=DATA_MAX_GLOBAL
            ).isoformat()
            progresso.append({
                'id': progresso_id_counter,
                'matricula_id': matricula['id'],
                'aula_id': aula['id'],
                'concluida': concluida,
                'data_conclusao': data_conclusao_aula,
                'tempo_assistido_minutos': max(0, random.randint(aula['duracao_minutos'] - 5, aula['duracao_minutos'])),
            })
            progresso_id_counter += 1
        if taxa_conclusao >= 0.50 and random.random() < 0.25:
            avaliacoes.append({
                'id': len(avaliacoes) + 1,
                'matricula_id': matricula['id'], 
                'curso_id': matricula['curso_id'],
                'nota': random.randint(3, 5),
                'comentario': fake.sentence(nb_words=15),
                'data_avaliacao': gerar_data_historica()
            })
        if taxa_conclusao >= 0.99:
            matricula['status'] = 'concluida'
            matricula['data_conclusao'] = data_conclusao_aula.split('T')[0]
    return progresso, avaliacoes

def executar_gerador_cli():
    print("Bem vindo a Plataforma EduTech! Vamos gerar seus dados?\n")

    QTD_ALUNOS = obter_quantidade("alunos", 30)
    QTD_INSTRUTORES = obter_quantidade("instrutores", 10)
    QTD_CATEGORIAS = obter_quantidade("categorias", 5)
    QTD_CURSOS = obter_quantidade("cursos", 20)
    QTD_CUPONS = obter_quantidade("cupons", 5)
    QTD_PEDIDOS = obter_quantidade("pedidos", 80) 
    
    print("\nLoading alunos...")
    dados_alunos = gerar_alunos(QTD_ALUNOS)
    exportar_para_csv(dados_alunos, 'alunos')
    
    print("\nLoading instrutores...")
    dados_instrutores = gerar_instrutores(QTD_INSTRUTORES)
    exportar_para_csv(dados_instrutores, 'instrutores')
    
    print("\nLoading categorias...")
    dados_categorias = gerar_categorias(QTD_CATEGORIAS)
    exportar_para_csv(dados_categorias, 'categorias')
    
    print("\nLoading cupons...")
    dados_cupons = gerar_cupons(QTD_CUPONS)
    exportar_para_csv(dados_cupons, 'cupons')

    instrutores_ids = [i['id'] for i in dados_instrutores]
    categorias_ids = [c['id'] for c in dados_categorias]
    
    print("\nLoading cursos...")
    dados_cursos = gerar_cursos(QTD_CURSOS, instrutores_ids, categorias_ids)
    exportar_para_csv(dados_cursos, 'cursos')

    print("\nLoading modulos...")
    print("\nLoading aulas...")
    dados_modulos, dados_aulas = gerar_modulos_e_aulas(dados_cursos)
    exportar_para_csv(dados_modulos, 'modulos')
    exportar_para_csv(dados_aulas, 'aulas')

    print("\nLoading pedidos...")
    print("\nLoading pagamentos...")
    dados_pedidos, dados_pagamentos = gerar_pedidos_e_pagamentos(
        dados_alunos, dados_cursos, dados_cupons, QTD_PEDIDOS
    )
    pedidos_para_export = [{k: v for k, v in p.items() if k != 'cursos_comprados'} for p in dados_pedidos]
    exportar_para_csv(pedidos_para_export, 'pedidos')
    exportar_para_csv(dados_pagamentos, 'pagamentos')

    print("\nLoading matriculas...")
    dados_matriculas = gerar_matriculas(dados_pedidos)
    exportar_para_csv(dados_matriculas, 'matriculas')
    
    print("\nLoading matriculas concluidas...")
    print("\nLoading progresso de aulas...")
    print("\nLoading avaliações...")
    dados_progresso, dados_avaliacoes = gerar_progresso_e_avaliacoes(
        dados_matriculas, dados_modulos, dados_aulas
    )
    exportar_para_csv(dados_matriculas, 'matriculas') 
    exportar_para_csv(dados_progresso, 'progresso_aulas')
    exportar_para_csv(dados_avaliacoes, 'avaliacoes')

    print("🎉 Geração de Todos os CSVs Concluída!")


if __name__ == '__main__':
    executar_gerador_cli()