\COPY alunos FROM 'data/alunos.csv' DELIMITER ',' CSV HEADER;
\COPY instrutores FROM 'data/instrutores.csv' DELIMITER ',' CSV HEADER;
\COPY categorias FROM 'data/categorias.csv' DELIMITER ',' CSV HEADER;
\COPY cupons FROM 'data/cupons.csv' DELIMITER ',' CSV HEADER;

\COPY cursos FROM 'data/cursos.csv' DELIMITER ',' CSV HEADER;
\COPY modulos FROM 'data/modulos.csv' DELIMITER ',' CSV HEADER;
\COPY aulas FROM 'data/aulas.csv' DELIMITER ',' CSV HEADER;

\COPY pedidos FROM 'data/pedidos.csv' DELIMITER ',' CSV HEADER NULL 'None';
\COPY pagamentos FROM 'data/pagamentos.csv' DELIMITER ',' CSV HEADER NULL 'None';

\COPY matriculas FROM 'data/matriculas.csv' DELIMITER ',' CSV HEADER NULL 'None';
\COPY progresso_aulas FROM 'data/progresso_aulas.csv' DELIMITER ',' CSV HEADER NULL 'None';
\COPY avaliacoes FROM 'data/avaliacoes.csv' DELIMITER ',' CSV HEADER NULL 'None';

SELECT setval('alunos_id_seq', (SELECT max(id) FROM alunos), true);
SELECT setval('instrutores_id_seq', (SELECT max(id) FROM instrutores), true);
SELECT setval('categorias_id_seq', (SELECT max(id) FROM categorias), true);
SELECT setval('cupons_id_seq', (SELECT max(id) FROM cupons), true);

SELECT setval('cursos_id_seq', (SELECT max(id) FROM cursos), true);
SELECT setval('modulos_id_seq', (SELECT max(id) FROM modulos), true);
SELECT setval('aulas_id_seq', (SELECT max(id) FROM aulas), true);

SELECT setval('pedidos_id_seq', (SELECT max(id) FROM pedidos), true);
SELECT setval('pagamentos_id_seq', (SELECT max(id) FROM pagamentos), true);

SELECT setval('matriculas_id_seq', (SELECT max(id) FROM matriculas), true);
SELECT setval('progresso_aulas_id_seq', (SELECT max(id) FROM progresso_aulas), true);
SELECT setval('avaliacoes_id_seq', (SELECT max(id) FROM avaliacoes), true);

\echo 'Importação e ajustes concluídos!'