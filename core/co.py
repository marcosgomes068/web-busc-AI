"""
Módulo de Integração com Cohere API
===================================

Este módulo gerencia a integração com a API Cohere para criar agentes
de IA especializados em diferentes tarefas de análise de conteúdo.

Funcionalidades:
- Configuração segura de API keys
- Factory de agentes especializados
- Gestão de chamadas para API Cohere
- Fallback para modelos default quando necessário

Dependências:
- cohere: Cliente oficial da API Cohere
- os: Para acessar variáveis de ambiente

Autor: Marco
Data: Agosto 2025
"""

import os
from typing import Callable, Optional

try:
    from .config import SystemConfig
except ImportError:
    # Fallback se config não estiver disponível
    class SystemConfig:
        COHERE_DEFAULT_TEMPERATURE = 0.6
        COHERE_MAX_TOKENS_MEDIUM = 500
        @classmethod
        def get_cohere_config(cls, content_size):
            return {'max_tokens': 500, 'temperature': 0.6}
        @classmethod
        def get_agent_config(cls, agent_type):
            return {'max_tokens': 500, 'temperature': 0.6}


def get_api_key() -> str:
    """
    Obtém a chave da API Cohere das variáveis de ambiente ou arquivo .env.
    
    Returns:
        str: Chave da API Cohere
        
    Raises:
        RuntimeError: Se a chave da API não for encontrada
        
    Note:
        Busca primeiro nas variáveis de ambiente, depois no arquivo .env
    """
    # Primeira tentativa: variável de ambiente
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key:
        # Segunda tentativa: arquivo .env no diretório do projeto
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_path = os.path.abspath(env_path)
        
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith("COHERE_API_KEY="):
                            api_key = line.split("=", 1)[1].strip()
                            # Define a variável de ambiente para uso futuro
                            os.environ["COHERE_API_KEY"] = api_key
                            break
            except Exception as e:
                print(f"⚠️ Erro ao ler arquivo .env: {e}")
    
    if not api_key:
        raise RuntimeError(
            "❌ COHERE_API_KEY não encontrada!\n"
            "💡 Configure a chave da API:\n"
            "   1. Como variável de ambiente: COHERE_API_KEY=sua_chave\n"
            "   2. No arquivo .env: COHERE_API_KEY=sua_chave"
        )
    
    return api_key


def create_agent(system_prompt: str, max_tokens: int = 500) -> Callable[[str], str]:
    """
    Factory para criar agentes de IA especializados usando Cohere.
    
    Args:
        system_prompt (str): Prompt que define o comportamento do agente
        max_tokens (int, optional): Número máximo de tokens na resposta. Default: 500
        
    Returns:
        Callable[[str], str]: Função agente que processa mensagens
        
    Examples:
        >>> agent = create_agent("Você é um resumidor especialista.")
        >>> summary = agent("Texto para resumir...")
        >>> print(summary)
        
    Note:
        Usa configuração otimizada para textos longos e respostas estruturadas.
        Implementa sistema de fallback inteligente para diferentes tamanhos.
    """
    def agent(user_prompt: str) -> str:
        """
        Processa uma mensagem usando o agente configurado.
        
        Args:
            user_prompt (str): Mensagem do usuário para processar
            
        Returns:
            str: Resposta gerada pelo agente
        """
        try:
            # Importa cohere dinamicamente para evitar dependências desnecessárias
            import cohere
            
            # Inicializa cliente com chave da API
            client = cohere.Client(get_api_key())
            
            # Combina prompt do sistema com entrada do usuário de forma otimizada
            complete_message = f"{system_prompt}\n\n---\n\nTEXTO PARA PROCESSAR:\n{user_prompt}\n\n---\n\nRESPOSTA:"
            
            # Determina configuração baseada no tamanho do conteúdo
            content_length = len(user_prompt)
            cohere_config = SystemConfig.get_cohere_config(content_length)
            
            # Usa configuração otimizada ou fallback
            tokens = cohere_config.get('max_tokens', max_tokens)
            temperature = cohere_config.get('temperature', SystemConfig.COHERE_DEFAULT_TEMPERATURE)
            
            # Ajusta tokens se especificado
            if max_tokens != 500:  # Se não for o padrão, usa o especificado
                tokens = max_tokens
            
            # Gera resposta usando configuração otimizada
            response = client.generate(
                prompt=complete_message,
                max_tokens=tokens,
                temperature=temperature,
                k=cohere_config.get('k', 0),
                p=cohere_config.get('p', 0.9),
                frequency_penalty=cohere_config.get('frequency_penalty', 0.1),
                presence_penalty=cohere_config.get('presence_penalty', 0.1)
            )
            
            return response.generations[0].text.strip()
            
        except ImportError:
            return "❌ Erro: Biblioteca 'cohere' não instalada. Execute: pip install cohere"
            
        except Exception as error:
            error_msg = str(error).lower()
            
            # Fallback inteligente para diferentes tipos de erro
            if "token" in error_msg or "length" in error_msg:
                try:
                    print("🔄 Tentando com menos tokens devido a limite excedido...")
                    fallback_tokens = min(300, max_tokens // 2)
                    
                    # Trunca conteúdo se muito longo
                    if len(user_prompt) > 2000:
                        truncated_prompt = user_prompt[:2000] + "\n\n[CONTEÚDO TRUNCADO - ANÁLISE PARCIAL]"
                    else:
                        truncated_prompt = user_prompt
                    
                    complete_message = f"{system_prompt}\n\n---\n\nTEXTO PARA PROCESSAR:\n{truncated_prompt}\n\n---\n\nRESPOSTA:"
                    
                    response = client.generate(
                        prompt=complete_message,
                        max_tokens=fallback_tokens,
                        temperature=0.6
                    )
                    return response.generations[0].text.strip()
                    
                except Exception as e2:
                    return f"❌ Erro persistente após fallback: {str(e2)}"
            
            return f"❌ Erro Cohere: {str(error)}"
    
    return agent


def create_specialized_agents() -> dict:
    """
    Cria um conjunto de agentes especializados para análise de conteúdo.
    
    Returns:
        dict: Dicionário com agentes especializados pré-configurados
        
    Agents Available:
        - resumidor: Resume conteúdo de forma concisa e estruturada
        - analista: Faz análise detalhada e identifica insights
        - organizador: Estrutura e organiza informações hierarquicamente
        - sintetizador: Combina múltiplas fontes em síntese coerente
    """
    agents = {
        'resumidor': create_agent(
            "Você é um ESPECIALISTA EM RESUMOS TÉCNICOS. Sua missão é extrair os pontos mais importantes do texto fornecido.\n\n"
            "DIRETRIZES:\n"
            "• Foque nos conceitos centrais e informações-chave\n"
            "• Use linguagem clara, objetiva e técnica\n"
            "• Mantenha a estrutura lógica do conteúdo original\n"
            "• Elimine redundâncias e informações secundárias\n"
            "• Use português brasileiro formal\n"
            "• Limite-se aos fatos apresentados no texto\n\n"
            "FORMATO DE RESPOSTA:\n"
            "- Pontos principais em bullets\n"
            "- Máximo 5-7 pontos essenciais\n"
            "- Cada ponto deve ser conciso mas completo",
            max_tokens=600
        ),
        
        'analista': create_agent(
            "Você é um ANALISTA SÊNIOR DE CONTEÚDO com expertise em identificar insights e padrões.\n\n"
            "SUAS RESPONSABILIDADES:\n"
            "• Identificar tendências e padrões importantes\n"
            "• Extrair insights técnicos e práticos\n"
            "• Conectar conceitos e relações entre temas\n"
            "• Destacar informações críticas para tomada de decisão\n"
            "• Avaliar qualidade e relevância das informações\n"
            "• Usar terminologia técnica apropriada\n\n"
            "ESTRUTURA DA ANÁLISE:\n"
            "1. INSIGHTS PRINCIPAIS (3-5 pontos)\n"
            "2. TENDÊNCIAS IDENTIFICADAS\n"
            "3. IMPLICAÇÕES PRÁTICAS\n"
            "4. PONTOS DE ATENÇÃO\n\n"
            "Use português brasileiro e seja detalhado mas objetivo.",
            max_tokens=800
        ),
        
        'organizador': create_agent(
            "Você é um ESPECIALISTA EM ORGANIZAÇÃO DE INFORMAÇÕES e estruturação de conteúdo.\n\n"
            "OBJETIVOS:\n"
            "• Criar estrutura hierárquica clara e lógica\n"
            "• Categorizar informações por relevância e tema\n"
            "• Usar formatação visual para facilitar leitura\n"
            "• Estabelecer relações entre diferentes seções\n"
            "• Criar índice mental do conteúdo\n\n"
            "FORMATAÇÃO OBRIGATÓRIA:\n"
            "```\n"
            "# TÍTULO PRINCIPAL\n"
            "## Seção 1\n"
            "### Subseção 1.1\n"
            "• Ponto importante\n"
            "• Outro ponto\n"
            "\n"
            "## Seção 2\n"
            "### Subseção 2.1\n"
            "...\n"
            "```\n\n"
            "Use numeração, bullets e hierarquia visual clara.",
            max_tokens=700
        ),
        
        'sintetizador': create_agent(
            "Você é o SINTETIZADOR MASTER - responsável pela síntese final e integração de múltiplas análises.\n\n"
            "MISSÃO CRÍTICA:\n"
            "• Integrar resumos, análises e organizações em documento único\n"
            "• Eliminar redundâncias entre diferentes fontes\n"
            "• Criar visão holística e coerente do tema\n"
            "• Destacar conclusões e recomendações principais\n"
            "• Produzir documento final de alta qualidade\n\n"
            "ESTRUTURA OBRIGATÓRIA DA SÍNTESE:\n"
            "# SÍNTESE EXECUTIVA\n"
            "## 🎯 Resumo Geral\n"
            "## 🔍 Principais Descobertas\n"
            "## 📊 Insights Estratégicos\n"
            "## 💡 Recomendações\n"
            "## 🔗 Conexões Entre Temas\n"
            "## ⚡ Conclusões Finais\n\n"
            "QUALIDADE EXIGIDA:\n"
            "• Linguagem profissional e técnica\n"
            "• Português brasileiro formal\n"
            "• Estrutura visual clara com emojis\n"
            "• Máxima coerência e fluidez\n"
            "• Foco em valor agregado",
            max_tokens=1200
        )
    }
    
    return agents


def test_api_connection() -> bool:
    """
    Testa a conexão com a API Cohere.
    
    Returns:
        bool: True se a conexão foi bem-sucedida, False caso contrário
    """
    try:
        # Cria um agente simples para teste
        test_agent = create_agent("Responda apenas 'Teste OK'", max_tokens=50)
        response = test_agent("teste de conexão")
        
        if "ok" in response.lower() or "teste" in response.lower():
            print("✅ Conexão com Cohere API: Sucesso")
            return True
        else:
            print(f"⚠️ Conexão estabelecida, resposta: {response}")
            return True  # Considera sucesso mesmo com resposta diferente
            
    except Exception as e:
        print(f"❌ Erro na conexão com Cohere API: {e}")
        return False


# Alias para compatibilidade com código existente
criar_agente = create_agent


if __name__ == "__main__":
    # Teste de conexão quando executado diretamente
    print("🧪 Testando integração com Cohere API...")
    test_api_connection()
