"""
Teste das Otimizações do Sistema
================================

Script para testar as melhorias de performance e qualidade dos prompts.

Autor: Marco
Data: Agosto 2025
"""

import time
import json
from core.co import create_agent, test_api_connection
from core.config import SystemConfig
from utils.console import (
    print_header, print_section, print_step, print_result, 
    log, RichProgress, RichTable, console
)


def test_optimized_prompts():
    """Testa os prompts otimizados com diferentes tamanhos de conteúdo."""
    print_section("TESTANDO PROMPTS OTIMIZADOS")
    
    # Verifica conexão
    if not test_api_connection():
        log.error("Falha na conexão com API. Configure COHERE_API_KEY")
        return
    
    # Conteúdo de teste
    test_contents = {
        'pequeno': "Python é uma linguagem de programação versátil e fácil de aprender.",
        'medio': """
Python é uma linguagem de programação de alto nível, interpretada e de propósito geral.
Foi criada por Guido van Rossum e lançada pela primeira vez em 1991.
Python enfatiza a legibilidade do código e sua sintaxe permite que os programadores
expressem conceitos em menos linhas de código do que seria possível em linguagens
como C++ ou Java. A linguagem fornece construções que permitem programação clara
em pequena e grande escala.
        """,
        'grande': """
Python é uma linguagem de programação de alto nível, interpretada, de script, 
imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte.
Foi lançada por Guido van Rossum em 1991. Atualmente possui um modelo de 
desenvolvimento comunitário, aberto e gerenciado pela organização sem fins 
lucrativos Python Software Foundation. Apesar de várias partes da linguagem 
possuírem padrões e especificações formais, a linguagem como um todo não é 
formalmente especificada. O padrão de facto é a implementação CPython.
A filosofia de design do Python enfatiza a importância do esforço do programador 
sobre o esforço computacional. Prioriza a legibilidade do código sobre a velocidade 
ou expressividade. Combina uma sintaxe concisa e clara com os recursos poderosos 
de sua biblioteca padrão e por uma vasta gama de módulos e frameworks 
desenvolvidos por terceiros. Python é uma linguagem de propósito geral de alto 
nível, multiparadigma, suporta o paradigma orientado a objetos, imperativo, 
funcional e procedural. Possui tipagem dinâmica e uma de suas principais 
características é permitir a fácil leitura do código e exigir poucas linhas 
de código se comparado ao mesmo programa em outras linguagens.
        """ * 2
    }
    
    # Cria agente otimizado
    log.step("Criando agente com prompts otimizados")
    optimized_agent = create_agent(
        "ESPECIALISTA EM ANÁLISE TÉCNICA\n"
        "═══════════════════════════════\n\n"
        "MISSÃO: Analisar conteúdo técnico e extrair insights importantes.\n\n"
        "INSTRUÇÕES:\n"
        "• Identifique pontos-chave\n"
        "• Use linguagem técnica apropriada\n"
        "• Seja conciso mas informativo\n"
        "• Foque em aspectos práticos\n\n"
        "FORMATO: Resposta estruturada em português brasileiro.",
        max_tokens=400
    )
    
    # Testa com diferentes tamanhos
    test_results = []
    
    with RichProgress("Testando conteúdos de diferentes tamanhos") as progress:
        total_tests = len(test_contents)
        for i, (size_name, content) in enumerate(test_contents.items()):
            progress.update((i / total_tests) * 100, f"Testando conteúdo {size_name}")
            
            start_time = time.time()
            
            try:
                response = optimized_agent(f"Analise este conteúdo sobre Python:\n\n{content}")
                processing_time = time.time() - start_time
                
                test_results.append({
                    "Tamanho": size_name.title(),
                    "Chars Input": len(content),
                    "Chars Output": len(response),
                    "Tempo (s)": f"{processing_time:.2f}",
                    "Status": "✅ Sucesso"
                })
                
                log.success(f"Conteúdo {size_name} processado em {processing_time:.2f}s")
                
            except Exception as e:
                test_results.append({
                    "Tamanho": size_name.title(),
                    "Chars Input": len(content),
                    "Chars Output": 0,
                    "Tempo (s)": "N/A",
                    "Status": f"❌ {str(e)[:30]}..."
                })
                log.error(f"Erro no conteúdo {size_name}: {e}")
    
    # Exibe tabela de resultados
    if test_results:
        table = RichTable.create_summary_table(test_results, "Resultados dos Testes de Prompts")
        console.print(table)
    
    log.success("Teste de prompts otimizados concluído!")


def test_system_config():
    """Testa as configurações do sistema."""
    print_section("TESTANDO CONFIGURAÇÕES DO SISTEMA")
    
    # Testa configurações de diferentes tamanhos
    sizes = [500, 1500, 4000]
    config_results = []
    
    for size in sizes:
        config = SystemConfig.get_cohere_config(size)
        config_results.append({
            "Tamanho": f"{size} chars",
            "Tokens": config['max_tokens'],
            "Temperature": config['temperature'],
            "P-value": config['p']
        })
    
    # Exibe tabela de configurações por tamanho
    if config_results:
        table = RichTable.create_summary_table(config_results, "Configurações por Tamanho de Conteúdo")
        console.print(table)
    
    # Testa configurações de agentes
    agents = ['resumidor', 'analista', 'organizador', 'sintetizador']
    agent_results = []
    
    for agent in agents:
        config = SystemConfig.get_agent_config(agent)
        agent_results.append({
            "Agente": agent.title(),
            "Tokens": config['max_tokens'],
            "Temperature": config.get('temperature', 'N/A'),
            "Especialização": config.get('role', 'N/A')[:30] + "..."
        })
    
    # Exibe tabela de configurações de agentes
    if agent_results:
        table = RichTable.create_summary_table(agent_results, "Configurações dos Agentes Especializados")
        console.print(table)
    
    log.success("Teste de configurações concluído!")


def benchmark_performance():
    """Benchmark básico de performance."""
    print_section("BENCHMARK DE PERFORMANCE")
    
    if not test_api_connection():
        log.error("Não é possível fazer benchmark sem conexão API")
        return
    
    # Cria agente simples para teste
    test_agent = create_agent("Responda de forma concisa sobre o tema apresentado.")
    
    test_prompts = [
        "O que é Python?",
        "Explique programação orientada a objetos em Python.",
        "Descreva as vantagens do Python para ciência de dados.",
    ]
    
    benchmark_results = []
    total_time = 0
    successful_calls = 0
    
    with RichProgress("Executando benchmark de performance") as progress:
        for i, prompt in enumerate(test_prompts):
            progress.update((i / len(test_prompts)) * 100, f"Teste {i+1}/{len(test_prompts)}")
            
            start_time = time.time()
            
            try:
                response = test_agent(prompt)
                end_time = time.time()
                
                call_time = end_time - start_time
                total_time += call_time
                successful_calls += 1
                
                benchmark_results.append({
                    "Teste": f"#{i+1}",
                    "Prompt": prompt[:30] + "...",
                    "Tempo (s)": f"{call_time:.2f}",
                    "Chars": len(response),
                    "Status": "✅ Sucesso"
                })
                
                log.success(f"Teste {i+1} concluído em {call_time:.2f}s")
                
            except Exception as e:
                benchmark_results.append({
                    "Teste": f"#{i+1}",
                    "Prompt": prompt[:30] + "...",
                    "Tempo (s)": "N/A",
                    "Chars": 0,
                    "Status": f"❌ {str(e)[:20]}..."
                })
                log.error(f"Falha no teste {i+1}: {e}")
    
    # Exibe resultados do benchmark
    if benchmark_results:
        table = RichTable.create_summary_table(benchmark_results, "Resultados do Benchmark")
        console.print(table)
    
    if successful_calls > 0:
        avg_time = total_time / successful_calls
        console.print(f"\n[bold green]📊 ESTATÍSTICAS FINAIS:[/bold green]")
        console.print(f"   [cyan]•[/cyan] Chamadas bem-sucedidas: [bold]{successful_calls}/{len(test_prompts)}[/bold]")
        console.print(f"   [cyan]•[/cyan] Tempo médio por chamada: [bold]{avg_time:.2f}s[/bold]")
        console.print(f"   [cyan]•[/cyan] Tempo total: [bold]{total_time:.2f}s[/bold]")
    else:
        log.error("Nenhuma chamada bem-sucedida")


if __name__ == "__main__":
    print_header("SISTEMA DE TESTES DE OTIMIZAÇÃO", "Validação completa das melhorias implementadas")
    
    try:
        # Executa todos os testes
        test_system_config()
        test_optimized_prompts()
        benchmark_performance()
        
        console.print()
        log.success("TODOS OS TESTES CONCLUÍDOS!")
        log.info("Sistema otimizado e pronto para uso.")
        
    except Exception as e:
        log.error(f"Erro durante testes: {e}")
        log.info("Verifique a configuração da API Cohere.")
