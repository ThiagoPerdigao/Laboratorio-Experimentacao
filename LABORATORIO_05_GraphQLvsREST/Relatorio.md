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

## 5. Resultados

Os resultados apresentados abaixo foram extraidos das 120 medições realizadas para cada combinação de API (REST vs GraphQL) e cenário (simples vs complexo).

### 5.1. Resultados Consolidados

| API      | Cenario   | Tempo Medio (ms) | Tamanho Medio (bytes) |
|----------|-----------|------------------|------------------------|
| REST     | Simple    | ~260 ms          | ~2560 bytes            |
| REST     | Complex   | ~340 ms          | ~42576 bytes           |
| GraphQL  | Simple    | ~295 ms          | ~1184 bytes            |
| GraphQL  | Complex   | ~850-900 ms      | ~2177 bytes            |

### 5.2. Interpretacao

- REST foi consistentemente mais rapido, tanto no cenario simples quanto no complexo.
- GraphQL retornou cargas significativamente menores, especialmente no cenario complexo.
- No cenario complexo, GraphQL apresentou tempo maior devido ao custo de resolucao de campos aninhados no servidor.

---

## 6. Analise Estatistica

### 6.1. Teste t independente

Foram aplicados testes t para comparar medias de tempo e tamanho entre REST e GraphQL.

#### Tempo de resposta
- REST foi significativamente mais rapido (p < 0.05).
- GraphQL apresentou maior variabilidade no cenario complexo.

#### Tamanho da resposta
- GraphQL retornou respostas significativamente menores (p < 0.001).

### 6.2. Conclusao dos Testes
- Ha evidencia estatistica para rejeitar H0 em ambos os casos.
- GraphQL difere significativamente de REST tanto em tempo quanto em tamanho.

---

## 7. Discussao

### 7.1. Vantagens observadas do REST
- Tempo de resposta menor.
- Arquitetura mais simples.
- Menor custo computacional do lado do servidor.

### 7.2. Vantagens observadas do GraphQL
- Grande economia de dados transferidos.
- Flexibilidade na selecao de campos.
- Melhor escalabilidade para front-end.

### 7.3. Interpretacao dos resultados
O GraphQL se mostrou mais eficiente em transferencia de dados, mas nao em tempo de resposta. Isso se deve ao processamento adicional exigido pela resolucao da arvore de consultas.

No cenario simples, REST e GraphQL possuem tempos proximos. No cenario complexo, REST se manteve estavel enquanto GraphQL sofreu aumento de latencia.

---

## 8. Conclusoes

### RQ01 - O GraphQL eh mais rapido que o REST?
Resposta: Nao.  
REST demonstrou menor tempo de resposta em ambos os cenarios.

### RQ02 - O GraphQL possui tamanho de resposta menor?
Resposta: Sim.  
GraphQL retornou respostas notavelmente menores, especialmente em requests complexas.

### Sintese Geral
- REST vence em tempo.
- GraphQL vence em tamanho.
- A escolha depende da prioridade da aplicacao (latencia vs economia de dados).

---

## 9. Trabalhos Futuros

- Executar testes sob carga concorrente.
- Avaliar o uso de persistent queries no GraphQL.
- Considerar cenarios com paginas maiores (pagination).
- Medir impacto em redes moveis lentas.
- Comparar com outras APIs alem do GitHub.

---

## 10. Conclusao Final

Os dados mostram que:
- REST e mais rapido.
- GraphQL e mais enxuto.
- GraphQL e REST nao se substituem; se complementam.
- A decisao depende de requisitos especificos do sistema.

