CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    data_nascimento DATE,
    data_cadastro TIMESTAMP NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE alunos IS 'Tabela de informações dos estudantes da plataforma EduTech.';

CREATE TABLE instrutores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    especialidade VARCHAR(100),
    biografia TEXT
);
COMMENT ON TABLE instrutores IS 'Tabela de informações dos instrutores e professores.';

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    descricao TEXT
);
COMMENT ON TABLE categorias IS 'Tabela das categorias temáticas dos cursos.';

CREATE TABLE cursos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    categoria_id INTEGER NOT NULL REFERENCES categorias(id),
    instrutor_id INTEGER NOT NULL REFERENCES instrutores(id),
    preco NUMERIC(5, 2) NOT NULL CHECK (preco >= 0),
    carga_horaria INTEGER NOT NULL CHECK (carga_horaria > 0),
    nivel VARCHAR(20) NOT NULL CHECK (nivel IN ('iniciante', 'intermediario', 'avancado')),
    data_criacao TIMESTAMP NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE cursos IS 'Tabela central dos cursos ofertados na plataforma.';

CREATE TABLE modulos (
    id SERIAL PRIMARY KEY,
    curso_id INTEGER NOT NULL REFERENCES cursos(id),
    titulo VARCHAR(150) NOT NULL,
    ordem INTEGER NOT NULL,
    descricao TEXT,
    UNIQUE (curso_id, ordem)
);
COMMENT ON COLUMN modulos.ordem IS 'Ordem sequencial do módulo dentro do curso.';

CREATE TABLE aulas (
    id SERIAL PRIMARY KEY,
    modulo_id INTEGER NOT NULL REFERENCES modulos(id),
    titulo VARCHAR(150) NOT NULL,
    ordem INTEGER NOT NULL,
    duracao_minutos INTEGER CHECK (duracao_minutos >= 0),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('video', 'texto', 'quiz')),
    UNIQUE (modulo_id, ordem)
);
COMMENT ON COLUMN aulas.tipo IS 'Tipo de conteúdo da aula: video, texto ou quiz.';

CREATE TABLE cupons (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('percentual', 'fixo')),
    valor_desconto NUMERIC(5, 2) NOT NULL CHECK (valor_desconto > 0),
    data_expiracao DATE,
    uso_maximo INTEGER CHECK (uso_maximo >= 0),
    usos_atuais INTEGER DEFAULT 0 CHECK (usos_atuais >= 0)
);
COMMENT ON TABLE cupons IS 'Gerenciamento de códigos promocionais e regras de desconto.';

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES alunos(id),
    data_pedido TIMESTAMP NOT NULL DEFAULT NOW(),
    cupom_id INTEGER REFERENCES cupons(id),
    valor_bruto NUMERIC(5, 2) NOT NULL CHECK (valor_bruto >= 0),
    valor_desconto_aplicado NUMERIC(5, 2) NOT NULL DEFAULT 0 CHECK (valor_desconto_aplicado >= 0),
    valor_final NUMERIC(5, 2) NOT NULL CHECK (valor_final >= 0),
    status_pedido VARCHAR(30) NOT NULL CHECK (status_pedido IN ('pendente_pagamento', 'pago', 'cancelado', 'falha_processamento')),
    UNIQUE (aluno_id, data_pedido)
);
COMMENT ON TABLE pedidos IS 'Representa a fatura (Ordem de Serviço) criada pelo aluno para compra de cursos.';

CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
    metodo_pagamento VARCHAR(50) NOT NULL CHECK (metodo_pagamento IN ('debito', 'credito', 'pix')),
    id_transacao_gateway VARCHAR(100) UNIQUE,
    valor_pago NUMERIC(5, 2) NOT NULL CHECK (valor_pago > 0),
    data_pagamento TIMESTAMP NOT NULL DEFAULT NOW(),
    status_transacao VARCHAR(30) NOT NULL CHECK (status_transacao IN ('aprovado', 'falhou', 'estornado', 'pendente'))
);
COMMENT ON TABLE pagamentos IS 'Detalhes da transação financeira real para um pedido.';

CREATE TABLE matriculas (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES alunos(id),
    curso_id INTEGER NOT NULL REFERENCES cursos(id),
    pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
    data_matricula TIMESTAMP NOT NULL DEFAULT NOW(),
    data_conclusao DATE,
    istatus VARCHAR(20) NOT NULL CHECK (istatus IN ('ativa', 'concluida', 'cancelada')),
    UNIQUE (aluno_id, curso_id)
);
COMMENT ON TABLE matriculas IS 'Relacionamento N:M: Registra a liberação de acesso (após pagamento) aos cursos.';

CREATE TABLE progresso_aulas (
    id SERIAL PRIMARY KEY,
    matricula_id INTEGER NOT NULL REFERENCES matriculas(id),
    aula_id INTEGER NOT NULL REFERENCES aulas(id),
    concluida BOOLEAN NOT NULL DEFAULT FALSE,
    data_conclusao TIMESTAMP WITHOUT TIME ZONE,
    tempo_assistido_minutos INTEGER CHECK (tempo_assistido_minutos >= 0),
    UNIQUE (matricula_id, aula_id)
);
COMMENT ON TABLE progresso_aulas IS 'Rastreia o progresso do aluno em cada aula individual.';

CREATE TABLE avaliacoes (
    id SERIAL PRIMARY KEY,
    matricula_id INTEGER NOT NULL UNIQUE REFERENCES matriculas(id),
    curso_id INTEGER NOT NULL REFERENCES cursos(id),
    nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP NOT NULL DEFAULT NOW()
);
COMMENT ON TABLE avaliacoes IS 'Avaliações e notas dadas pelos alunos aos cursos.';
