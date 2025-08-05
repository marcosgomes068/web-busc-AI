# 🤖 Web-Busc-AI: Sistema Inteligente de Busca e Análise Web

Sistema avançado que combina web scraping inteligente com análise multi-agente usando IA (Cohere) para coletar, processar e sintetizar conteúdo educacional sobre qualquer tema de forma automatizada.

## 🌟 Características Principais

- **🧠 Multi-Agente IA**: Sistema com 4 agentes especializados (Resumidor, Analista, Organizador, Sintetizador)
- **🎨 Interface Rica**: Terminal profissional com Rich library e fallback compatibility
- **📡 Web Scraping Inteligente**: Coleta automática de conteúdo educacional de alta qualidade
- **🔍 Busca Contextual**: Geração automática de termos de busca usando IA
- **📊 Análise Estruturada**: Processamento sequencial com relatórios executivos detalhados
- **💾 Armazenamento JSON**: Dados estruturados e facilmente reutilizáveis
- **� Integração C#**: Suporte completo para integração com aplicações .NET
- **�🛡️ Tratamento Robusto**: Gestão avançada de erros e fallbacks

## 🏗️ Arquitetura do Sistema

```
🔍 Geração de Termos (IA Cohere) 
    ↓
📡 Coleta Web (Automática + Validação)
    ↓  
📝 Extração de Texto (Otimizada)
    ↓
🤖 Análise Multi-Agente (4 Especialistas IA)
    ↓
📊 Síntese Executiva Final (2000+ tokens)
```

### 🤖 Agentes Especializados

1. **📝 Resumidor**: Condensação inteligente de conteúdo
2. **🔍 Analista**: Identificação de padrões e insights
3. **📋 Organizador**: Estruturação e categorização
4. **🎯 Sintetizador**: Síntese executiva com 6 seções detalhadas

## 📋 Pré-requisitos

- **Python 3.8+**
- **Chave API Cohere** (gratuita em [cohere.ai](https://cohere.ai))
- **Rich Library** (para interface terminal profissional)
- **Conexão com Internet**

## 🚀 Instalação Rápida

### 1. Clone o repositório
```bash
git clone https://github.com/marcosgomes068/web-busc-AI.git
cd web-busc-AI
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a API Cohere
Crie um arquivo `.env` na raiz do projeto:
```env
COHERE_API_KEY=sua_chave_aqui
```

### 4. Execute o sistema
```bash
python main.py
```

## 📦 Dependências

| Biblioteca | Versão | Descrição |
|------------|--------|-----------|
| `cohere` | ≥4.0.0 | Cliente oficial da API Cohere |
| `requests` | ≥2.28.0 | Requisições HTTP |
| `beautifulsoup4` | ≥4.11.0 | Parsing de HTML |
| `python-dotenv` | ≥0.19.0 | Carregamento de variáveis de ambiente |

## 🎯 Uso Básico

### Exemplo Simples
```python
from core.web_search import collect_web_pages, download_and_save_content
from core.proces_response import create_multi_agent_summary

# 1. Definir termos de busca
search_terms = ["machine learning", "python basics"]

# 2. Coletar URLs
collected_urls = collect_web_pages(search_terms, max_pages=5)

# 3. Extrair conteúdo e salvar
data = download_and_save_content(collected_urls, "dados_ml.json")

# 4. Análise com múltiplos agentes
create_multi_agent_summary("dados_ml.json")
```

### Exemplo Completo
```python
import main

# Busca completa automatizada
terms, urls, data = main.search("inteligência artificial")

# Ou apenas análise de dados existentes
main.summarize_only("inteligência artificial")
```

## 🧬 Agentes Especializados

### 🤖 Resumidor
- **Função**: Extrai pontos principais
- **Foco**: Concisão e clareza
- **Output**: Resumos objetivos

### 🔍 Analista  
- **Função**: Identifica insights e tendências
- **Foco**: Análise técnica aprofundada
- **Output**: Padrões e informações relevantes

### 📊 Organizador
- **Função**: Estrutura informações logicamente
- **Foco**: Hierarquia e categorização
- **Output**: Conteúdo organizado sistematicamente

### 🎯 Sintetizador
- **Função**: Cria síntese final unificada
- **Foco**: Integração e coerência
- **Output**: Documento final estruturado

## 📁 Estrutura do Projeto

```
projeto/
├── main.py                 # 🚀 Módulo principal - orquestra todo fluxo
├── requirements.txt        # 📦 Dependências do projeto  
├── .env                   # 🔑 Configurações da API (não versionado)
├── README.md              # 📖 Este arquivo
│
├── core/                  # 📚 Pacote principal
│   ├── __init__.py        # 🏠 Inicialização do pacote
│   ├── co.py             # 🤖 Integração Cohere API
│   ├── web_search.py     # 📡 Coleta e extração web
│   ├── proces_response.py # 🔄 Sistema multi-agente
│   └── htmlcolect.py     # 🗂️ Módulo legacy (compatibilidade)
│
└── outputs/               # 📊 Arquivos gerados (criado automaticamente)
    ├── dados_*.json       # 📄 Dados coletados estruturados
    ├── resumos_parciais_*.txt  # 📋 Análises individuais
    └── sintese_final_*.txt     # 🎯 Síntese final unificada
```

## ⚙️ Configuração Avançada

### Personalizando Agentes
```python
from core.co import create_agent

# Criar agente personalizado
custom_agent = create_agent(
    "Você é especialista em [ÁREA]. Foque em [ASPECTOS].",
    max_tokens=500
)

# Usar agente
result = custom_agent("Texto para analisar...")
```

### Configurando Coleta Web
```python
from core.web_search import collect_web_pages

# Busca personalizada
urls = collect_web_pages(
    search_terms=["termo1", "termo2"],
    max_pages=10  # Mais páginas por termo
)
```

### Processamento Customizado
```python
from core.proces_response import process_with_multiple_agents

# Análise de arquivo específico
process_with_multiple_agents("meu_arquivo.json")
```

## 📊 Outputs Gerados

### 1. Dados Coletados (`dados_*.json`)
```json
{
  "metadata": {
    "data_coleta": "2025-01-XX...",
    "total_termos": 5,
    "total_urls": 25
  },
  "dados": {
    "termo1": [
      {
        "url": "https://...",
        "titulo": "...",
        "conteudo_texto": "...",
        "status": "sucesso"
      }
    ]
  }
}
```

### 2. Resumos Parciais (`resumos_parciais_*.txt`)
```
TERMO: machine learning
================================================

📋 RESUMO:
Machine learning é uma subárea da IA...

🔍 ANÁLISE:  
Principais tendências identificadas...

📊 ORGANIZAÇÃO:
1. Conceitos Fundamentais
2. Algoritmos Principais
3. Aplicações Práticas
```

### 3. Síntese Final (`sintese_final_*.txt`)
```
SÍNTESE FINAL - SISTEMA MULTI-AGENTE
===============================================

📋 RESUMO EXECUTIVO
...

🎯 PRINCIPAIS INSIGHTS POR TEMA
...

📈 TENDÊNCIAS E PADRÕES IDENTIFICADOS
...
```

## 🔧 Troubleshooting

### ❌ Erro de API Cohere
```bash
# Verificar chave da API
python -c "from core.co import test_api_connection; test_api_connection()"
```

### ❌ Erro de Rede
- Verificar conexão com internet
- Alguns sites podem bloquear bots (comportamento esperado)
- Taxa de sucesso típica: 70-90%

### ❌ Arquivo JSON não encontrado
```python
# Verificar se o arquivo existe
import os
print(os.path.exists("dados_seu_tema.json"))

# Executar coleta primeiro
main.search("seu tema")
```

## 🤝 Contribuições

1. **Fork** o projeto
2. **Clone** seu fork
3. **Crie** uma branch para sua feature
4. **Faça** commit das mudanças
5. **Push** para a branch
6. **Abra** um Pull Request

### Diretrizes de Contribuição
- Use docstrings detalhadas
- Siga PEP 8 para formatação
- Adicione type hints
- Inclua testes quando possível
- Mantenha compatibilidade com versões anteriores

## 📝 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🏆 Versioning

Usamos [SemVer](http://semver.org/) para versionamento. Para versões disponíveis, veja as [tags neste repositório](https://github.com/seu-usuario/sistema-coleta-web/tags).

**Versão Atual: 2.0.0**

### Changelog
- **v2.0.0**: Sistema multi-agente completo, refatoração clean code
- **v1.5.0**: Otimização de extração de texto, múltiplos agentes
- **v1.0.0**: Versão inicial com coleta web básica

## 👨‍💻 Autor

**Marco** - [GitHub](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- **Cohere AI** pela API de inteligência artificial
- **BeautifulSoup** pela biblioteca de parsing HTML
- **Requests** pela biblioteca HTTP robusta
- **Comunidade Python** pelo suporte e documentação
  
---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela! ⭐**

</div>

