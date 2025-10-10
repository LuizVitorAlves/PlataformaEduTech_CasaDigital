# 🎓 Sistema de Gerenciamento de Cursos Online (EduTech)

## 🧠 Contexto do Projeto

Este projeto tem como objetivo **modelar o banco de dados de uma plataforma EduTech**, com foco em domínio de SQL e consultas avançadas, simulando um cenário real de backend para um sistema de cursos online.

---

## 🧱 Decisões de Modelagem

- **PostgreSQL** foi escolhido como SGBD por sua robustez e recursos avançados.  
- O modelo segue **normalização até a 3ª forma normal (3FN)** para reduzir redundâncias e garantir integridade.  
- Todas as tabelas possuem **chave primária** (`SERIAL + PRIMARY KEY`) e, quando aplicável, **chaves estrangeiras**.  
- Foram aplicadas **constraints** importantes:
  - `NOT NULL` para campos obrigatórios  
  - `UNIQUE` para e-mails e combinações que exigem unicidade  
  - `CHECK` para validações de valores permitidos (níveis, status, formas de pagamento etc.)  
- Campos com **alta frequência de consulta** receberam índices e/ou chaves únicas para otimização.  
- Alguns elementos extras foram adicionados para **simular um cenário de negócio mais realista**.  

---

## 📊 Descrição das Tabelas

| Tabela | Descrição |
|--------|------------|
| **alunos** | Informações cadastrais dos estudantes da plataforma. Inclui nome, e-mail único e datas de cadastro/nascimento. |
| **instrutores** | Dados dos instrutores, incluindo especialidade e biografia. |
| **categorias** | Agrupamentos temáticos para organizar os cursos. |
| **cursos** | Tabela central do sistema. Cada curso está ligado a um instrutor e a uma categoria. Contém preço, carga horária, nível e data de criação. |
| **modulos** | Divide o curso em seções temáticas. A ordem de cada módulo é única dentro do curso. |
| **aulas** | Elementos individuais de conteúdo. Podem ser vídeo, texto ou quiz. Cada módulo tem sua sequência definida. |
| **cupons** 🆕 | Gerencia códigos promocionais com valor fixo ou percentual e controle de uso. |
| **pedidos** 🆕 | Representa a fatura do aluno, armazenando valores brutos, descontos, valores finais e status do pedido. |
| **pagamentos** 🆕 | Detalhes da transação financeira real vinculada ao pedido. Inclui método de pagamento e status da transação. |
| **matriculas** | Registra a liberação de acesso de um aluno a um curso, vinculada a um pedido pago. |
| **progresso_aulas** | Rastreia quais aulas foram concluídas e quanto tempo o aluno assistiu. |
| **avaliacoes** | Cada matrícula pode gerar uma avaliação única para o curso. Inclui nota de 1 a 5 e comentário. |

---

## 🆕 Destaques e Diferenças da Modelagem Base

| Item | Original | Atual |
|------|-----------|--------|
| **Sistema de matrículas** | Matriculava direto aluno → curso | Agora está vinculado a **pedido**, permitindo rastrear compras |
| **Pagamentos** | Não existia | Adicionada tabela **pagamentos** com status e métodos (pix, débito, crédito) |
| **Cupons de desconto** | Não existia | Adicionada tabela **cupons** com validade, tipo e controle de uso |
| **Status do pedido** | Não existia | Implementado com `CHECK` (`pendente_pagamento`, `pago`, `cancelado`, `falha_processamento`) |
| **Unicidade** | Apenas para e-mails | Adicionadas combinações únicas (ex: `aluno_id` + `curso_id` em matriculas, `curso_id` + `ordem` em módulos etc.) |
| **Comentários no schema** | Não obrigatório | Foram adicionados `COMMENT ON` para documentar cada tabela e algumas colunas |

---
