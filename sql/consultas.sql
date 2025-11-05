\set CURSO_ID_TESTE 3
\set NOME_CURSO_EXIBICAO (SELECT titulo FROM cursos WHERE id = :CURSO_ID_TESTE)

-- 1. Listar todos os cursos com nome da categoria e do instrutor.
\echo '\n---------------------------------------------------'
\echo 'CONSULTA 1: Cursos, Instrutor e Categoria'
\echo '---------------------------------------------------\n'
SELECT
    c.titulo AS "Nome do Curso",
    i.nome AS "Instrutor",
    cat.nome AS "Categoria",
    c.nivel AS "Nível",
    c.preco AS "Preço"
FROM
    cursos c
JOIN
    instrutores i ON c.instrutor_id = i.id
JOIN
    categorias cat ON c.categoria_id = cat.id
ORDER BY
    c.data_criacao DESC;

-- 2. Listar todos os alunos matriculados em um curso específico.
\echo '\n---------------------------------------------------'
\echo 'CONSULTA 2: Alunos Matriculados no Curso: '
\echo '---------------------------------------------------\n'
SELECT
    a.nome AS "Nome do Aluno",
    a.email,
    m.data_matricula
FROM
    alunos a
JOIN
    matriculas m ON a.id = m.aluno_id
WHERE
    m.curso_id = :CURSO_ID_TESTE
ORDER BY
    m.data_matricula;

-- 3. Exibir todas as aulas de um curso ordenadas por módulo e ordem.
\echo '\n---------------------------------------------------'
\echo 'CONSULTA 3: Aulas Ordenadas do Curso: '
\echo '---------------------------------------------------\n'
SELECT
    m.ordem AS "Módulo Ordem",
    m.titulo AS "Módulo",
    a.ordem AS "Aula Ordem",
    a.titulo AS "Aula",
    a.tipo,
    a.duracao_minutos || ' min' AS "Duração"
FROM
    cursos c
JOIN
    modulos m ON c.id = m.curso_id
JOIN
    aulas a ON m.id = a.modulo_id
WHERE
    c.id = :CURSO_ID_TESTE
ORDER BY
    m.ordem ASC,
    a.ordem ASC;

-- 4. Calcular a média de avaliações de cada curso
\echo '\n---------------------------------------------------'
\echo 'CONSULTA 4: Média de Avaliações por Curso'
\echo '---------------------------------------------------\n'
SELECT
    c.titulo AS "Curso",
    TO_CHAR(AVG(a.nota), '9.99') AS "Média de Avaliações"
FROM
    cursos c
JOIN
    avaliacoes a ON c.id = a.curso_id
GROUP BY
    c.id, c.titulo
ORDER BY
    "Média de Avaliações" DESC;

-- 5. Contar quantos alunos estão matriculados por curso
\echo '\n---------------------------------------------------'
\echo 'CONSULTA 5: Total de Alunos por Curso'
\echo '---------------------------------------------------\n'
SELECT
    c.titulo AS "Curso",
    COUNT(m.aluno_id) AS "Total de Alunos Matriculados"
FROM
    cursos c
JOIN
    matriculas m ON c.id = m.curso_id
GROUP BY
    c.id, c.titulo
ORDER BY
    "Total de Alunos Matriculados" DESC;

-- 6. Calcular o faturamento total por categoria
\echo '\n---------------------------------------------------'
\echo 'CONSULTA 6: Faturamento Bruto por Categoria'
\echo '---------------------------------------------------\n'
SELECT
    cat.nome AS "Categoria",
    TO_CHAR(SUM(c.preco), 'L99G999D99') AS "Faturamento Bruto Gerado"
FROM
    categorias cat
JOIN
    cursos c ON cat.id = c.categoria_id
JOIN
    matriculas m ON c.id = m.curso_id
JOIN
    pedidos ped ON m.pedido_id = ped.id
WHERE
    ped.status_pedido = 'pago'
GROUP BY
    cat.nome
ORDER BY
    SUM(c.preco) DESC;