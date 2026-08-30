# Uso de IA no projeto

Esse documento existe pra ser transparente sobre onde e como usei IA durante o desenvolvimento, como pede o edital do desafio.

## Ferramenta utilizada

Usei o Claude (Anthropic) como assistente durante praticamente todo o projeto, num formato de mentoria contínua — não como gerador de código pronto que eu simplesmente copio e colo, mas como um "dev sênior" com quem discuto decisões, que revisa o que eu trago e me aponta erros, trade-offs e alternativas antes de eu implementar.

## Como usei

**Planejamento e arquitetura**
- Discussão de stack (Python/FastAPI no back, React/Vite/TypeScript no front, Postgres) e os porquês de cada escolha frente ao meu histórico técnico e ao prazo de 7 dias
- Definição da estrutura de pastas por domínio (backend e frontend), incluindo a separação entre o que é genuinamente compartilhado (`components/`, `shared/`) e o que pertence a um domínio específico
- Modelagem do banco de dados: entidades, relacionamentos, decisões de PK/FK e das constraints que impedem venda duplicada de assento (índice único parcial no Postgres)
- Decisão consciente de manter o catálogo de eventos isolado atrás de uma interface (`CatalogProvider`), para que trocar o mock por uma integração real com TMDb no futuro exija mudar uma única linha, sem tocar em service ou router
- No frontend, escolha de Context API em vez de Zustand/Redux para o estado de autenticação, por ser o menor mecanismo que resolve o problema (usuário logado + token), sem dependência extra
- Discussão sobre cortes de escopo dado o prazo: mapa de assentos visual (virou lista simples), leitura de QR por câmera (virou digitação manual, que o edital aceita), Docker Compose completo (só o Postgres roda em container)

**Geração de código**
- Boa parte dos arquivos base foi gerada com apoio da IA, seguindo a arquitetura em camadas definida em conjunto (Router → Service → Repository → SQLAlchemy no backend; páginas por domínio consumindo `api.ts` próprio no frontend): models, schemas, services, repositories e routers de todos os domínios (auth, events, reservations, tickets), e as páginas React de cada fluxo (login, seleção de papel, listagem de eventos, reserva, pagamento, meus ingressos, portaria, painel do organizador)
- Todo código gerado foi lido, testado por mim manualmente pelo navegador/Swagger e ajustado quando necessário — não foi copy-paste cego

**Debugging (processo real, com erros de verdade)**
Documento aqui os problemas reais que apareceram e como foram resolvidos, porque muitos vieram de código gerado por IA que não funcionou de primeira ou de edições minhas que colaram trecho novo sem remover o antigo — o que reforça por que reviso e testo tudo antes de aceitar como pronto:

*Backend:*
- `env.py` do Alembic gerado numa tentativa anterior tinha bugs de ordem (`config` sendo usado antes de ser definido) e uma atribuição de `target_metadata` sendo sobrescrita por `None` logo depois
- Conflito de compatibilidade entre `passlib` e versões recentes do `bcrypt` (`bcrypt` >= 4.1 removeu um atributo que o `passlib` usa pra auto-detecção), causando um erro confuso de "senha maior que 72 bytes" sem relação real com o tamanho da senha — resolvido fixando `bcrypt==4.0.1`
- Erro de ordem no `main.py`: `app.include_router(...)` chamado antes de `app = FastAPI(...)` existir (aconteceu mais de uma vez, ao adicionar novos routers)
- Método `list_by_session` colado na classe errada (`ReservationRepository` em vez de `SeatRepository`) por causa da indentação, quebrando a listagem de assentos até eu perceber pelo `AttributeError`
- Endpoint `pay_reservation` duplicado no router — a versão nova (que gera o ticket) foi colada abaixo da antiga sem remover a antiga; como o FastAPI usa a primeira definição encontrada, o pagamento funcionava mas o ticket nunca era gerado, até eu comparar as duas versões e apagar a obsoleta
- Import faltando (`SeatStatus`) ao criar o schema `SeatOut`
- Ambiente WSL2/Docker Desktop não configurado — precisou habilitar componentes do Windows via `dism.exe`, reiniciar, e só depois instalar o Docker Desktop; Docker Desktop precisa estar aberto manualmente a cada sessão de trabalho (não inicia sozinho com o Windows)

*Frontend:*
- Rota raiz (`/`) sumiu do `App.tsx` ao adicionar uma rota nova — colei a rota de reserva substituindo a de eventos em vez de adicionar ao lado, causando "No routes matched location /"
- Mesmo erro se repetiu com a rota `/my-tickets`, faltando simplesmente porque ainda não tinha sido criada quando testei o botão que apontava pra ela
- CORS bloqueando o frontend: o Vite subiu na porta `5174` (porque a `5173` já estava ocupada por outra instância esquecida rodando), e o backend só liberava `5173` — resolvido liberando as duas portas no CORS
- Arquivos salvos no editor mas esquecidos sem `Ctrl+S`, fazendo uma rota nova (`/tickets/validate`) "não existir" até eu perceber que o problema era só isso
- "Failed to fetch" no login pela segunda vez, causado por interceptação de `localhost` pelo navegador — resolvido usando `127.0.0.1` nas URLs locais, tanto no backend quanto no frontend

## O que fiz sem IA

- Toda a execução prática: rodar comandos no terminal, criar pastas e arquivos, ativar ambiente virtual, configurar Docker Desktop e WSL2 na minha máquina
- Testes manuais de cada endpoint via Swagger (`/docs`) e depois pelo próprio frontend no navegador, validando cada fluxo (registro, login, criação de evento, reserva, pagamento, geração de ticket, validação na portaria) nos 3 papéis antes de seguir pra próxima etapa
- Organização do backlog no Jira (épicos, stories, priorização do Sprint 1)
- Todos os commits e a forma como estruturei o histórico do Git
- Decisões finais sobre modelagem (por exemplo, aceitar o modelo com `seat_id`/`quantity` nullable em vez de tabelas separadas, ciente do trade-off de normalização) e sobre UX (exigir que o papel escolhido na tela inicial bata com o papel real da conta, em vez de deixar como só um enfeite visual)
- Identificação de vários dos bugs listados acima a partir do comportamento real na tela ou dos logs do terminal, antes mesmo de pedir ajuda pra IA revisar o código

## Por que documentar assim

Fica mais fácil de avaliar (e mais honesto da minha parte) mostrar que não é um sistema que "saiu pronto" de um prompt único: cada camada foi construída em etapas, testada, e quando teve bug — teve mesmo, de código gerado e de configuração de ambiente — o processo de identificar e corrigir também faz parte do que estou entregando.