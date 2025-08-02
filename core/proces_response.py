"""
Módulo de Processamento Multi-Agente
====================================

Este módulo gerencia o processamento de conteúdo coletado usando
múltiplos agentes especializados de IA para análise aprofundada.

Funcionalidades:
- Sistema multi-agente com 4 especialistas
- Processamento sequencial e estruturado
- Geração de resumos parciais e síntese final
- Relatórios detalhados e estatísticas
- Tratamento robusto de dados JSON

Agentes Especializados:
- Resumidor: Extrai pontos principais
- Analista: Identifica insights e tendências
- Organizador: Estrutura informações logicamente
- Sintetizador: Cria síntese final unificada

Autor: Marco
Data: Agosto 2025
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
from utils.console import (
    print_header, print_section, print_step, print_result, 
    log, RichProgress, RichStatus, console
)
from core.co import create_agent


# Configurações do processamento
MAX_CONTENT_LENGTH = 3000  # Aumentado para processar mais conteúdo
MAX_SYNTHESIS_LENGTH = 12000  # Aumentado para síntese mais completa
ENCODING = 'utf-8'


def process_with_multiple_agents(json_file: str) -> None:
    """
    Processa conteúdo JSON usando sistema multi-agente especializado.
    
    Args:
        json_file (str): Caminho para arquivo JSON com dados coletados
        
    Raises:
        FileNotFoundError: Se o arquivo JSON não for encontrado
        json.JSONDecodeError: Se o arquivo JSON estiver malformado
        
    Note:
        Gera dois arquivos de saída:
        - resumos_parciais_*.txt: Análises individuais por termo
        - sintese_final_*.txt: Síntese unificada de todos os agentes
    """
    print_header("SISTEMA MULTI-AGENTE DE ANÁLISE", "Processamento inteligente com 4 agentes especializados")
    
    # Carrega e valida dados
    data = _load_json_data(json_file)
    if not data:
        return
    
    # Cria agentes especializados
    agents = _create_specialized_agents()
    
    # Processa dados e gera resumos
    partial_summaries = _process_terms_with_agents(data, agents, json_file)
    
    # Cria síntese final
    _create_final_synthesis(partial_summaries, agents['sintetizador'], json_file)
    
    # Exibe estatísticas finais
    _display_processing_stats(len(partial_summaries), json_file)


def _load_json_data(json_file: str) -> Dict[str, Any]:
    """
    Carrega e valida dados do arquivo JSON.
    
    Args:
        json_file (str): Caminho para o arquivo JSON
        
    Returns:
        Dict[str, Any]: Dados carregados ou dicionário vazio em caso de erro
    """
    try:
        with open(json_file, 'r', encoding=ENCODING) as file:
            data = json.load(file)
        
        log.success(f"Dados carregados com sucesso: {json_file}")
        
        # Valida estrutura básica
        if 'dados' not in data:
            log.warning("Estrutura JSON inválida: campo 'dados' não encontrado")
            return {}
            
        return data
        
    except FileNotFoundError:
        log.error(f"Arquivo não encontrado: {json_file}")
        return {}
        
    except json.JSONDecodeError as e:
        log.error(f"Erro ao decodificar JSON: {e}")
        return {}
        
    except Exception as e:
        log.error(f"Erro inesperado ao carregar arquivo: {e}")
        return {}


def _create_specialized_agents() -> Dict[str, Any]:
    """
    Cria o conjunto de agentes especializados para análise.
    
    Returns:
        Dict[str, Any]: Dicionário com agentes especializados
    """
    print_section("CRIANDO AGENTES ESPECIALIZADOS")
    
    with RichStatus("Configurando agentes especializados..."):
        agents = {
            'resumidor': create_agent(
            "ESPECIALISTA EM RESUMOS TÉCNICOS\n"
            "═══════════════════════════════\n\n"
            "MISSÃO: Extrair e consolidar os pontos mais importantes do conteúdo fornecido.\n\n"
            "INSTRUÇÕES ESPECÍFICAS:\n"
            "• Identifique os 5-7 conceitos mais importantes\n"
            "• Use linguagem técnica mas acessível\n"
            "• Mantenha a ordem lógica do conteúdo original\n"
            "• Foque em informações práticas e aplicáveis\n"
            "• Elimine detalhes redundantes ou secundários\n\n"
            "FORMATO DE SAÍDA:\n"
            "📋 RESUMO TÉCNICO:\n"
            "• [Ponto principal 1 - detalhamento conciso]\n"
            "• [Ponto principal 2 - detalhamento conciso]\n"
            "• [Ponto principal 3 - detalhamento conciso]\n"
            "...\n\n"
            "Use SEMPRE português brasileiro e seja objetivo.",
            max_tokens=600
        ),
        
        'analista': create_agent(
            "ANALISTA SÊNIOR DE CONTEÚDO TÉCNICO\n"
            "══════════════════════════════════\n\n"
            "EXPERTISE: Análise profunda, identificação de patterns e extração de insights.\n\n"
            "RESPONSABILIDADES:\n"
            "• Identificar tendências e padrões emergentes\n"
            "• Extrair insights técnicos e estratégicos\n"
            "• Avaliar qualidade e confiabilidade das informações\n"
            "• Conectar conceitos e estabelecer relações\n"
            "• Destacar implicações práticas e aplicações\n\n"
            "ESTRUTURA OBRIGATÓRIA:\n"
            "🔍 ANÁLISE TÉCNICA:\n\n"
            "💡 INSIGHTS PRINCIPAIS:\n"
            "• [Insight 1 com justificativa]\n"
            "• [Insight 2 com justificativa]\n\n"
            "📈 TENDÊNCIAS IDENTIFICADAS:\n"
            "• [Tendência 1 e implicações]\n"
            "• [Tendência 2 e implicações]\n\n"
            "⚡ IMPLICAÇÕES PRÁTICAS:\n"
            "• [Aplicação prática 1]\n"
            "• [Aplicação prática 2]\n\n"
            "Use terminologia técnica apropriada em português brasileiro.",
            max_tokens=800
        ),
        
        'organizador': create_agent(
            "ESPECIALISTA EM ARQUITETURA DE INFORMAÇÃO\n"
            "═══════════════════════════════════════\n\n"
            "OBJETIVO: Estruturar informações de forma hierárquica, lógica e visualmente clara.\n\n"
            "METODOLOGIA:\n"
            "• Criar taxonomia clara dos tópicos\n"
            "• Estabelecer hierarquia de importância\n"
            "• Agrupar conceitos relacionados\n"
            "• Usar formatação visual consistente\n"
            "• Facilitar navegação e compreensão\n\n"
            "TEMPLATE OBRIGATÓRIO:\n"
            "📊 ESTRUTURA ORGANIZACIONAL:\n\n"
            "# 🎯 TÓPICO PRINCIPAL\n"
            "## 📝 Seção 1: [Nome da Seção]\n"
            "### 🔸 Subseção 1.1\n"
            "   • Ponto importante A\n"
            "   • Ponto importante B\n"
            "### 🔸 Subseção 1.2\n"
            "   • Ponto importante C\n\n"
            "## 📝 Seção 2: [Nome da Seção]\n"
            "### 🔸 Subseção 2.1\n"
            "   • Ponto importante D\n\n"
            "SEMPRE use emojis, numeração e hierarquia visual clara.",
            max_tokens=700
        ),
        
        'sintetizador': create_agent(
            "SINTETIZADOR MASTER - SÍNTESE EXECUTIVA COMPLETA\n"
            "═══════════════════════════════════════════════\n\n"
            "RESPONSABILIDADE CRÍTICA: Criar síntese executiva ABRANGENTE e DETALHADA consolidando todas as análises.\n\n"
            "PROCESSO AVANÇADO DE SÍNTESE:\n"
            "• CONSOLIDAR completamente resumos, análises e estruturas organizacionais\n"
            "• ELIMINAR redundâncias mantendo informações essenciais\n"
            "• EXPANDIR insights com contexto adicional e implicações\n"
            "• DETALHAR conclusões e recomendações estratégicas\n"
            "• PRODUZIR documento executivo extenso e comprehensivo\n"
            "• MANTER rigor acadêmico com linguagem profissional\n\n"
            "TEMPLATE EXECUTIVO EXPANDIDO OBRIGATÓRIO:\n\n"
            "# 🎯 SÍNTESE EXECUTIVA COMPLETA\n\n"
            "## 📋 RESUMO GERAL CONSOLIDADO\n"
            "[Visão geral detalhada e consolidada do tema com contexto amplo]\n\n"
            "## 🔍 DESCOBERTAS PRINCIPAIS DETALHADAS\n"
            "### 💎 Descoberta Crítica 1\n"
            "• **Descrição:** [Detalhamento completo]\n"
            "• **Impacto:** [Análise de impacto específica]\n"
            "• **Evidências:** [Dados que suportam a descoberta]\n"
            "• **Implicações:** [Consequências práticas]\n\n"
            "### 💎 Descoberta Crítica 2\n"
            "• **Descrição:** [Detalhamento completo]\n"
            "• **Impacto:** [Análise de impacto específica]\n"
            "• **Evidências:** [Dados que suportam a descoberta]\n"
            "• **Implicações:** [Consequências práticas]\n\n"
            "### 💎 Descoberta Crítica 3\n"
            "• **Descrição:** [Detalhamento completo]\n"
            "• **Impacto:** [Análise de impacto específica]\n"
            "• **Evidências:** [Dados que suportam a descoberta]\n"
            "• **Implicações:** [Consequências práticas]\n\n"
            "## 📊 ANÁLISE DE TENDÊNCIAS E PADRÕES\n"
            "### 📈 Tendências Emergentes\n"
            "• [Tendência 1 com análise detalhada]\n"
            "• [Tendência 2 com análise detalhada]\n"
            "• [Tendência 3 com análise detalhada]\n\n"
            "### 🔄 Padrões Identificados\n"
            "• [Padrão 1 e suas manifestações]\n"
            "• [Padrão 2 e suas manifestações]\n\n"
            "## 🧠 INSIGHTS ESTRATÉGICOS APROFUNDADOS\n"
            "### 💡 Insight Estratégico 1\n"
            "• **Natureza:** [Caracterização do insight]\n"
            "• **Fundamentação:** [Base teórica ou empírica]\n"
            "• **Aplicabilidade:** [Contextos de aplicação]\n"
            "• **Valor Agregado:** [Benefícios específicos]\n\n"
            "### 💡 Insight Estratégico 2\n"
            "• **Natureza:** [Caracterização do insight]\n"
            "• **Fundamentação:** [Base teórica ou empírica]\n"
            "• **Aplicabilidade:** [Contextos de aplicação]\n"
            "• **Valor Agregado:** [Benefícios específicos]\n\n"
            "## 🎯 RECOMENDAÇÕES ESPECÍFICAS E ACIONÁVEIS\n"
            "### ⚡ Ações Imediatas (0-30 dias)\n"
            "• [Recomendação 1 com passos específicos]\n"
            "• [Recomendação 2 com passos específicos]\n\n"
            "### 📅 Ações de Médio Prazo (1-6 meses)\n"
            "• [Recomendação estratégica 1]\n"
            "• [Recomendação estratégica 2]\n\n"
            "### � Ações de Longo Prazo (6+ meses)\n"
            "• [Recomendação visionária 1]\n"
            "• [Recomendação visionária 2]\n\n"
            "## �🔗 CONEXÕES E INTERRELAÇÕES\n"
            "### 🌐 Mapa de Conexões\n"
            "[Análise detalhada de como os diferentes aspectos se relacionam e influenciam mutuamente]\n\n"
            "### 🔄 Sistemas e Processos\n"
            "[Identificação de sistemas complexos e processos interconectados]\n\n"
            "## ⚡ CONCLUSÕES FINAIS E DIREÇÕES FUTURAS\n"
            "### 🎯 Conclusões Definitivas\n"
            "[Conclusões consolidadas com base em toda a análise]\n\n"
            "### 🚀 Direções Estratégicas\n"
            "[Orientações para desenvolvimentos futuros]\n\n"
            "### 📝 Considerações Finais\n"
            "[Reflexões finais e contextualizações adicionais]\n\n"
            "EXIGÊNCIAS DE QUALIDADE PREMIUM:\n"
            "• Linguagem executiva sofisticada e profissional\n"
            "• Português brasileiro formal com precisão técnica\n"
            "• Máxima clareza, coerência e profundidade\n"
            "• Foco em valor agregado máximo e aplicabilidade prática\n"
            "• Estrutura visual rica e hierarquizada\n"
            "• Densidade informacional alta com organização exemplar",
            max_tokens=2000  # Aumentado significativamente para sínteses completas
        )
    }
    
    log.success(f"{len(agents)} agentes especializados criados com prompts otimizados")
    return agents


def _process_terms_with_agents(
    data: Dict[str, Any], 
    agents: Dict[str, Any], 
    json_file: str
) -> List[str]:
    """
    Processa cada termo usando a sequência de agentes especializados.
    
    Args:
        data (Dict[str, Any]): Dados carregados do JSON
        agents (Dict[str, Any]): Agentes especializados
        json_file (str): Nome do arquivo original para nomenclatura
        
    Returns:
        List[str]: Lista de resumos parciais gerados
    """
    # Configuração de arquivos de saída
    partial_file = _generate_output_filename(json_file, 'resumos_parciais_', '.txt')
    partial_summaries = []
    
    print_section("PROCESSAMENTO MULTI-AGENTE POR TERMO")
    
    total_terms = len(data.get('dados', {}))
    
    with open(partial_file, 'w', encoding=ENCODING) as file:
        # Cabeçalho do arquivo
        _write_file_header(file, "RESUMOS PARCIAIS - PIPELINE MULTI-AGENTE")
        
        term_counter = 0
        
        # Usa RichProgress para mostrar progresso
        with RichProgress(f"Processando {total_terms} termos") as progress:
            for term, pages in data.get('dados', {}).items():
                term_counter += 1
                progress.update(
                    (term_counter / total_terms) * 100,
                    f"Termo {term_counter}/{total_terms}: {term}"
                )
                
                # Extrai e prepara conteúdo do termo
                term_content = _extract_term_content(pages)
                
                if not term_content:
                    log.warning(f"Nenhum conteúdo válido encontrado para '{term}'")
                    continue
                
                # Aplica pipeline de agentes
                term_result = _apply_agent_pipeline(term, term_content, agents)
                
                # Salva resultado parcial
                _write_term_result(file, term, term_result)
                
                # Adiciona à lista para síntese final
                partial_summaries.append(_format_partial_summary(term, term_result))
                
                log.success(f"Termo '{term}' processado com sucesso")
    
    log.info(f"Resumos parciais salvos em: {partial_file}")
    return partial_summaries


def _extract_term_content(pages: List[Dict[str, Any]]) -> str:
    """
    Extrai e combina conteúdo válido de todas as páginas de um termo.
    
    Args:
        pages (List[Dict[str, Any]]): Lista de páginas do termo
        
    Returns:
        str: Conteúdo combinado e limitado
    """
    valid_content = []
    
    for page in pages:
        if page.get('status') == 'sucesso':
            # Tenta múltiplos campos de conteúdo
            text = (
                page.get('conteudo_texto') or 
                page.get('conteudo', '') or 
                page.get('texto', '')
            )
            
            # Filtra conteúdo muito pequeno
            if len(text) > 100:
                # Limita tamanho para evitar sobrecarga
                limited_text = text[:MAX_CONTENT_LENGTH] if len(text) > MAX_CONTENT_LENGTH else text
                valid_content.append(limited_text)
    
    return "\n\n".join(valid_content)


def _apply_agent_pipeline(
    term: str, 
    content: str, 
    agents: Dict[str, Any]
) -> Dict[str, str]:
    """
    Aplica sequência de agentes especializados em um termo.
    
    Args:
        term (str): Nome do termo sendo processado
        content (str): Conteúdo combinado do termo
        agents (Dict[str, Any]): Agentes especializados
        
    Returns:
        Dict[str, str]: Resultados de cada agente
    """
    print(f"      🔄 Executando pipeline multi-agente otimizado...")
    
    # Preparar contexto rico para os agentes
    content_stats = {
        'tamanho': len(content),
        'palavras': len(content.split()),
        'linhas': len(content.splitlines())
    }
    
    context_header = f"""
CONTEXTO DO PROCESSAMENTO:
═══════════════════════════
🏷️  TERMO: {term}
📊 ESTATÍSTICAS: {content_stats['palavras']} palavras, {content_stats['linhas']} linhas
🎯 OBJETIVO: Análise técnica completa e estruturada

"""
    
    # Agente 1: Resumidor
    print(f"      🤖 Agente Resumidor processando...")
    summary_prompt = f"{context_header}TAREFA: Resuma os pontos técnicos mais importantes do conteúdo abaixo.\n\nCONTEÚDO:\n{content}"
    summary = agents['resumidor'](summary_prompt)
    
    # Agente 2: Analista (com contexto do resumo)
    print(f"      🤖 Agente Analista processando...")
    analysis_prompt = f"""{context_header}TAREFA: Analise profundamente o conteúdo, identificando insights e padrões.

RESUMO INICIAL DISPONÍVEL:
{summary}

CONTEÚDO COMPLETO PARA ANÁLISE:
{content}

Foque em insights não cobertos no resumo e conexões importantes."""
    
    analysis = agents['analista'](analysis_prompt)
    
    # Agente 3: Organizador (com contexto acumulado)
    print(f"      🤖 Agente Organizador processando...")
    organization_prompt = f"""{context_header}TAREFA: Organize hierarquicamente todas as informações disponíveis.

RESUMO TÉCNICO:
{summary}

ANÁLISE DETALHADA:
{analysis}

CONTEÚDO ORIGINAL:
{content[:1500]}...

Crie uma estrutura visual clara que integre resumo, análise e conteúdo original."""
    
    organization = agents['organizador'](organization_prompt)
    
    return {
        'resumo': summary,
        'analise': analysis,
        'organizacao': organization
    }


def _create_final_synthesis(
    partial_summaries: List[str], 
    synthesizer: Any, 
    json_file: str
) -> None:
    """
    Cria síntese final usando o agente sintetizador.
    
    Args:
        partial_summaries (List[str]): Resumos parciais de todos os termos
        synthesizer (Any): Agente sintetizador
        json_file (str): Nome do arquivo original
    """
    print("🎯 Criando Síntese Final Executiva...")
    
    if not partial_summaries:
        print("❌ Nenhum resumo parcial disponível para síntese")
        return
    
    # Combina todos os resumos parciais
    combined_content = "\n\n" + "="*60 + "\n\n".join(partial_summaries)
    
    # Limita conteúdo para evitar sobrecarga do agente
    if len(combined_content) > MAX_SYNTHESIS_LENGTH:
        # Trunca inteligentemente mantendo resumos completos
        truncated_summaries = []
        current_length = 0
        
        for summary in partial_summaries:
            if current_length + len(summary) <= MAX_SYNTHESIS_LENGTH:
                truncated_summaries.append(summary)
                current_length += len(summary)
            else:
                # Adiciona resumo parcial do último item
                remaining_space = MAX_SYNTHESIS_LENGTH - current_length - 100
                if remaining_space > 200:
                    truncated_summaries.append(summary[:remaining_space] + "\n\n[RESUMO TRUNCADO]")
                break
        
        combined_content = "\n\n" + "="*60 + "\n\n".join(truncated_summaries)
        print(f"   ⚠️ Conteúdo otimizado: {len(truncated_summaries)} de {len(partial_summaries)} resumos incluídos")
    
    # Estatísticas para contexto
    stats = {
        'total_termos': len(partial_summaries),
        'total_caracteres': len(combined_content),
        'arquivo_origem': json_file
    }
    
    # Prompt otimizado para síntese executiva
    synthesis_prompt = f"""
BRIEFING EXECUTIVO PARA SÍNTESE FINAL
═══════════════════════════════════

📊 ESTATÍSTICAS DO PROJETO:
• Total de termos analisados: {stats['total_termos']}
• Volume de conteúdo processado: {stats['total_caracteres']:,} caracteres
• Fonte de dados: {stats['arquivo_origem']}

🎯 MISSÃO CRÍTICA:
Você recebeu análises especializadas de múltiplos agentes sobre diferentes aspectos de um tema.
Sua tarefa é criar uma SÍNTESE EXECUTIVA DEFINITIVA que integre todos os insights de forma coerente.

📋 ANÁLISES DOS AGENTES ESPECIALIZADOS:
{combined_content}

🎯 INSTRUÇÕES PARA SÍNTESE FINAL:
• Integre TODOS os insights dos agentes especializados
• Elimine redundâncias mantendo informações únicas
• Crie narrativa coerente e fluida
• Destaque descobertas mais importantes
• Formule recomendações práticas e aplicáveis
• Use formatação executiva profissional
• Mantenha tom técnico mas acessível

ENTREGUE uma síntese que demonstre o valor agregado de todo o processo de análise multi-agente.
"""
    
    # Gera síntese final
    final_synthesis = synthesizer(synthesis_prompt)
    
    # Salva síntese final
    final_file = _generate_output_filename(json_file, 'sintese_final_', '.txt')
    
    with open(final_file, 'w', encoding=ENCODING) as file:
        _write_file_header(file, "SÍNTESE FINAL - SISTEMA MULTI-AGENTE OTIMIZADO")
        file.write(final_synthesis)
        file.write("\n\n" + "="*80 + "\n")
        file.write(f"📊 METADATA DO PROCESSAMENTO AVANÇADO\n")
        file.write(f"   • Termos processados: {stats['total_termos']}\n")
        file.write(f"   • Agentes utilizados: 4 (Resumidor, Analista, Organizador, Sintetizador)\n")
        file.write(f"   • Volume processado: {stats['total_caracteres']:,} caracteres\n")
        file.write(f"   • Arquivo fonte: {stats['arquivo_origem']}\n")
        file.write(f"   • Tokens otimizados: Sistema adaptativo\n")
        file.write(f"   • Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        file.write(f"   • Versão do sistema: 2.0 (Clean Code + IA Otimizada)\n")
    
    print(f"🎉 Síntese final otimizada salva em: {final_file}")
    
    # Exibe prévia da síntese no terminal
    print("\n" + "="*80)
    print("🎯 PRÉVIA DA SÍNTESE FINAL OTIMIZADA")
    print("="*80)
    # Mostra mais conteúdo na prévia
    preview_length = 800
    print(final_synthesis[:preview_length] + "..." if len(final_synthesis) > preview_length else final_synthesis)
    print("="*80)


def _generate_output_filename(original_file: str, prefix: str, extension: str) -> str:
    """Gera nome de arquivo de saída baseado no arquivo original."""
    return original_file.replace('dados_', prefix).replace('.json', extension)


def _write_file_header(file, title: str) -> None:
    """Escreve cabeçalho padrão nos arquivos de saída."""
    file.write(f"{title}\n")
    file.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    file.write("="*80 + "\n\n")


def _write_term_result(file, term: str, result: Dict[str, str]) -> None:
    """Escreve resultado de um termo no arquivo de resumos parciais."""
    formatted_result = f"""
TERMO: {term}
{"="*50}

📋 RESUMO:
{result['resumo']}

🔍 ANÁLISE:
{result['analise']}

📊 ORGANIZAÇÃO:
{result['organizacao']}

{"="*80}

"""
    file.write(formatted_result)
    file.flush()  # Força escrita imediata


def _format_partial_summary(term: str, result: Dict[str, str]) -> str:
    """Formata resumo parcial para síntese final."""
    return (
        f"TERMO: {term}\n"
        f"RESUMO: {result['resumo']}\n"
        f"ANÁLISE: {result['analise']}\n"
        f"ORGANIZAÇÃO: {result['organizacao']}"
    )


def _display_processing_stats(terms_processed: int, json_file: str) -> None:
    """Exibe estatísticas finais do processamento."""
    print(f"\n✅ Processamento Multi-Agente Concluído!")
    print(f"📊 Estatísticas Finais:")
    print(f"   📝 Termos processados: {terms_processed}")
    print(f"   🤖 Agentes utilizados: 4 (Pipeline especializado)")
    print(f"   📄 Arquivos gerados: 2 (resumos parciais + síntese final)")
    print(f"   📂 Arquivo fonte: {json_file}")
    print(f"   ⏱️ Processamento concluído: {datetime.now().strftime('%H:%M:%S')}")


def create_multi_agent_summary(json_file: str) -> None:
    """
    Função principal para processar arquivo JSON com sistema multi-agente.
    
    Args:
        json_file (str): Caminho para arquivo JSON com dados coletados
        
    Note:
        Esta é a interface pública do módulo.
        Alias para compatibilidade com código existente.
    """
    process_with_multiple_agents(json_file)


# Aliases para compatibilidade com código existente
processar_com_multiplos_agentes = process_with_multiple_agents
criar_resumo_com_agentes = create_multi_agent_summary


if __name__ == "__main__":
    # Teste do módulo quando executado diretamente
    print("🧪 Testando Sistema Multi-Agente...")
    
    # Arquivo de teste (deve existir)
    test_file = "dados_python_programação.json"
    
    if os.path.exists(test_file):
        create_multi_agent_summary(test_file)
    else:
        print(f"❌ Arquivo de teste não encontrado: {test_file}")
        print("💡 Execute primeiro uma coleta de dados para gerar o arquivo JSON.")
