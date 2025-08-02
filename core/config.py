"""
Configurações Avançadas do Sistema
==================================

Este módulo centraliza todas as configurações do sistema para facilitar
ajustes de performance e personalização.

Autor: Marco
Data: Agosto 2025
"""

import os
from typing import Dict, Any


class SystemConfig:
    """Classe de configuração centralizada do sistema."""
    
    # ========================================================================
    # CONFIGURAÇÕES DE IA E PROCESSAMENTO
    # ========================================================================
    
    # Configurações Cohere API
    COHERE_DEFAULT_TEMPERATURE = 0.6
    COHERE_MAX_TOKENS_SMALL = 400
    COHERE_MAX_TOKENS_MEDIUM = 800
    COHERE_MAX_TOKENS_LARGE = 1200
    COHERE_K_VALUE = 0  # Nucleus sampling
    COHERE_P_VALUE = 0.9  # Top-p sampling
    COHERE_FREQUENCY_PENALTY = 0.1
    COHERE_PRESENCE_PENALTY = 0.1
    
    # Limites de conteúdo para processamento
    CONTENT_SMALL_THRESHOLD = 1000
    CONTENT_MEDIUM_THRESHOLD = 3000
    CONTENT_LARGE_THRESHOLD = 6000
    
    # Processamento multi-agente
    MAX_CONTENT_LENGTH = 3000
    MAX_SYNTHESIS_LENGTH = 12000
    AGENT_CONTEXT_WINDOW = 8000
    
    # ========================================================================
    # CONFIGURAÇÕES DE WEB SCRAPING
    # ========================================================================
    
    # Timeouts e limites
    REQUEST_TIMEOUT = 15
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    
    # Tamanhos de conteúdo
    MAX_PAGE_CONTENT = 8000
    MIN_CONTENT_LENGTH = 100
    
    # Headers HTTP
    DEFAULT_USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
    }
    
    # ========================================================================
    # CONFIGURAÇÕES DE SAÍDA E FORMATAÇÃO
    # ========================================================================
    
    # Arquivos e diretórios
    OUTPUT_DIRECTORY = "outputs"
    BACKUP_DIRECTORY = "backups"
    LOG_DIRECTORY = "logs"
    
    # Encoding
    DEFAULT_ENCODING = 'utf-8'
    
    # Formatação de datas
    DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
    DATE_FORMAT = '%d/%m/%Y'
    
    # ========================================================================
    # CONFIGURAÇÕES DE PERFORMANCE
    # ========================================================================
    
    # Cache e otimização
    ENABLE_CACHE = True
    CACHE_DURATION = 3600  # 1 hora
    
    # Processamento paralelo
    MAX_WORKERS = 4
    ENABLE_PARALLEL_PROCESSING = False  # Para desenvolvimento futuro
    
    # ========================================================================
    # CONFIGURAÇÕES DE DEBUG E LOGGING
    # ========================================================================
    
    # Níveis de log
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    ENABLE_VERBOSE = True
    SAVE_DEBUG_FILES = True
    
    # Estatísticas
    COLLECT_STATS = True
    SHOW_PROGRESS_BARS = True
    
    @classmethod
    def get_cohere_config(cls, content_size: int) -> Dict[str, Any]:
        """
        Retorna configuração otimizada do Cohere baseada no tamanho do conteúdo.
        
        Args:
            content_size (int): Tamanho do conteúdo em caracteres
            
        Returns:
            Dict[str, Any]: Configuração otimizada
        """
        if content_size <= cls.CONTENT_SMALL_THRESHOLD:
            return {
                'max_tokens': cls.COHERE_MAX_TOKENS_SMALL,
                'temperature': cls.COHERE_DEFAULT_TEMPERATURE + 0.1,
                'k': cls.COHERE_K_VALUE,
                'p': cls.COHERE_P_VALUE,
                'frequency_penalty': cls.COHERE_FREQUENCY_PENALTY,
                'presence_penalty': cls.COHERE_PRESENCE_PENALTY
            }
        elif content_size <= cls.CONTENT_MEDIUM_THRESHOLD:
            return {
                'max_tokens': cls.COHERE_MAX_TOKENS_MEDIUM,
                'temperature': cls.COHERE_DEFAULT_TEMPERATURE,
                'k': cls.COHERE_K_VALUE,
                'p': cls.COHERE_P_VALUE,
                'frequency_penalty': cls.COHERE_FREQUENCY_PENALTY,
                'presence_penalty': cls.COHERE_PRESENCE_PENALTY
            }
        else:
            return {
                'max_tokens': cls.COHERE_MAX_TOKENS_LARGE,
                'temperature': cls.COHERE_DEFAULT_TEMPERATURE - 0.1,
                'k': cls.COHERE_K_VALUE,
                'p': cls.COHERE_P_VALUE - 0.05,
                'frequency_penalty': cls.COHERE_FREQUENCY_PENALTY + 0.05,
                'presence_penalty': cls.COHERE_PRESENCE_PENALTY + 0.05
            }
    
    @classmethod
    def get_agent_config(cls, agent_type: str) -> Dict[str, Any]:
        """
        Retorna configuração específica para cada tipo de agente.
        
        Args:
            agent_type (str): Tipo do agente (resumidor, analista, etc.)
            
        Returns:
            Dict[str, Any]: Configuração específica do agente
        """
        configs = {
            'resumidor': {
                'max_tokens': 600,
                'temperature': 0.5,
                'focus': 'concisão e clareza'
            },
            'analista': {
                'max_tokens': 800,
                'temperature': 0.6,
                'focus': 'insights e padrões'
            },
            'organizador': {
                'max_tokens': 700,
                'temperature': 0.4,
                'focus': 'estrutura e hierarquia'
            },
            'sintetizador': {
                'max_tokens': 1200,
                'temperature': 0.5,
                'focus': 'integração e síntese'
            }
        }
        
        return configs.get(agent_type, {
            'max_tokens': cls.COHERE_MAX_TOKENS_MEDIUM,
            'temperature': cls.COHERE_DEFAULT_TEMPERATURE,
            'focus': 'análise geral'
        })
    
    @classmethod
    def load_from_env(cls) -> None:
        """Carrega configurações de variáveis de ambiente."""
        # Configurações que podem ser sobrescritas por variáveis de ambiente
        env_mappings = {
            'REQUEST_TIMEOUT': ('REQUEST_TIMEOUT', int),
            'MAX_CONTENT_LENGTH': ('MAX_CONTENT_LENGTH', int),
            'COHERE_DEFAULT_TEMPERATURE': ('COHERE_TEMPERATURE', float),
            'LOG_LEVEL': ('LOG_LEVEL', str),
            'ENABLE_VERBOSE': ('VERBOSE_MODE', lambda x: x.lower() == 'true'),
        }
        
        for attr, (env_var, converter) in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value:
                try:
                    setattr(cls, attr, converter(env_value))
                except (ValueError, TypeError):
                    print(f"⚠️ Valor inválido para {env_var}: {env_value}")
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Valida se as configurações estão corretas.
        
        Returns:
            bool: True se configurações válidas
        """
        validations = [
            (cls.REQUEST_TIMEOUT > 0, "REQUEST_TIMEOUT deve ser positivo"),
            (0.0 <= cls.COHERE_DEFAULT_TEMPERATURE <= 1.0, "Temperature deve estar entre 0 e 1"),
            (cls.MAX_CONTENT_LENGTH > 0, "MAX_CONTENT_LENGTH deve ser positivo"),
            (cls.COHERE_MAX_TOKENS_LARGE > cls.COHERE_MAX_TOKENS_MEDIUM, "Tokens devem ser crescentes"),
        ]
        
        for is_valid, message in validations:
            if not is_valid:
                print(f"❌ Erro de configuração: {message}")
                return False
        
        return True


# Carrega configurações de ambiente na importação
SystemConfig.load_from_env()

# Valida configurações
if not SystemConfig.validate_config():
    print("⚠️ Algumas configurações podem estar incorretas")

# Exports para fácil importação
__all__ = ['SystemConfig']
