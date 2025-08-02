"""
Módulo de Coleta de Conteúdo Web
================================

Este módulo gerencia a coleta e extração de conteúdo de páginas web,
incluindo busca de URLs, extração de texto e processamento de dados.

Funcionalidades:
- Busca inteligente de URLs baseada em termos
- Extração otimizada de conteúdo textual
- Limpeza e normalização de texto
- Salvamento estruturado em JSON
- Tratamento robusto de erros

Dependências:
- requests: Para requisições HTTP
- beautifulsoup4: Para parsing de HTML
- json: Para serialização de dados
- datetime: Para timestamps

Autor: Marco
Data: Agosto 2025
"""

import requests
from utils.console import (
    print_header, print_section, print_step, print_result, 
    log, RichProgress, RichStatus, console
)
from bs4 import BeautifulSoup
import urllib.parse
import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional


# Configurações globais
REQUEST_TIMEOUT = 15
MAX_CONTENT_LENGTH = 8000  # Aumentado para capturar mais conteúdo
DEFAULT_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
)

# Base de URLs educacionais para Python
PYTHON_RESOURCES = {
    "aprender python": [
        "https://docs.python.org/pt-br/3/tutorial/",
        "https://www.python.org/",
        "https://realpython.com/",
        "https://www.w3schools.com/python/",
        "https://pythonacademy.com.br/"
    ],
    "tutorial python": [
        "https://docs.python.org/pt-br/3/tutorial/",
        "https://www.codecademy.com/learn/learn-python-3",
        "https://www.learnpython.org/",
        "https://www.tutorialspoint.com/python/",
        "https://automatetheboringstuff.com/"
    ],
    "python para iniciantes": [
        "https://www.python.org/about/gettingstarted/",
        "https://realpython.com/python-beginner-tips/",
        "https://www.w3schools.com/python/python_intro.asp",
        "https://docs.python.org/pt-br/3/tutorial/introduction.html",
        "https://pythonspot.com/"
    ],
    "sintaxe python": [
        "https://docs.python.org/pt-br/3/reference/",
        "https://www.w3schools.com/python/python_syntax.asp",
        "https://realpython.com/python-syntax/",
        "https://docs.python.org/pt-br/3/tutorial/introduction.html",
        "https://www.programiz.com/python-programming/syntax"
    ],
    "exemplos de código python": [
        "https://github.com/python/cpython",
        "https://realpython.com/python-practice-problems/",
        "https://www.programiz.com/python-programming/examples",
        "https://docs.python.org/pt-br/3/tutorial/",
        "https://www.w3resource.com/python-exercises/"
    ]
}


def search_pages_for_term(search_term: str, max_pages: int = 5) -> List[str]:
    """
    Busca URLs relevantes para um termo específico.
    
    Args:
        search_term (str): Termo de busca
        max_pages (int, optional): Número máximo de páginas. Default: 5
    
    Returns:
        List[str]: Lista de URLs encontradas
        
    Note:
        Usa uma base de conhecimento pré-definida para garantir
        qualidade e relevância dos recursos educacionais.
    """
    # Normaliza o termo para busca case-insensitive
    normalized_term = search_term.lower().strip()
    
    # Busca correspondências na base de conhecimento
    found_urls = []
    
    for resource_key, urls in PYTHON_RESOURCES.items():
        # Verifica se alguma palavra do termo coincide com a chave
        if any(word in normalized_term for word in resource_key.split()):
            found_urls = urls[:max_pages]
            break
    
    # Fallback: URLs gerais se não encontrar correspondência específica
    if not found_urls:
        found_urls = [
            "https://docs.python.org/pt-br/3/",
            "https://www.python.org/",
            "https://realpython.com/",
            "https://www.w3schools.com/python/",
            "https://www.programiz.com/python-programming/"
        ][:max_pages]
    
    return found_urls


def collect_web_pages(search_terms: List[str], max_pages: int = 5) -> Dict[str, List[str]]:
    """
    Coleta páginas web para uma lista de termos de busca.
    
    Args:
        search_terms (List[str]): Lista de termos de busca
        max_pages (int, optional): Número máximo de páginas por termo. Default: 5
    
    Returns:
        Dict[str, List[str]]: Dicionário mapeando termos para suas URLs
        
    Examples:
        >>> terms = ["python básico", "python avançado"]
        >>> results = collect_web_pages(terms, max_pages=3)
        >>> print(results)
        {'python básico': ['url1', 'url2', 'url3'], ...}
    """
    search_results = {}
    
    for index, term in enumerate(search_terms, 1):
        print(f"\n🔍 Buscando páginas para termo {index}: {term}")
        
        # Busca URLs para o termo atual
        found_pages = search_pages_for_term(term, max_pages)
        search_results[term] = found_pages
        
        # Mostra resultados
        print(f"📋 Encontradas {len(found_pages)} páginas:")
        for page_num, url in enumerate(found_pages, 1):
            print(f"   {page_num}. {url}")
    
    return search_results


def extract_page_content(url: str) -> Dict[str, Any]:
    """
    Extrai o conteúdo textual de uma página web.
    
    Args:
        url (str): URL da página para extrair conteúdo
    
    Returns:
        Dict[str, Any]: Dicionário com dados extraídos da página
        
    Structure:
        - url: URL original
        - titulo: Título da página
        - descricao: Meta description
        - conteudo_texto: Texto limpo extraído
        - tamanho_texto: Tamanho do texto em caracteres
        - status: Status da extração
        - timestamp: Timestamp da extração
    """
    try:
        # Configuração da requisição
        headers = {'User-Agent': DEFAULT_USER_AGENT}
        
        # Requisição HTTP com timeout
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        # Parse do HTML
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Remove elementos desnecessários
        _remove_unwanted_elements(soup)
        
        # Extrai metadados
        title = _extract_title(soup)
        description = _extract_meta_description(soup)
        
        # Extrai conteúdo principal
        main_content = _extract_main_content(soup)
        
        # Limpa e normaliza o texto
        clean_text = _clean_text_content(main_content)
        
        return {
            "url": url,
            "titulo": title,
            "descricao": description,
            "conteudo_texto": clean_text[:MAX_CONTENT_LENGTH],
            "tamanho_texto": len(clean_text),
            "status": "sucesso",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as error:
        return {
            "url": url,
            "titulo": "",
            "descricao": "",
            "conteudo_texto": "",
            "tamanho_texto": 0,
            "status": f"erro: {str(error)}",
            "timestamp": datetime.now().isoformat()
        }


def _remove_unwanted_elements(soup: BeautifulSoup) -> None:
    """Remove elementos HTML desnecessários para extração de texto."""
    unwanted_tags = [
        "script", "style", "nav", "header", "footer", 
        "aside", "noscript", "iframe", "form", "button"
    ]
    
    for tag_name in unwanted_tags:
        for element in soup.find_all(tag_name):
            element.decompose()


def _extract_title(soup: BeautifulSoup) -> str:
    """Extrai o título da página."""
    title_element = soup.find("title")
    return title_element.get_text().strip() if title_element else "Sem título"


def _extract_meta_description(soup: BeautifulSoup) -> str:
    """Extrai a meta description da página."""
    meta_element = soup.find("meta", attrs={"name": "description"})
    return meta_element.get("content", "").strip() if meta_element else ""


def _extract_main_content(soup: BeautifulSoup) -> str:
    """Extrai o conteúdo principal da página usando seletores prioritários."""
    # Seletores ordenados por prioridade
    priority_selectors = [
        'main', 'article', '.content', '.main-content',
        '#content', '.post-content', '.entry-content'
    ]
    
    # Tenta encontrar conteúdo usando seletores prioritários
    for selector in priority_selectors:
        elements = soup.select(selector)
        if elements:
            return elements[0].get_text()
    
    # Fallback: usa body ou todo o documento
    body_element = soup.find("body")
    if body_element:
        return body_element.get_text()
    
    return soup.get_text()


def _clean_text_content(raw_text: str) -> str:
    """Limpa e normaliza o conteúdo textual."""
    # Remove quebras de linha excessivas e espaços
    lines = (line.strip() for line in raw_text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # Junta chunks não vazios com tamanho mínimo
    clean_text = ' '.join(chunk for chunk in chunks if chunk and len(chunk) > 3)
    
    # Normaliza espaços em branco
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    # Remove caracteres especiais mantendo pontuação básica
    clean_text = re.sub(
        r'[^\w\s\.,!?;:()\-\[\]"áàâãéèêíìîóòôõúùûç]', 
        ' ', 
        clean_text
    )
    
    # Normalização final
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return clean_text


def download_and_save_content(
    search_results: Dict[str, List[str]], 
    output_file: str = "dados_coletados.json"
) -> Dict[str, Any]:
    """
    Baixa conteúdo de todas as URLs e salva em arquivo JSON estruturado.
    
    Args:
        search_results (Dict[str, List[str]]): Resultados da busca por termo
        output_file (str, optional): Nome do arquivo de saída. Default: "dados_coletados.json"
    
    Returns:
        Dict[str, Any]: Dados completos coletados e organizados
        
    Structure:
        - metadata: Informações sobre a coleta
        - dados: Conteúdo organizado por termo de busca
    """
    # Estrutura inicial dos dados
    complete_data = {
        "metadata": {
            "data_coleta": datetime.now().isoformat(),
            "total_termos": len(search_results),
            "total_urls": sum(len(urls) for urls in search_results.values()),
            "arquivo": output_file,
            "versao": "2.0"
        },
        "dados": {}
    }
    
    print(f"\n📥 Iniciando download do conteúdo das páginas...")
    
    # Processa cada termo e suas URLs
    for term, urls in search_results.items():
        print(f"\n🔄 Processando termo: {term}")
        complete_data["dados"][term] = []
        
        for index, url in enumerate(urls, 1):
            print(f"   📖 Baixando {index}/{len(urls)}: {url[:80]}...")
            
            # Extrai conteúdo da página
            page_content = extract_page_content(url)
            complete_data["dados"][term].append(page_content)
    
    # Salva dados no arquivo JSON
    _save_json_data(complete_data, output_file)
    
    # Exibe estatísticas finais
    _display_collection_stats(complete_data)
    
    return complete_data


def _save_json_data(data: Dict[str, Any], filename: str) -> None:
    """Salva dados em arquivo JSON com tratamento de erros."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"\n✅ Dados salvos com sucesso em: {filename}")
        
    except Exception as error:
        print(f"❌ Erro ao salvar arquivo JSON: {error}")
        raise


def _display_collection_stats(data: Dict[str, Any]) -> None:
    """Exibe estatísticas da coleta de dados."""
    # Calcula estatísticas
    success_count = sum(
        len([page for page in pages if page["status"] == "sucesso"]) 
        for pages in data["dados"].values()
    )
    
    error_count = sum(
        len([page for page in pages if page["status"] != "sucesso"]) 
        for pages in data["dados"].values()
    )
    
    total_pages = success_count + error_count
    
    # Exibe relatório
    print(f"\n📊 Estatísticas da Coleta:")
    print(f"   📄 Total de páginas processadas: {total_pages}")
    print(f"   ✅ Sucessos: {success_count}")
    print(f"   ❌ Erros: {error_count}")
    
    if total_pages > 0:
        success_rate = (success_count / total_pages) * 100
        print(f"   📈 Taxa de sucesso: {success_rate:.1f}%")


# Aliases para compatibilidade com código existente
buscar_paginas = search_pages_for_term
coletar_todas_paginas = collect_web_pages
extrair_conteudo_pagina = extract_page_content
baixar_e_salvar_conteudo = download_and_save_content


if __name__ == "__main__":
    # Teste do módulo quando executado diretamente
    print("🧪 Testando módulo de coleta web...")
    
    test_terms = ["python básico", "tutorial python"]
    test_results = collect_web_pages(test_terms, max_pages=2)
    
    print(f"\n📋 Teste concluído com {len(test_results)} termos processados.")
