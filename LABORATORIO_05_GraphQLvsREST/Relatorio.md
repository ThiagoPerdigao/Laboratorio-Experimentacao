# 📝 Relatório Técnico - Laboratório 05: GraphQL vs REST

## 1. Informações do grupo
- **🎓 Curso:** Engenharia de Software
- **📘 Disciplina:** Laboratório de Experimentação de Software
- **🗓 Período:** 6° Período
- **👨‍🏫 Professor(a):** Prof. Dr. João Paulo Carneiro Aramuni
- **👥 Membros do Grupo:** Matheus Hoske, Samuel Pinheiro, Ryan Cristian e Thiago Perdigão

---

## 2. Introdução
Este laboratório tem como objetivo conduzir um experimento controlado comparando quantitativamente as APIs GraphQL e REST em relação ao tempo de resposta e ao tamanho das respostas. Com o crescimento da adoção do GraphQL, torna-se importante avaliar empiricamente seus benefícios em cenários práticos.

### 2.1. Questões de Pesquisa (RQs)
| RQ | Pergunta de Pesquisa |
|----|----------------------|
| RQ01 | Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST? |
| RQ02 | Respostas às consultas GraphQL possuem tamanho menor que as respostas REST? |

## 3. Desenho do Experimento

### 3.1. Hipóteses

#### RQ01 — Tempo de Resposta
- H0: Não há diferença significativa no tempo de resposta entre GraphQL e REST.
- H1: Consultas GraphQL são mais rápidas que consultas REST.

#### RQ02 — Tamanho da Resposta
- H0: Não há diferença significativa no tamanho das respostas entre GraphQL e REST.
- H1: Respostas GraphQL são menores que respostas REST.

### 3.2. Variáveis

#### Variáveis Dependentes
- Tempo de resposta (ms)
- Tamanho da resposta (bytes)

#### Variáveis Independentes
- Tipo de API (GraphQL, REST)
- Cenário da consulta (Simples, Complexo)
- Usuário-alvo (octocat, torvalds, mojombo)

### 3.3. Tratamentos
| Código | Tratamento | Endpoint |
|--------|------------|----------|
| T1 | REST | https://api.github.com |
| T2 | GraphQL | https://api.github.com/graphql |

### 3.4. Objetos Experimentais
- Dados públicos da API do GitHub
- Usuários: octocat, torvalds, mojombo
- Entidades consultadas: usuários, repositórios, issues

### 3.5. Tipo de Projeto Experimental
- Within-subjects (medidas repetidas)
- Randomização da ordem de execução

### 3.6. Quantidade de Medições
- 30 repetições por tratamento por cenário
- Total: 120 medições (2 APIs × 2 cenários × 30 repetições)

## 4. Ameaças à Validade

| Tipo de Validade | Ameaça | Mitigação |
|------------------|--------|-----------|
| Interna | Variação de rede | Executar testes em horários de baixo tráfego |
| Interna | Cache influenciando resultados | Usar Cache-Control: no-cache |
| Interna | Rate limiting do GitHub | Utilizar token de autenticação |
| Externa | Baixa generalização | Testar com múltiplos usuários e cenários |
| De Construção | Medição inconsistente de tempo | Medir apenas rede + processamento |
| De Construção | Medição inconsistente de tamanho | Mensurar payload bruto (corpo + headers) |