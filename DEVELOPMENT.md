# Guia de Desenvolvimento - Task Manager

## 🛠️ Configuração do Ambiente de Desenvolvimento

### Pré-requisitos
- Python 3.8+
- Git
- Editor de código (VS Code, PyCharm, etc.)

### Setup Inicial

1. **Clone o repositório**
```bash
git clone <repository-url>
cd task_manager
```

2. **Execute o script de inicialização**
```bash
python setup.py
```

3. **Configure o ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

4. **Instale dependências de desenvolvimento**
```bash
pip install -r requirements.txt
pip install -e .  # Instala o projeto em modo desenvolvimento
```

## 📁 Estrutura do Projeto

```
task_manager/
├── modules/                    # Módulos principais
│   ├── __init__.py
│   ├── usuario.py             # Gerenciamento de usuários
│   ├── tag.py                 # Gerenciamento de tags
│   ├── time.py                # Gerenciamento de times
│   ├── tarefa.py              # Gerenciamento de tarefas
│   └── gerenciamento_tarefas.py # Orquestração principal
├── tests/                     # Testes automatizados
│   ├── test_*.py              # Testes unitários
│   └── run_tests.py           # Runner de testes
├── web/                       # Interface web
│   └── task_manager_web/      # Aplicação Flask
├── data/                      # Arquivos de dados (JSON)
├── logs/                      # Logs da aplicação
├── exports/                   # Arquivos exportados
├── docs/                      # Documentação
├── config.py                  # Configurações
├── utils.py                   # Utilitários
└── setup.py                   # Script de inicialização
```

## 🏗️ Arquitetura do Sistema

### Princípios de Design

1. **Modularidade**: Cada módulo tem responsabilidade única
2. **Encapsulamento**: Dados internos protegidos por interfaces
3. **Reutilização**: Funções e classes reutilizáveis
4. **Testabilidade**: Código facilmente testável
5. **Documentação**: Código bem documentado

### Padrões de Código

#### Nomenclatura
- **Funções**: `snake_case` (ex: `usuario_criar`)
- **Classes**: `PascalCase` (ex: `Usuario`)
- **Constantes**: `UPPER_CASE` (ex: `MAX_NOME_LENGTH`)
- **Variáveis**: `snake_case` (ex: `nome_usuario`)

#### Estrutura de Módulos
```python
"""
Módulo de [Nome]

Descrição do módulo e suas responsabilidades.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

# Imports de configuração
from config import CONSTANTES

# Classe principal
class MinhaClasse:
    """Documentação da classe"""
    pass

# Funções públicas
def minha_funcao_criar(param1: str, param2: int) -> Optional[MinhaClasse]:
    """
    Cria uma nova instância.
    
    Args:
        param1: Descrição do parâmetro
        param2: Descrição do parâmetro
    
    Returns:
        Instância criada ou None em caso de erro
    """
    pass

# Funções de acesso
def minha_funcao_get_propriedade(instancia: MinhaClasse) -> str:
    """Obtém propriedade da instância"""
    pass
```

## 🧪 Desenvolvimento Orientado a Testes (TDD)

### Estrutura de Testes

Cada módulo deve ter seu arquivo de teste correspondente:
- `modules/usuario.py` → `tests/test_usuario.py`
- `modules/tag.py` → `tests/test_tag.py`

### Padrão de Testes

```python
import unittest
from modules.meu_modulo import minha_funcao

class TestMeuModulo(unittest.TestCase):
    """Testes para o módulo"""
    
    def setUp(self):
        """Preparação antes de cada teste"""
        pass
    
    def tearDown(self):
        """Limpeza após cada teste"""
        pass
    
    def test_01_caso_sucesso(self):
        """Teste de caso de sucesso"""
        # Arrange
        dados = "dados de teste"
        
        # Act
        resultado = minha_funcao(dados)
        
        # Assert
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.propriedade, "valor esperado")
    
    def test_02_caso_erro(self):
        """Teste de caso de erro"""
        resultado = minha_funcao(None)
        self.assertIsNone(resultado)
```

### Executando Testes

```bash
# Todos os testes
python tests/run_tests.py

# Teste específico
python -m unittest tests.test_usuario -v

# Com cobertura
python -m pytest --cov=modules tests/
```

## 🌐 Desenvolvimento Web

### Estrutura da API

As rotas da API seguem o padrão RESTful:

```python
# src/routes/minha_rota.py
from flask import Blueprint, request, jsonify

minha_bp = Blueprint('minha_rota', __name__)

@minha_bp.route('/endpoint', methods=['GET'])
def listar():
    """Lista recursos"""
    return jsonify({'data': []})

@minha_bp.route('/endpoint', methods=['POST'])
def criar():
    """Cria novo recurso"""
    data = request.get_json()
    # Lógica de criação
    return jsonify({'success': True}), 201
```

### Frontend

O frontend utiliza:
- **HTML5**: Estrutura semântica
- **Tailwind CSS**: Estilização utilitária
- **JavaScript Vanilla**: Interatividade
- **Chart.js**: Gráficos
- **Lucide Icons**: Ícones

Estrutura do JavaScript:
```javascript
// Estado global
let appState = {
    currentSection: 'dashboard',
    data: []
};

// API Client
const api = {
    async request(endpoint, options = {}) {
        // Lógica de requisição
    }
};

// UI Components
const ui = {
    showLoading: () => {},
    hideLoading: () => {},
    showToast: (message, type) => {}
};
```

## 📊 Persistência de Dados

### Formato JSON

Os dados são armazenados em arquivos JSON:

```json
{
  "usuarios": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@email.com",
      "data_criacao": "2024-01-01T10:00:00"
    }
  ]
}
```

### Funções de Persistência

```python
# utils.py
def salvar_json(dados: Dict, arquivo: str) -> bool:
    """Salva dados em arquivo JSON"""
    pass

def carregar_json(arquivo: str) -> Dict:
    """Carrega dados de arquivo JSON"""
    pass
```

## 🔧 Configuração e Constantes

### config.py

```python
from enum import Enum

# Códigos de retorno
SUCESSO = 0
ERRO = -1

# Limites
MAX_NOME_LENGTH = 100
MAX_EMAIL_LENGTH = 150

# Enums
class StatusTarefa(Enum):
    TAREFA_ABERTA = "TAREFA_ABERTA"
    TAREFA_EM_PROGRESSO = "TAREFA_EM_PROGRESSO"
    TAREFA_CONCLUIDA = "TAREFA_CONCLUIDA"

# Arquivos de dados
USUARIOS_FILE = "data/usuarios.json"
TAGS_FILE = "data/tags.json"
TIMES_FILE = "data/times.json"
TAREFAS_FILE = "data/tarefas.json"
```

## 🐛 Debug e Logging

### Configuração de Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Debug da Aplicação Web

```python
# Para debug do Flask
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 📝 Documentação

### Docstrings

Use o formato Google/NumPy:

```python
def minha_funcao(param1: str, param2: int = 0) -> bool:
    """
    Descrição breve da função.
    
    Descrição mais detalhada se necessário.
    
    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2 (opcional)
    
    Returns:
        True se sucesso, False caso contrário
    
    Raises:
        ValueError: Se param1 for inválido
    
    Example:
        >>> minha_funcao("teste", 5)
        True
    """
    pass
```

### Comentários

```python
# Comentário de linha explicando lógica complexa

"""
Comentário de bloco para explicar
seções importantes do código
"""
```

## 🚀 Deploy e Distribuição

### Preparação para Deploy

1. **Atualize requirements.txt**
```bash
pip freeze > requirements.txt
```

2. **Execute todos os testes**
```bash
python tests/run_tests.py
```

3. **Verifique a documentação**
```bash
# Gere documentação se necessário
```

### Checklist de Release

- [ ] Todos os testes passando
- [ ] Documentação atualizada
- [ ] Requirements.txt atualizado
- [ ] Versão atualizada em `__init__.py`
- [ ] CHANGELOG.md atualizado
- [ ] README.md revisado

## 🤝 Contribuição

### Fluxo de Trabalho

1. **Fork** do repositório
2. **Clone** do seu fork
3. **Crie branch** para feature (`git checkout -b feature/nova-feature`)
4. **Desenvolva** seguindo os padrões
5. **Teste** suas mudanças
6. **Commit** com mensagem clara
7. **Push** para sua branch
8. **Pull Request** com descrição detalhada

### Padrões de Commit

```
tipo(escopo): descrição breve

Descrição mais detalhada se necessário

Fixes #123
```

Tipos:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas de manutenção

### Code Review

Pontos de atenção:
- [ ] Código segue padrões estabelecidos
- [ ] Testes cobrem as mudanças
- [ ] Documentação atualizada
- [ ] Performance não foi degradada
- [ ] Não introduz vulnerabilidades

## 📚 Recursos Adicionais

### Ferramentas Recomendadas

- **IDE**: VS Code com extensões Python
- **Linting**: flake8, black
- **Type Checking**: mypy
- **Testing**: pytest
- **Documentation**: Sphinx

### Links Úteis

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Chart.js](https://www.chartjs.org/)

---

**Happy Coding! 🚀**

