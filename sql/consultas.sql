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