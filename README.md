# Verzel Project — Plataforma de Eventos e Ingressos

Plataforma onde um organizador publica eventos (a partir de um catálogo) e clientes compram ingressos com QR Code, validados na portaria na entrada do evento.

Desenvolvido para o **Desafio Elite Dev 2026 - Verzel**.

## Stack

- **Frontend:** React + Vite + TypeScript, React Router, Context API (estado de autenticação)
- **Backend:** Python + FastAPI, SQLAlchemy (async) + Alembic
- **Banco de dados:** PostgreSQL (via Docker)
- **Autenticação:** JWT com 3 papéis (Organizador, Cliente, Portaria)
- **QR Code:** assinado com JWT (HMAC), não-forjável; renderizado com `qrcode.react`

## Arquitetura

Backend organizado por domínio, em camadas:

```
Router (API) → Service (regra de negócio) → Repository (acesso a dados) → SQLAlchemy → PostgreSQL
```

Domínios: `auth`, `events`, `reservations`, `tickets`. Cada um com sua própria anatomia (`router.py`, `service.py`, `repository.py`, `schemas.py`, `models.py`), evitando acoplamento entre eles.

Frontend organizado por domínio, no mesmo espírito: `domains/auth`, `domains/events`, `domains/reservations`, `domains/tickets`, `domains/gate`, `domains/organizer` — cada um com suas próprias páginas e chamadas de API.

## Pré-requisitos

- Python 3.11+
- Node.js 18+
- Docker Desktop (para o PostgreSQL)

## Configurando o backend

```bash
cd backend

# Cria e ativa o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# Instala as dependências
pip install -r requirements.txt

# Cria o arquivo .env na pasta backend/ com:
# DATABASE_URL=postgresql+asyncpg://elite:elite@localhost:5432/elite_dev_eventos
# SECRET_KEY=troque-essa-chave-em-producao
```

### Subindo o banco de dados

**Importante:** o Docker Desktop precisa estar aberto e rodando antes deste passo.

Na raiz do projeto (onde está o `docker-compose.yml`):
```bash
docker compose up -d db
```

Confirma que subiu:
```bash
docker ps
```
Deve aparecer o container `elite_dev_db` com status `healthy`.

### Aplicando as migrations

De volta em `backend/`:
```bash
alembic upgrade head
```

### Populando dados de teste (seed)

```bash
# Com o backend já rodando (veja o próximo passo), em outro terminal:
python seed.py
```

Isso cria:
- 1 organizador, 2 clientes, 1 usuário de portaria
- 1 evento publicado com 1 sessão e assentos disponíveis

**Credenciais de teste:**
| Papel | E-mail | Senha |
|---|---|---|
| Organizador | organizador@teste.com | senha123 |
| Cliente 1 | cliente@teste.com | senha123 |
| Cliente 2 | cliente2@teste.com | senha123 |
| Portaria | portaria@teste.com | senha123 |

### Rodando o backend

```bash
uvicorn app.main:app --reload
```

API disponível em `http://127.0.0.1:8000`. Documentação interativa (Swagger) em `http://127.0.0.1:8000/docs`.

## Configurando o frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse `http://127.0.0.1:5173`.

**Importante:** use `127.0.0.1`, não `localhost`, para evitar bloqueios de CORS que alguns navegadores/extensões apresentam com `localhost` em ambiente de desenvolvimento.

## Fluxo de uso

1. Acesse o frontend — você verá a tela de seleção de papel (Organizador / Cliente / Portaria)
2. **Organizador**: cria um evento a partir do catálogo mockado, cria uma sessão (define local, data, capacidade, preço e modo — mapa de assentos ou quantidade)
3. **Cliente**: navega pelos eventos publicados, reserva um assento, confirma o pagamento simulado, e visualiza o ingresso com QR Code em "Meus ingressos"
4. **Portaria**: valida o ingresso digitando/colando o código do QR e informando a sessão — recebe um dos 4 estados (válido, inválido, já utilizado, evento errado)

## Funcionalidades implementadas

- [x] Autenticação com 3 papéis distintos (JWT)
- [x] Catálogo de eventos (mockado, com adapter pronto para plugar TMDb — ver seção abaixo)
- [x] CRUD de eventos e sessões pelo organizador
- [x] Geração automática de mapa de assentos
- [x] Reserva de assento com trava real contra venda duplicada (lock de linha + índice único parcial no Postgres)
- [x] Pagamento simulado (confirmação e recusa aleatórias)
- [x] Geração de ingresso com QR assinado (JWT/HMAC) — não pode ser forjado
- [x] Validação de ingresso na portaria, com bloqueio de reuso
- [x] Área "Meus ingressos" com QR renderizado
- [x] Seed de dados de teste
- [x] Tela de seleção de papel antes do login, com bloqueio se a conta não corresponder ao papel escolhido
- [x] Auto-logout por inatividade (5 minutos)

## O que não foi implementado (limitações conhecidas)

- **Integração real com TMDb**: o catálogo usa um provider mockado (`MockCatalogProvider`). A arquitetura já isola essa dependência atrás de uma interface (`CatalogProvider`) — existe até um `TMDbCatalogProvider` esqueleto pronto em `app/domains/events/catalog.py`, faltando apenas configurar uma API key real.
- **Mapa de assentos visual**: a seleção de assento no frontend é uma lista simples de botões, não um mapa gráfico de cinema/teatro. A regra de negócio (trava de duplicidade) funciona igual; é uma decisão de escopo por prazo.
- **Leitura de QR por câmera**: a portaria aceita apenas digitação/colagem manual do código (que o edital aceita como alternativa válida). Não foi implementada leitura via câmera.
- **Docker Compose completo**: apenas o PostgreSQL roda em container. Backend e frontend rodam localmente via `uvicorn` e `npm run dev`.
- **Compartilhamento de ingresso via link**: não implementado nesta versão.
- **Reserva com múltiplos assentos por vez**: cada reserva cobre um único assento (modo mapa) ou uma quantidade (modo pista); não há seleção múltipla de assentos numa única reserva.
## Deploy

- Frontend: [preencher com a URL da Vercel após o deploy]
- Backend: [preencher com a URL do Railway/Render após o deploy]

## Problemas conhecidos / troubleshooting

- Se o backend não conectar ao banco (`Connection refused` na porta 5432), confirme que o Docker Desktop está aberto e o container `elite_dev_db` está rodando (`docker ps`).
- Se o Swagger ou o frontend travarem ao carregar via `localhost`, use `127.0.0.1` na URL.
- Foi necessário fixar `bcrypt==4.0.1` no `requirements.txt` por incompatibilidade entre versões recentes do `bcrypt` e o `passlib`.

## Uso de IA

Este projeto foi desenvolvido com apoio de IA (Claude, Anthropic) como assistente técnico ao longo de todo o desenvolvimento. Detalhes completos sobre como e onde a IA foi usada, incluindo erros reais encontrados e como foram corrigidos, estão documentados em [`IA.md`](./IA.md).

## Estrutura de pastas

```
verzel-project/
├── frontend/
│   └── src/
│       ├── domains/       # auth, events, reservations, tickets, gate, organizer
│       ├── components/    # componentes genéricos reutilizáveis
│       └── ...
├── backend/
│   ├── app/
│   │   ├── domains/       # auth, events, reservations, tickets
│   │   ├── core/          # config, database, security
│   │   └── main.py
│   ├── alembic/           # migrations
│   ├── seed.py
│   └── requirements.txt
├── docker-compose.yml
├── IA.md
└── README.md
```