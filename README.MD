# 🎯 Pinnacle Drop Detector

Scraper modular e extensível para coleta contínua de odds esportivas da Pinnacle no mercado de futebol 1x2, com foco em organização por domínio, concorrência controlada e fácil evolução para notificações e persistência externa.

## Visão Geral

O sistema automatiza o ciclo de vida de coleta de dados de apostas, focando em alta performance e organização.

    Coleta Periódica: Ligas, partidas e odds sincronizadas automaticamente.

    Concorrência Controlada: Uso de ThreadPoolExecutor para processamento paralelo.

    Conversão de Dados: Transformação automática de odds Americanas para Decimais.

    Detecção de Eventos: Motor de notificações para eventos específicos (ex: queda brusca de odds).

    Thread-Safety: Repositórios em memória protegidos para acesso concorrente.

### Arquitetura e Estrutura

O projeto divide-se em camadas para isolar a lógica de negócio das implementações externas:

```text
odds_scope/
├── core/
│   ├── domain/     # Modelos, contratos (interfaces) e regras puras.
│   ├── infra/      # Implementações (Pinnacle API, Repositories, Scheduler).
│   ├── services/   # Orquestração, coordenação e lógica de atualização.
│   └── utils/      # Helpers e utilitários de conversão.
├── config/         # Configurações de ambiente e parâmetros da API.
└── main.py         # Entry point da aplicação.
```

Domain: Define as entidades (League, Match, Odd) e as interfaces que a infraestrutura deve seguir.

Infra: Lida com a comunicação externa (API da Pinnacle) e o agendamento de tarefas (APScheduler).

Services: Coordena o fluxo de dados entre a infraestrutura e o domínio, aplicando filtros e consolidando informações.

### Fluxo de Execução

Ao iniciar o main.py, o sistema segue este fluxo:

    Bootstrapping: Inicializa autenticação, clientes API e repositórios.

    Scheduling: O CoordinatorScheduler ativa dois jobs principais:

        Ligas: Atualização do catálogo (padrão: 120s).

        Partidas/Odds: Coleta e consolidação de dados vivos (padrão: 15s).

    Processamento:

        Coleta concorrente via ThreadPoolExecutor.

        Filtros de validade (ex: remover partidas encerradas ou próximas do início).

        Disparo de notificações baseadas em estratégias.

### Autenticação e Segurança

A autenticação é resiliente e dinâmica:

    IAuthProvider: Interface que permite trocar o provedor de autenticação.

    PinnacleKeyManager: Obtém chaves de API automaticamente de endpoints públicos.

    Auto-Renewal: Tokens expirados ou inválidos são detectados e renovados automaticamente pelo AuthenticatedClient.

### Estratégias de Notificação

O sistema utiliza o padrão Strategy para monitorar o mercado. Atualmente suporta:

    OddDropStrategy: Detecta quedas significativas de valor (ex: ≥ 10%) em intervalos curtos.

    Extensibilidade: Novos alertas (ex: Surebets, Valuebets) podem ser adicionados criando novas classes em services/notifier/ sem alterar o código existente.

### Como executar

## Instalação
Certifique-se de ter o Python 3.8 ou superior instalado. Instale as dependências necessárias com:
```bash
pip install -r requirements.txt
```

## Uso
Para executar o cálculo do SPI:
```bash
python main.py
```

O processo permanece ativo até interrupção manual (Ctrl + C).
    
