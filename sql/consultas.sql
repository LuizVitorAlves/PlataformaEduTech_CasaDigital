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

-- 7. Identificar o curso com maior número de matrículas ativas
\echo '\n---------------------------------------------------'
\echo 'CONSULTA 7: Curso com Mais Matrículas Ativas'
\echo '---------------------------------------------------\n'
SELECT
    c.titulo AS "Curso",
    COUNT(m.id) AS "Total de Matrículas Ativas"
FROM
    cursos c
JOIN
    matriculas m ON c.id = m.curso_id
WHERE
    m.status = 'ativa'
GROUP BY
    c.id, c.titulo
ORDER BY
    "Total de Matrículas Ativas" DESC
LIMIT 1;

-- 8. Listar alunos, cursos matriculados e porcentagem de conclusão
\echo '\n---------------------------------------------------'
\echo 'CONSULTA 8: Progresso dos Alunos por Curso (com CTEs)'
\echo '---------------------------------------------------\n'

-- CTE 1: Contar o total de aulas de cada curso
WITH TotalAulasPorCurso AS (
    SELECT
        c.id AS curso_id,
        COUNT(a.id) AS total_aulas
    FROM
        cursos c
    JOIN
        modulos m ON c.id = m.curso_id
    JOIN
        aulas a ON m.id = a.modulo_id
    GROUP BY
        c.id
),

-- CTE 2: Contar quantas aulas foram concluídas por cada matrícula
AulasConcluidasPorMatricula AS (
    SELECT
        pa.matricula_id,
        COUNT(pa.id) AS aulas_concluidas
    FROM
        progresso_aulas pa
    WHERE
        pa.concluida = TRUE 
    GROUP BY
        pa.matricula_id
)

-- Principal que é juntar tudo
SELECT
    al.nome AS "Aluno",
    c.titulo AS "Curso",
    COALESCE(ac.aulas_concluidas, 0) AS "Aulas Concluídas",
    ta.total_aulas AS "Total de Aulas",
    TO_CHAR(
        (COALESCE(ac.aulas_concluidas, 0) * 100.0) / ta.total_aulas,
        '990.99'
    ) || '%' AS "Progresso"
FROM
    matriculas m
JOIN
    alunos al ON m.aluno_id = al.id
JOIN
    cursos c ON m.curso_id = c.id
JOIN
    TotalAulasPorCurso ta ON c.id = ta.curso_id
LEFT JOIN
    AulasConcluidasPorMatricula ac ON m.id = ac.matricula_id
WHERE
    ta.total_aulas > 0
ORDER BY
    al.nome, "Progresso" DESC;