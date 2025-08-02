"""
Pacote Core - Sistema Inteligente de Coleta e Análise Web
=========================================================

Este pacote contém os módulos principais para coleta de dados web,
processamento de conteúdo e análise usando inteligência artificial.

Módulos Disponíveis:
===================

📡 web_search.py
    Gerencia coleta de conteúdo de páginas web
    - Busca inteligente de URLs educacionais
    - Extração otimizada de texto
    - Limpeza e normalização de conteúdo

🤖 co.py
    Integração com API Cohere para IA
    - Factory de agentes especializados
    - Configuração segura de API keys
    - Tratamento robusto de erros

🔄 proces_response.py
    Sistema multi-agente para análise
    - Pipeline de 4 agentes especializados
    - Processamento sequencial estruturado
    - Geração de resumos e sínteses

🗂️ htmlcolect.py (Legacy)
    Funcionalidade anterior de coleta HTML
    - Mantido para compatibilidade
    - Substituído por web_search.py otimizado

Uso Básico:
==========

```python
from core.web_search import collect_web_pages, download_and_save_content
from core.proces_response import create_multi_agent_summary

# 1. Coleta dados da web
terms = ["python básico", "programação"]
urls = collect_web_pages(terms)
data = download_and_save_content(urls, "dados.json")

# 2. Análise com IA
create_multi_agent_summary("dados.json")
```

Configuração Necessária:
========================

1. Arquivo .env na raiz do projeto:
   ```
   COHERE_API_KEY=sua_chave_aqui
   ```

2. Dependências (requirements.txt):
   ```
   cohere>=4.0.0
   requests>=2.28.0
   beautifulsoup4>=4.11.0
   python-dotenv>=0.19.0
   ```

Arquitetura:
============

O sistema segue uma arquitetura em pipeline:

1. 🔍 Geração de Termos (IA) → 
2. 📡 Coleta Web (Automática) → 
3. 📝 Extração de Texto (Otimizada) → 
4. 🤖 Análise Multi-Agente (IA) → 
5. 📊 Síntese Final (Estruturada)

Autor: Marco
Data: Agosto 2025
Versão: 2.0
"""

# Imports principais para facilitar uso do pacote
from .co import create_agent, get_api_key, create_specialized_agents
from .web_search import (
    collect_web_pages, 
    download_and_save_content, 
    search_pages_for_term,
    extract_page_content
)
from .proces_response import (
    create_multi_agent_summary,
    process_with_multiple_agents
)

# Configurações do pacote
__version__ = "2.0.0"
__author__ = "Marco"
__description__ = "Sistema Inteligente de Coleta e Análise Web com IA"

# Exports principais
__all__ = [
    # Módulo co.py
    'create_agent',
    'get_api_key', 
    'create_specialized_agents',
    
    # Módulo web_search.py
    'collect_web_pages',
    'download_and_save_content',
    'search_pages_for_term',
    'extract_page_content',
    
    # Módulo proces_response.py
    'create_multi_agent_summary',
    'process_with_multiple_agents',
    
    # Metadados
    '__version__',
    '__author__',
    '__description__'
]
