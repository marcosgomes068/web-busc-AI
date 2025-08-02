"""
Módulo Legacy de Coleta HTML
============================

⚠️ AVISO: Este módulo é mantido apenas para compatibilidade.
Use o módulo web_search.py para funcionalidades atualizadas.

Funcionalidades Legacy:
- Carregamento de dados JSON (substituído)
- Coleta HTML completa (ineficiente)
- Processamento básico (sem otimizações)

Migração Recomendada:
====================

EM VEZ DE:
```python
from core.htmlcolect import carregar_dados_json
dados = carregar_dados_json("arquivo.json")
```

USE:
```python
import json
with open("arquivo.json", 'r', encoding='utf-8') as f:
    dados = json.load(f)
```

EM VEZ DE:
```python
from core.htmlcolect import baixar_html_completo
html = baixar_html_completo(urls)
```

USE:
```python
from core.web_search import download_and_save_content
dados = download_and_save_content(urls, "arquivo.json")
```

Autor: Marco
Data: Agosto 2025 (Legacy)
Status: Deprecated - Use web_search.py
"""

import json
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import time
from typing import Dict, Any, List, Optional


def carregar_dados_json(arquivo_json: str = "dados_coletados.json") -> Optional[Dict[str, Any]]:
    """
    [LEGACY] Carrega dados do arquivo JSON.
    
    ⚠️ DEPRECATED: Use json.load() diretamente.
    
    Args:
        arquivo_json (str): Caminho para o arquivo JSON
    
    Returns:
        Optional[Dict[str, Any]]: Dados carregados ou None se erro
    """
    print("⚠️ AVISO: Função legacy em uso. Considere migrar para json.load()")
    
    try:
        if not os.path.exists(arquivo_json):
            print(f"❌ Arquivo {arquivo_json} não encontrado!")
            return None
            
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print(f"✅ Dados carregados de: {arquivo_json}")
        return dados
    
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo JSON: {e}")
        return None
        return None

def extrair_html_completo(url, timeout=15):
    """
    Extrai o HTML completo de uma URL
    
    Args:
        url (str): URL para extrair o HTML
        timeout (int): Timeout em segundos
    
    Returns:
        dict: Dicionário com HTML completo e metadados
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        print(f"  Extraindo HTML de: {url[:80]}...")
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        
        # Detectar encoding
        encoding = resp.encoding if resp.encoding else 'utf-8'
        html_content = resp.content.decode(encoding, errors='ignore')
        
        # Extrair metadados básicos com BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Título
        titulo = soup.find("title")
        titulo = titulo.get_text().strip() if titulo else "Sem título"
        
        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        descricao = meta_desc.get("content", "").strip() if meta_desc else ""
        
        # Meta keywords
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        keywords = meta_keywords.get("content", "").strip() if meta_keywords else ""
        
        return {
            "url": url,
            "titulo": titulo,
            "descricao": descricao,
            "keywords": keywords,
            "html_completo": html_content,
            "tamanho_html": len(html_content),
            "encoding": encoding,
            "status_code": resp.status_code,
            "content_type": resp.headers.get('content-type', ''),
            "status": "sucesso",
            "timestamp": datetime.now().isoformat()
        }
        
    except requests.exceptions.Timeout:
        return {
            "url": url,
            "status": "erro: timeout",
            "timestamp": datetime.now().isoformat()
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status": f"erro: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "url": url,
            "status": f"erro: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def processar_todos_links(dados_json, delay=1):
    """
    Processa todos os links do JSON e extrai o HTML completo
    
    Args:
        dados_json (dict): Dados carregados do JSON
        delay (int): Delay em segundos entre requisições
    
    Returns:
        dict: Dados com HTML completo adicionado
    """
    if not dados_json or "dados" not in dados_json:
        print("Dados JSON inválidos!")
        return None
    
    dados_com_html = {
        "metadata": {
            "data_processamento": datetime.now().isoformat(),
            "total_termos": len(dados_json["dados"]),
            "delay_usado": delay
        },
        "dados": {}
    }
    
    total_urls = 0
    urls_processadas = 0
    
    # Contar total de URLs
    for termo, paginas in dados_json["dados"].items():
        total_urls += len(paginas)
    
    print(f"\nIniciando extração de HTML de {total_urls} URLs...")
    
    for termo, paginas in dados_json["dados"].items():
        print(f"\nProcessando termo: {termo}")
        dados_com_html["dados"][termo] = []
        
        for i, pagina in enumerate(paginas, 1):
            if "url" in pagina:
                url = pagina["url"]
                print(f"  {i}/{len(paginas)} - URL {urls_processadas + 1}/{total_urls}")
                
                # Extrair HTML completo
                html_data = extrair_html_completo(url)
                
                # Combinar dados originais com HTML
                dados_combinados = {**pagina, **html_data}
                dados_com_html["dados"][termo].append(dados_combinados)
                
                urls_processadas += 1
                
                # Delay entre requisições para não sobrecarregar
                if delay > 0 and urls_processadas < total_urls:
                    time.sleep(delay)
            else:
                # Manter dados originais se não tiver URL
                dados_com_html["dados"][termo].append(pagina)
    
    return dados_com_html

def salvar_html_completo(dados_com_html, arquivo_saida="dados_com_html.json"):
    """
    Salva os dados com HTML completo em um arquivo JSON
    
    Args:
        dados_com_html (dict): Dados com HTML extraído
        arquivo_saida (str): Nome do arquivo de saída
    
    Returns:
        bool: True se salvou com sucesso
    """
    try:
        # Adicionar metadados sobre o arquivo de saída
        if "metadata" not in dados_com_html:
            dados_com_html["metadata"] = {}
        
        dados_com_html["metadata"]["arquivo_html"] = arquivo_saida
        dados_com_html["metadata"]["data_salvamento"] = datetime.now().isoformat()
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(dados_com_html, f, ensure_ascii=False, indent=2)
        
        print(f"\nDados com HTML salvos em: {arquivo_saida}")
        
        # Estatísticas
        total_sucessos = 0
        total_erros = 0
        tamanho_total = 0
        
        for termo, paginas in dados_com_html["dados"].items():
            for pagina in paginas:
                if pagina.get("status") == "sucesso":
                    total_sucessos += 1
                    tamanho_total += pagina.get("tamanho_html", 0)
                else:
                    total_erros += 1
        
        print(f"\nEstatísticas finais:")
        print(f"  Arquivo: {arquivo_saida}")
        print(f"  Sucessos: {total_sucessos}")
        print(f"  Erros: {total_erros}")
        print(f"  Tamanho total do HTML: {tamanho_total / 1024 / 1024:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False

def extrair_html_de_json(arquivo_json="dados_coletados.json", arquivo_saida="dados_com_html.json", delay=1):
    """
    Função principal para extrair HTML completo dos links do JSON
    
    Args:
        arquivo_json (str): Arquivo JSON de entrada
        arquivo_saida (str): Arquivo JSON de saída
        delay (int): Delay entre requisições
    
    Returns:
        bool: True se processou com sucesso
    """
    print("="*60)
    print("EXTRAÇÃO DE HTML COMPLETO DOS LINKS")
    print("="*60)
    
    # Carregar dados
    dados = carregar_dados_json(arquivo_json)
    if not dados:
        return False
    
    # Processar todos os links
    dados_com_html = processar_todos_links(dados, delay)
    if not dados_com_html:
        return False
    
    # Salvar resultados
    return salvar_html_completo(dados_com_html, arquivo_saida)

if __name__ == "__main__":
    print("⚠️ MÓDULO LEGACY - Para funcionalidades atualizadas, use:")
    print("   python -m core.web_search")
    print("   ou execute: python main.py")
    print()
    
    # Executar extração legacy
    print("🔄 Executando funcionalidade legacy...")
    sucesso = extrair_html_de_json()
    if sucesso:
        print("✅ Extração legacy concluída com sucesso!")
        print("💡 Considere migrar para o módulo web_search.py")
    else:
        print("❌ Falha na extração legacy!")


# ============================================================================
# MIGRAÇÃO RECOMENDADA
# ============================================================================
"""
Este módulo será removido em versões futuras. Migre para:

NOVO MÓDULO: core.web_search
- Extração otimizada de texto
- Melhor tratamento de erros  
- Suporte a type hints
- Documentação completa
- Testes automatizados

EXEMPLO DE MIGRAÇÃO:

# ANTES (Legacy):
from core.htmlcolect import baixar_html_completo
dados = baixar_html_completo(urls, "dados.json")

# DEPOIS (Recomendado):
from core.web_search import download_and_save_content
dados = download_and_save_content(urls, "dados.json")
"""
