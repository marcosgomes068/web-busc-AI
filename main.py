"""
Sistema Inteligente de Coleta e Análise de Conteúdo Web
======================================================

Este módulo principal coordena todo o fluxo de coleta de dados da web,
extração de conteúdo e análise usando múltiplos agentes de IA.

Funcionalidades:
- Geração automática de termos de busca
- Coleta de conteúdo de páginas web
- Análise inteligente usando múltiplos agentes especializados
- Geração de relatórios e sínteses

Autor: Marco
Data: Agosto 2025
"""

import re
import os
from typing import Tuple, List, Dict, Any
from utils.console import (
    print_header, print_section, print_step, print_result, 
    log, RichProgress, confirm_action, prompt_input, console
)

from core.web_search import collect_web_pages, download_and_save_content
from core.proces_response import create_multi_agent_summary


def normalize_filename(topic: str) -> str:
    """
    Normaliza um tema para criar um nome de arquivo válido.
    
    Args:
        topic (str): Tema de busca original
        
    Returns:
        str: Nome de arquivo normalizado e seguro
        
    Examples:
        >>> normalize_filename("Python & Machine Learning")
        'python__machine_learning'
    """
    # Remove caracteres especiais não permitidos em nomes de arquivo
    clean_name = re.sub(r'[<>:"/\\|?*]', '', topic)
    
    # Substitui espaços por underscores
    clean_name = re.sub(r'\s+', '_', clean_name.strip())
    
    # Converte para minúsculas
    clean_name = clean_name.lower()
    
    # Limita o tamanho para evitar problemas no sistema de arquivos
    return clean_name[:50]


def process_search_query(search_query: str) -> Tuple[List[str], Dict[str, List[str]], Dict[str, Any]]:
    """
    Processa uma consulta de busca completa: geração de termos, coleta e análise.
    
    Args:
        search_query (str): Consulta de busca do usuário
        
    Returns:
        Tuple contendo:
        - List[str]: Termos de busca extraídos
        - Dict[str, List[str]]: URLs coletadas por termo
        - Dict[str, Any]: Dados completos salvos
    """
    print(f"🔍 Iniciando busca para: {search_query}")
    
    # Gera nome de arquivo baseado no tema
    file_base = normalize_filename(search_query)
    data_file = f"dados_{file_base}.json"
    
    log.info(f"Arquivo será salvo como: {data_file}")
    
    # Etapa 1: Gera termos de busca usando IA
    print_section("GERANDO TERMOS DE BUSCA COM IA")
    
    search_terms = _generate_search_terms(search_query)
    
    # Etapa 2: Coleta páginas da web
    print_section("COLETANDO PÁGINAS DA WEB")
    
    collected_urls = collect_web_pages(search_terms)
    
    # Etapa 3: Extrai conteúdo otimizado
    print_section("EXTRAINDO CONTEÚDO DE TEXTO")
    
    complete_data = download_and_save_content(collected_urls, data_file)
    
    # Etapa 4: Análise com múltiplos agentes
    print_section("PROCESSANDO COM MÚLTIPLOS AGENTES IA")
    
    create_multi_agent_summary(data_file)
    
    return search_terms, collected_urls, complete_data


def _generate_search_terms(search_query: str) -> List[str]:
    """
    Gera termos de busca usando IA baseado na consulta do usuário.
    
    Args:
        search_query (str): Consulta original do usuário
        
    Returns:
        List[str]: Lista de termos de busca gerados
    """
    from core.co import create_agent
    
    # Cria agente especializado em geração de termos de busca
    log.step("Criando gerador de termos com IA")
    term_generator = create_agent(
        "ESPECIALISTA EM ESTRATÉGIA DE BUSCA EDUCACIONAL\n"
        "════════════════════════════════════════════\n\n"
        "MISSÃO: Gerar termos de busca estratégicos para coleta de conteúdo educacional de alta qualidade.\n\n"
        "CRITÉRIOS OBRIGATÓRIOS:\n"
        "• Foque APENAS em recursos educacionais confiáveis\n"
        "• EVITE sites comerciais, marketplaces ou páginas pagas\n"
        "• Priorize documentação oficial, tutoriais e guias técnicos\n"
        "• Use termos que direcionem para conteúdo substantivo\n"
        "• Varie entre termos específicos e gerais\n\n"
        "FORMATO DE RESPOSTA OBRIGATÓRIO:\n"
        "1. [termo específico técnico]\n"
        "2. [termo de aprendizado/tutorial]\n"
        "3. [termo de documentação]\n"
        "4. [termo de exemplos práticos]\n"
        "5. [termo de conceitos fundamentais]\n\n"
        "EXEMPLOS DE TERMOS VÁLIDOS:\n"
        "• 'python tutorial básico'\n"
        "• 'documentação oficial python'\n"
        "• 'python conceitos fundamentais'\n"
        "• 'guia python iniciantes'\n\n"
        "USE APENAS português brasileiro e seja específico para o tema solicitado.",
        max_tokens=400
    )
    
    # Prompt específico para geração de termos
    search_prompt = f"""
TEMA SOLICITADO: {search_query}

GERE 5 termos de busca estratégicos que direcionem para:
✅ Documentação oficial e tutoriais educacionais
✅ Guias técnicos e conceitos fundamentais  
✅ Exemplos práticos e aplicações
✅ Recursos de aprendizado confiáveis

❌ EVITE termos que levem a:
❌ Sites comerciais ou de venda
❌ Marketplaces ou plataformas pagas
❌ Conteúdo promocional ou publicitário

Responda APENAS com a lista numerada dos termos.
"""
    
    log.step("Processando consulta com IA")
    response = term_generator(search_prompt)
    
    # Extrai termos numerados da resposta
    terms = re.findall(r'\d+\.\s*([^\n]+)', response)
    
    # Fallback se não conseguir extrair termos
    if not terms:
        # Extrai qualquer linha que pareça um termo
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        terms = [line for line in lines if len(line) > 5 and not line.startswith(('TEMA', 'GERE', '✅', '❌'))]
        terms = terms[:5]  # Limita a 5 termos
    
    # Se ainda não tiver termos, usa termos padrão baseados na consulta
    if not terms:
        terms = [
            f"{search_query} tutorial",
            f"{search_query} documentação",
            f"{search_query} guia iniciantes",
            f"{search_query} conceitos básicos",
            f"{search_query} exemplos práticos"
        ]
    
    log.success("Termos de busca gerados:")
    for i, term in enumerate(terms, 1):
        console.print(f"   [bold cyan]{i}.[/bold cyan] [white]{term}[/white]")
    
    return terms


def search(query: str) -> Tuple[List[str], Dict[str, List[str]], Dict[str, Any]]:
    """
    Função pública principal para realizar busca completa.
    
    Args:
        query (str): Consulta de busca
        
    Returns:
        Tuple com resultados da busca
    """
    return process_search_query(query)


def summarize_only(topic: str) -> None:
    """
    Cria apenas o resumo de dados já coletados usando múltiplos agentes.
    
    Args:
        topic (str): Tema dos dados já coletados
        
    Note:
        O arquivo de dados deve existir no formato: dados_{topic_normalizado}.json
    """
    file_base = normalize_filename(topic)
    data_file = f"dados_{file_base}.json"
    
    if not os.path.exists(data_file):
        log.error(f"Arquivo não encontrado: {data_file}")
        log.info("Execute primeiro uma busca completa para gerar os dados.")
        return
    
    log.info(f"Criando resumo para dados existentes: {topic}")
    create_multi_agent_summary(data_file)


def get_user_choice() -> str:
    """
    Solicita ao usuário que escolha o tema de pesquisa.
    
    Returns:
        str: Tema escolhido pelo usuário
    """
    print_header(
        "SISTEMA INTELIGENTE DE ANÁLISE WEB", 
        "Análise automatizada com múltiplos agentes de IA"
    )
    
    # Opções sugeridas
    suggested_topics = [
        "Python programação",
        "Machine Learning",
        "Desenvolvimento Web",
        "Inteligência Artificial",
        "Data Science",
        "DevOps e Cloud",
        "Cybersecurity",
        "Blockchain"
    ]
    
    print_section("ESCOLHA SEU TEMA DE PESQUISA")
    
    # Exibe opções sugeridas
    log.info("Temas sugeridos:")
    for i, topic in enumerate(suggested_topics, 1):
        console.print(f"   [bold cyan]{i}.[/bold cyan] [white]{topic}[/white]")
    
    console.print()
    
    # Solicita entrada do usuário
    user_input = prompt_input(
        "Digite o número do tema sugerido ou escreva seu próprio tema",
        default="1"
    ).strip()
    
    # Processa a escolha
    if user_input.isdigit():
        choice_num = int(user_input)
        if 1 <= choice_num <= len(suggested_topics):
            chosen_topic = suggested_topics[choice_num - 1]
            log.success(f"Tema selecionado: {chosen_topic}")
            return chosen_topic
    
    # Se não for um número válido, usa como tema customizado
    if user_input and user_input != "1":
        log.success(f"Tema customizado: {user_input}")
        return user_input
    
    # Default
    default_topic = suggested_topics[0]
    log.info(f"Usando tema padrão: {default_topic}")
    return default_topic


def show_menu() -> str:
    """
    Exibe menu de opções para o usuário.
    
    Returns:
        str: Opção escolhida pelo usuário
    """
    print_section("MENU DE OPÇÕES")
    
    menu_options = [
        "🔍 Nova pesquisa completa",
        "📄 Gerar resumo de dados existentes",
        "🧪 Executar testes do sistema",
        "❓ Ajuda sobre o sistema",
        "🚪 Sair"
    ]
    
    for i, option in enumerate(menu_options, 1):
        console.print(f"   [bold cyan]{i}.[/bold cyan] [white]{option}[/white]")
    
    console.print()
    
    choice = prompt_input("Escolha uma opção", default="1").strip()
    
    return choice


def handle_existing_data_summary():
    """Lida com a geração de resumo de dados existentes."""
    print_section("RESUMO DE DADOS EXISTENTES")
    
    # Lista arquivos de dados disponíveis
    data_files = [f for f in os.listdir('.') if f.startswith('dados_') and f.endswith('.json')]
    
    if not data_files:
        log.warning("Nenhum arquivo de dados encontrado.")
        log.info("Execute primeiro uma pesquisa completa para gerar dados.")
        return
    
    log.info("Arquivos de dados disponíveis:")
    for i, file in enumerate(data_files, 1):
        # Extrai o tema do nome do arquivo
        topic = file.replace('dados_', '').replace('.json', '').replace('_', ' ').title()
        console.print(f"   [bold cyan]{i}.[/bold cyan] [white]{topic}[/white] [dim]({file})[/dim]")
    
    console.print()
    
    choice = prompt_input("Escolha o arquivo para gerar resumo", default="1").strip()
    
    if choice.isdigit():
        choice_num = int(choice)
        if 1 <= choice_num <= len(data_files):
            selected_file = data_files[choice_num - 1]
            topic = selected_file.replace('dados_', '').replace('.json', '').replace('_', ' ')
            
            log.info(f"Gerando resumo para: {topic}")
            create_multi_agent_summary(selected_file)
            return
    
    log.error("Escolha inválida.")


def show_help():
    """Exibe ajuda sobre o sistema."""
    print_section("AJUDA DO SISTEMA")
    
    help_content = """
🎯 SOBRE O SISTEMA:
Este é um sistema inteligente de análise web que usa múltiplos agentes de IA
para coletar, processar e analisar informações sobre qualquer tema.

📋 FUNCIONALIDADES:
• Geração automática de termos de busca otimizados
• Coleta inteligente de conteúdo web educacional
• Análise com 4 agentes especializados:
  - Resumidor: Extrai pontos principais
  - Analista: Identifica insights e tendências
  - Organizador: Estrutura informações
  - Sintetizador: Cria síntese executiva final

📁 ARQUIVOS GERADOS:
• dados_[tema].json: Dados coletados da web
• resumos_parciais_[tema].txt: Análises por termo
• sintese_final_[tema].txt: Síntese executiva completa

⚙️  CONFIGURAÇÃO NECESSÁRIA:
• Python 3.8+ com dependências instaladas
• Chave da API Cohere no arquivo .env
• Conexão com internet para coleta web

🔧 SOLUÇÃO DE PROBLEMAS:
• Se houver erro de API: Verifique COHERE_API_KEY no .env
• Se falhar coleta web: Verifique conexão internet
• Para mais detalhes: Consulte os logs durante execução
"""
    
    console.print(help_content)
    
    input("\nPressione Enter para continuar...")


def main():
    """
    Função principal do programa com interface interativa.
    """
    try:
        while True:
            choice = show_menu()
            
            if choice == "1":
                # Nova pesquisa completa
                search_query = get_user_choice()
                
                # Confirma antes de prosseguir
                if confirm_action(f"Iniciar pesquisa completa sobre '{search_query}'?"):
                    log.info(f"Iniciando análise completa para: {search_query}")
                    
                    # Executa busca completa
                    terms, pages, data = search(search_query)
                    
                    log.success("Processamento concluído com sucesso!")
                    console.print("\n[bold green]📊 Estatísticas finais:[/bold green]")
                    console.print(f"   [cyan]•[/cyan] Termos processados: [bold]{len(terms)}[/bold]")
                    console.print(f"   [cyan]•[/cyan] URLs coletadas: [bold]{sum(len(urls) for urls in pages.values())}[/bold]")
                    console.print(f"   [cyan]•[/cyan] Análise com múltiplos agentes: [bold green]Concluída[/bold green]")
                    
                    # Pergunta se quer continuar
                    if not confirm_action("Deseja fazer outra operação?"):
                        break
                else:
                    log.info("Operação cancelada pelo usuário.")
            
            elif choice == "2":
                # Gerar resumo de dados existentes
                handle_existing_data_summary()
                
                if not confirm_action("Deseja fazer outra operação?"):
                    break
            
            elif choice == "3":
                # Executar testes
                log.info("Executando testes do sistema...")
                try:
                    import subprocess
                    subprocess.run(["python", "test_optimization.py"], check=True)
                except Exception as e:
                    log.error(f"Erro ao executar testes: {e}")
                
                if not confirm_action("Deseja fazer outra operação?"):
                    break
            
            elif choice == "4":
                # Ajuda
                show_help()
            
            elif choice == "5":
                # Sair
                log.info("Encerrando sistema. Até logo!")
                break
            
            else:
                log.warning("Opção inválida. Tente novamente.")
                
    except KeyboardInterrupt:
        log.info("\nSistema interrompido pelo usuário. Até logo!")
    except Exception as e:
        log.error(f"Erro durante execução: {e}")
        log.info("Verifique a configuração da API Cohere no arquivo .env")


if __name__ == "__main__":
    # Para usar apenas resumo de dados existentes, descomente:
    # summarize_only("Python programação")
    
    # Execução padrão
    main()


