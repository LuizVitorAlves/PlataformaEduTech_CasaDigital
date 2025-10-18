\set CURSO_ID_TESTE 3
\set NOME_CURSO_EXIBICAO (SELECT titulo FROM cursos WHERE id = :CURSO_ID_TESTE)

-- 1. Listar todos os cursos com nome da categoria e do instrutor.
\echo '---------------------------------------------------'
\echo 'CONSULTA 1: Cursos, Instrutor e Categoria'
\echo '---------------------------------------------------'
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
\echo '---------------------------------------------------'
\echo 'CONSULTA 2: Alunos Matriculados no Curso: '
\echo '---------------------------------------------------'
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
\echo '---------------------------------------------------'
\echo 'CONSULTA 3: Aulas Ordenadas do Curso: '
\echo '---------------------------------------------------'
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