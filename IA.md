# Uso de IA no projeto

Esse documento existe pra ser transparente sobre onde e como usei IA durante o desenvolvimento, como pede o edital do desafio.

## Ferramenta utilizada

Usei o Claude (Anthropic) como assistente durante praticamente todo o projeto, num formato de mentoria contínua — não como gerador de código pronto que eu simplesmente copio e colo, mas como um "dev sênior" com quem discuto decisões, que revisa o que eu trago e me aponta erros, trade-offs e alternativas antes de eu implementar.

## Como usei

**Planejamento e arquitetura**
- Discussão de stack (Python/FastAPI no back, React/Vite no front, Postgres) e os porquês de cada escolha frente ao meu histórico técnico e ao prazo de 7 dias
- Definição da estrutura de pastas por domínio (backend e frontend), incluindo a separação entre o que é genuinamente compartilhado (`components/`, `shared/`) e o que pertence a um domínio específico
- Modelagem do banco de dados: entidades, relacionamentos, decisões de PK/FK e das constraints que impedem venda duplicada de assento (índice único parcial no Postgres)

**Geração de código**
- Boa parte dos arquivos base (models SQLAlchemy, schemas Pydantic, service, repository, router de autenticação) foi gerada com apoio da IA, seguindo a arquitetura em camadas que definimos juntos (API → Service → Repository → SQLAlchemy)
- Todo código gerado foi lido, testado por mim e ajustado quando necessário — não foi copy-paste cego

**Debugging (processo real, com erros de verdade)**
Documento aqui os problemas reais que apareceram e como foram resolvidos, porque muitos vieram de código gerado por IA que não funcionou de primeira — o que reforça por que reviso tudo antes de aceitar:

- `env.py` do Alembic gerado numa tentativa anterior tinha bugs de ordem (`config` sendo usado antes de ser definido) e uma atribuição de `target_metadata` sendo sobrescrita por `None` logo depois — corrigido manualmente após eu mandar o conteúdo pra revisão
- Conflito de compatibilidade entre `passlib` e versões recentes do `bcrypt` (`bcrypt` >= 4.1 removeu um atributo que o `passlib` usa pra auto-detecção), causando um erro confuso de "senha maior que 72 bytes" que na verdade não tinha relação com o tamanho da senha — resolvido fixando `bcrypt==4.0.1`
- Erro de ordem no `main.py`: `app.include_router(...)` chamado antes de `app = FastAPI(...)` existir
- Ambiente WSL2/Docker Desktop não configurado — precisou habilitar componentes do Windows via `dism.exe`, reiniciar, e só depois instalar o Docker Desktop
- Navegador (Edge) travando ao acessar `localhost:8000`, sem erro nenhum — resolvido usando `127.0.0.1` em vez de `localhost` nas URLs locais

## O que fiz sem IA

- Toda a execução prática: rodar comandos no terminal, criar pastas e arquivos, ativar ambiente virtual, configurar Docker Desktop e WSL2 na minha máquina
- Testes manuais de cada endpoint via Swagger (`/docs`), validando registro e login antes de seguir pra próxima etapa
- Organização do backlog no Jira (épicos, stories, priorização do Sprint 1)
- Todos os commits e a forma como estruturei o histórico do Git
- Decisões finais sobre modelagem (por exemplo, aceitar o modelo com `seat_id`/`quantity` nullable em vez de tabelas separadas, ciente do trade-off de normalização)

## Por que documentar assim

Fica mais fácil de avaliar (e mais honesto da minha parte) mostrar que não é um sistema que "saiu pronto" de um prompt único: cada camada foi construída em etapas, testada, e quando teve bug — teve mesmo, de código gerado e de configuração de ambiente — o processo de identificar e corrigir também faz parte do que estou entregando.