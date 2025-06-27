# Task Manager - Sistema de Gerenciamento de Tarefas

## 📋 Visão Geral

O Task Manager é um sistema completo de gerenciamento de tarefas desenvolvido em Python, seguindo uma arquitetura modular bem definida. O sistema oferece uma interface web moderna e intuitiva para gerenciar tarefas, usuários, times e tags de forma eficiente.

## ✨ Características Principais

- **Arquitetura Modular**: Sistema organizado em módulos independentes e reutilizáveis
- **Interface Web Moderna**: Interface responsiva e intuitiva desenvolvida com HTML5, CSS3 e JavaScript
- **API RESTful**: API completa para integração com outras aplicações
- **Persistência de Dados**: Sistema de armazenamento em arquivos JSON
- **Testes Automatizados**: Cobertura completa de testes unitários
- **Documentação Completa**: Documentação detalhada de todos os módulos e funcionalidades

## 🏗️ Arquitetura do Sistema

### Módulos Principais

1. **Módulo Usuario** (`modules/usuario.py`)
   - Gerenciamento de usuários do sistema
   - Validação de dados e emails
   - Operações CRUD completas

2. **Módulo Tag** (`modules/tag.py`)
   - Sistema de tags para categorização
   - Suporte a cores personalizadas
   - Validação de cores hexadecimais

3. **Módulo Time** (`modules/time.py`)
   - Gerenciamento de equipes
   - Adição/remoção de membros
   - Controle de quantidade de membros

4. **Módulo Tarefa** (`modules/tarefa.py`)
   - Gerenciamento completo de tarefas
   - Sistema de status (Aberta, Em Progresso, Concluída)
   - Associação com usuários, times e tags
   - Controle de prazos

5. **Módulo Gerenciamento de Tarefas** (`modules/gerenciamento_tarefas.py`)
   - Orquestração de todos os módulos
   - Persistência de dados
   - Operações de alto nível
   - Exportação de dados

### Interface Web

- **Frontend**: HTML5, CSS3 (Tailwind CSS), JavaScript
- **Backend**: Flask com API RESTful
- **Recursos**: Dashboard, CRUD completo, filtros, gráficos, notificações

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe o projeto**
```bash
# Se usando git
git clone <repository-url>
cd task_manager

# Ou extraia o arquivo ZIP baixado
```

2. **Configure o ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### Estrutura de Diretórios

```
task_manager/
├── modules/                    # Módulos principais do sistema
│   ├── __init__.py
│   ├── usuario.py             # Módulo de usuários
│   ├── tag.py                 # Módulo de tags
│   ├── time.py                # Módulo de times
│   ├── tarefa.py              # Módulo de tarefas
│   └── gerenciamento_tarefas.py # Módulo principal
├── tests/                     # Testes automatizados
│   ├── __init__.py
│   ├── test_usuario.py
│   ├── test_tag.py
│   ├── test_time.py
│   ├── test_tarefa.py
│   ├── test_gerenciamento_tarefas.py
│   └── run_tests.py           # Script para executar testes
├── web/                       # Interface web
│   └── task_manager_web/      # Aplicação Flask
│       ├── src/
│       │   ├── main.py        # Aplicação principal
│       │   ├── routes/        # Rotas da API
│       │   └── static/        # Arquivos estáticos (HTML, CSS, JS)
│       └── venv/              # Ambiente virtual do Flask
├── docs/                      # Documentação
├── config.py                  # Configurações do sistema
├── utils.py                   # Utilitários comuns
└── README.md                  # Este arquivo
```

## 🖥️ Como Usar

### 1. Executando a Interface Web

```bash
# Navegue até o diretório da aplicação web
cd web/task_manager_web

# Ative o ambiente virtual
source venv/bin/activate

# Execute a aplicação
python src/main.py
```

A aplicação estará disponível em: `http://localhost:5000`

### 2. Usando a API

A API RESTful está disponível em `http://localhost:5000/api` com os seguintes endpoints:

#### Usuários
- `GET /api/users` - Lista todos os usuários
- `POST /api/users` - Cria um novo usuário
- `GET /api/users/{id}` - Obtém um usuário específico
- `PUT /api/users/{id}` - Atualiza um usuário

#### Times
- `GET /api/teams` - Lista todos os times
- `POST /api/teams` - Cria um novo time
- `GET /api/teams/{id}` - Obtém um time específico
- `PUT /api/teams/{id}` - Atualiza um time
- `POST /api/teams/{id}/members/{user_id}` - Adiciona membro ao time
- `DELETE /api/teams/{id}/members/{user_id}` - Remove membro do time

#### Tags
- `GET /api/tags` - Lista todas as tags
- `POST /api/tags` - Cria uma nova tag
- `GET /api/tags/{id}` - Obtém uma tag específica
- `PUT /api/tags/{id}` - Atualiza uma tag

#### Tarefas
- `GET /api/tasks` - Lista todas as tarefas
- `POST /api/tasks` - Cria uma nova tarefa
- `GET /api/tasks/{id}` - Obtém uma tarefa específica
- `PUT /api/tasks/{id}` - Atualiza uma tarefa
- `DELETE /api/tasks/{id}` - Remove uma tarefa
- `GET /api/tasks/stats` - Obtém estatísticas das tarefas

### 3. Executando Testes

```bash
# Execute todos os testes
python tests/run_tests.py

# Execute testes de um módulo específico
python tests/run_tests.py usuario
python tests/run_tests.py tag
python tests/run_tests.py time
python tests/run_tests.py tarefa
```

### 4. Usando os Módulos Diretamente

```python
# Exemplo de uso direto dos módulos
from modules.usuario import usuario_criar, usuario_get_nome
from modules.tarefa import tarefa_criar
from modules.gerenciamento_tarefas import gt_inicializar

# Inicializa o sistema
gt = gt_inicializar()

# Cria um usuário
usuario = usuario_criar("João Silva", "joao@email.com")
print(f"Usuário criado: {usuario_get_nome(usuario)}")

# Registra no sistema
from modules.gerenciamento_tarefas import gt_registrar_usuario
gt_registrar_usuario(gt, usuario)
```

## 📊 Funcionalidades da Interface Web

### Dashboard
- Visão geral com estatísticas
- Gráfico de status das tarefas
- Lista de tarefas recentes
- Cards informativos

### Gerenciamento de Tarefas
- Criação de tarefas com título, descrição, prazo
- Associação com usuários e times
- Sistema de tags com cores
- Alteração de status (Aberta → Em Progresso → Concluída)
- Filtros por status, usuário e time
- Exclusão de tarefas

### Gerenciamento de Usuários
- Cadastro de usuários com nome e email
- Listagem em tabela
- Visualização de tarefas por usuário
- Edição de informações

### Gerenciamento de Times
- Criação de times
- Adição/remoção de membros
- Visualização de tarefas por time
- Controle de quantidade de membros

### Gerenciamento de Tags
- Criação de tags com cores personalizadas
- Seletor de cores visual
- Visualização em grid
- Edição de tags existentes

## 🧪 Testes

O sistema possui uma suíte completa de testes automatizados que cobrem:

- **Testes de Unidade**: Cada módulo possui testes específicos
- **Testes de Integração**: Testes do módulo de gerenciamento
- **Testes de API**: Validação dos endpoints da API
- **Testes de Validação**: Verificação de regras de negócio

### Executando Testes

```bash
# Todos os testes
python tests/run_tests.py

# Teste específico
python -m unittest tests.test_usuario -v
```

## 📁 Persistência de Dados

O sistema utiliza arquivos JSON para persistência:

- `data/usuarios.json` - Dados dos usuários
- `data/tags.json` - Dados das tags
- `data/times.json` - Dados dos times
- `data/tarefas.json` - Dados das tarefas

Os arquivos são criados automaticamente na primeira execução.

## 🔧 Configuração

As configurações do sistema estão em `config.py`:

```python
# Constantes de retorno
SUCESSO = 0
ERRO = -1

# Limites de caracteres
MAX_NOME_LENGTH = 100
MAX_EMAIL_LENGTH = 150
MAX_TITULO_LENGTH = 200
MAX_DESCRICAO_LENGTH = 1000

# Status das tarefas
class StatusTarefa(Enum):
    TAREFA_ABERTA = "TAREFA_ABERTA"
    TAREFA_EM_PROGRESSO = "TAREFA_EM_PROGRESSO"
    TAREFA_CONCLUIDA = "TAREFA_CONCLUIDA"
```

## 🐛 Solução de Problemas

### Problemas Comuns

1. **Erro de importação de módulos**
   - Verifique se está no diretório correto
   - Certifique-se de que o Python está encontrando os módulos

2. **Erro ao iniciar a aplicação web**
   - Verifique se as dependências estão instaladas
   - Confirme se o ambiente virtual está ativado

3. **Testes falhando**
   - Execute os testes individualmente para identificar o problema
   - Verifique se os módulos estão sendo importados corretamente

### Logs e Depuração

O sistema gera logs das operações principais. Para depuração:

```python
# Ative o modo debug no Flask
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Equipe de Desenvolvimento** - Implementação inicial

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no repositório
- Consulte a documentação completa em `/docs`

---

**Task Manager** - Sistema de Gerenciamento de Tarefas Modular e Eficiente

