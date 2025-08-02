"""
Módulo de Console com Rich - Versão Compatível
==============================================

Utilitários centralizados para interface rica no terminal.
Substitui prints simples por output formatado e profissional.
Versão otimizada para compatibilidade com diferentes versões do Rich.

Autor: Marco
Data: Agosto 2025
"""

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.table import Table
    from rich.text import Text
    from rich.tree import Tree
    from rich.columns import Columns
    from rich.align import Align
    from rich.live import Live
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    from rich.prompt import Prompt, Confirm
    from rich.status import Status
    RICH_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Rich não disponível: {e}")
    print("💡 Usando fallback para interface simples")
    RICH_AVAILABLE = False

from typing import Any, Dict, List, Optional
import time

# Console global configurado
if RICH_AVAILABLE:
    console = Console(width=120, force_terminal=True)
else:
    # Fallback simples
    class MockConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = MockConsole()


class RichLogger:
    """Logger customizado usando Rich para output profissional."""
    
    def __init__(self):
        self.console = console
    
    def info(self, message: str, title: str = "Info"):
        """Log de informação com formatação azul."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold blue]ℹ️  {title}:[/bold blue] {message}")
        else:
            print(f"ℹ️  {title}: {message}")
    
    def success(self, message: str, title: str = "Sucesso"):
        """Log de sucesso com formatação verde."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold green]✅ {title}:[/bold green] {message}")
        else:
            print(f"✅ {title}: {message}")
    
    def warning(self, message: str, title: str = "Aviso"):
        """Log de aviso com formatação amarela."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold yellow]⚠️  {title}:[/bold yellow] {message}")
        else:
            print(f"⚠️  {title}: {message}")
    
    def error(self, message: str, title: str = "Erro"):
        """Log de erro com formatação vermelha."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold red]❌ {title}:[/bold red] {message}")
        else:
            print(f"❌ {title}: {message}")
    
    def debug(self, message: str, title: str = "Debug"):
        """Log de debug com formatação magenta."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold magenta]🔍 {title}:[/bold magenta] {message}")
        else:
            print(f"🔍 {title}: {message}")
    
    def step(self, message: str, step_num: int = None):
        """Log de passo do processo."""
        if step_num:
            if RICH_AVAILABLE:
                self.console.print(f"[bold cyan]🔄 Passo {step_num}:[/bold cyan] {message}")
            else:
                print(f"🔄 Passo {step_num}: {message}")
        else:
            if RICH_AVAILABLE:
                self.console.print(f"[bold cyan]🔄[/bold cyan] {message}")
            else:
                print(f"🔄 {message}")
    
    def result(self, message: str, value: Any = None):
        """Log de resultado com valor opcional."""
        if value is not None:
            if RICH_AVAILABLE:
                self.console.print(f"[bold green]📊 Resultado:[/bold green] {message} = [bold]{value}[/bold]")
            else:
                print(f"📊 Resultado: {message} = {value}")
        else:
            if RICH_AVAILABLE:
                self.console.print(f"[bold green]📊 Resultado:[/bold green] {message}")
            else:
                print(f"📊 Resultado: {message}")


class RichPanel:
    """Criador de painéis formatados para diferentes contextos."""
    
    @staticmethod
    def title_panel(title: str, subtitle: str = None):
        """Cria painel de título principal."""
        if not RICH_AVAILABLE:
            print(f"\n{'='*60}")
            print(f"  {title}")
            if subtitle:
                print(f"  {subtitle}")
            print(f"{'='*60}\n")
            return None
            
        content = f"[bold blue]{title}[/bold blue]"
        if subtitle:
            content += f"\n[dim]{subtitle}[/dim]"
        
        return Panel(
            Align.center(Text(content, justify="center")),
            style="bold blue",
            padding=(1, 2)
        )
    
    @staticmethod
    def info_panel(content: str, title: str = "Informação"):
        """Cria painel informativo."""
        if not RICH_AVAILABLE:
            print(f"\n--- {title} ---")
            print(content)
            print("-" * (len(title) + 8))
            return None
            
        return Panel(
            content,
            title=f"[bold blue]ℹ️  {title}[/bold blue]",
            border_style="blue",
            padding=(0, 1)
        )
    
    @staticmethod
    def success_panel(content: str, title: str = "Sucesso"):
        """Cria painel de sucesso."""
        if not RICH_AVAILABLE:
            print(f"\n✅ {title}")
            print(content)
            print("-" * 40)
            return None
            
        return Panel(
            content,
            title=f"[bold green]✅ {title}[/bold green]",
            border_style="green",
            padding=(0, 1)
        )
    
    @staticmethod
    def error_panel(content: str, title: str = "Erro"):
        """Cria painel de erro."""
        if not RICH_AVAILABLE:
            print(f"\n❌ {title}")
            print(content)
            print("-" * 40)
            return None
            
        return Panel(
            content,
            title=f"[bold red]❌ {title}[/bold red]",
            border_style="red",
            padding=(0, 1)
        )
    
    @staticmethod
    def config_panel(configs: Dict[str, Any], title: str = "Configurações"):
        """Cria painel de configurações."""
        if not RICH_AVAILABLE:
            print(f"\n⚙️  {title}")
            for key, value in configs.items():
                print(f"  • {key}: {value}")
            print("-" * 40)
            return None
            
        content = ""
        for key, value in configs.items():
            content += f"[bold cyan]•[/bold cyan] {key}: [bold]{value}[/bold]\n"
        
        return Panel(
            content.rstrip(),
            title=f"[bold yellow]⚙️  {title}[/bold yellow]",
            border_style="yellow",
            padding=(0, 1)
        )


class RichProgress:
    """Gerenciador de progresso avançado."""
    
    def __init__(self, description: str = "Processando..."):
        if RICH_AVAILABLE:
            self.progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40),
                TaskProgressColumn(),
                console=console
            )
        else:
            self.progress = None
        self.description = description
        self.task_id = None
        self.is_rich = RICH_AVAILABLE
    
    def __enter__(self):
        if self.is_rich:
            self.progress.start()
            self.task_id = self.progress.add_task(self.description, total=100)
        else:
            print(f"🔄 {self.description}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_rich:
            self.progress.stop()
    
    def update(self, completed: int, description: str = None):
        """Atualiza o progresso."""
        if self.is_rich and self.progress:
            if description:
                self.progress.update(self.task_id, completed=completed, description=description)
            else:
                self.progress.update(self.task_id, completed=completed)
        else:
            if description:
                print(f"🔄 {description} ({completed:.0f}%)")
    
    def complete(self):
        """Marca como concluído."""
        if self.is_rich and self.progress:
            self.progress.update(self.task_id, completed=100)
        else:
            print("✅ Concluído!")


class RichTable:
    """Criador de tabelas formatadas."""
    
    @staticmethod
    def create_summary_table(data: List[Dict[str, Any]], title: str = "Resumo"):
        """Cria tabela de resumo."""
        if not RICH_AVAILABLE or not data:
            print(f"\n📊 {title}")
            print("-" * 50)
            for i, item in enumerate(data):
                print(f"{i+1}. {item}")
            print("-" * 50)
            return None
            
        table = Table(title=f"[bold blue]{title}[/bold blue]", show_header=True, header_style="bold cyan")
        
        # Adiciona colunas baseadas nas chaves do primeiro item
        for key in data[0].keys():
            table.add_column(key.title(), style="white")
        
        # Adiciona linhas
        for item in data:
            row = [str(value) for value in item.values()]
            table.add_row(*row)
        
        return table
    
    @staticmethod
    def create_config_table(configs: Dict[str, Any], title: str = "Configurações"):
        """Cria tabela de configurações."""
        if not RICH_AVAILABLE:
            print(f"\n⚙️  {title}")
            print("-" * 50)
            for key, value in configs.items():
                print(f"{key}: {value} ({type(value).__name__})")
            print("-" * 50)
            return None
            
        table = Table(title=f"[bold yellow]{title}[/bold yellow]", show_header=True, header_style="bold yellow")
        table.add_column("Parâmetro", style="cyan")
        table.add_column("Valor", style="white")
        table.add_column("Tipo", style="dim")
        
        for key, value in configs.items():
            table.add_row(key, str(value), type(value).__name__)
        
        return table


class RichStatus:
    """Indicador de status para operações longas."""
    
    def __init__(self, message: str, spinner: str = "dots"):
        if RICH_AVAILABLE:
            self.status = Status(message, spinner=spinner, console=console)
        else:
            self.status = None
        self.message = message
        self.is_rich = RICH_AVAILABLE
    
    def __enter__(self):
        if self.is_rich:
            self.status.start()
        else:
            print(f"🔄 {self.message}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_rich:
            self.status.stop()
    
    def update(self, message: str):
        """Atualiza a mensagem do status."""
        if self.is_rich:
            self.status.update(message)
        else:
            print(f"🔄 {message}")


def print_header(title: str, subtitle: str = None):
    """Imprime cabeçalho principal da aplicação."""
    if RICH_AVAILABLE:
        console.print()
        panel = RichPanel.title_panel(title, subtitle)
        if panel:
            console.print(panel)
        console.print()
    else:
        print("\n" + "="*60)
        print(f"  {title}")
        if subtitle:
            print(f"  {subtitle}")
        print("="*60 + "\n")


def print_section(title: str):
    """Imprime título de seção."""
    if RICH_AVAILABLE:
        console.print(f"\n[bold cyan]{'='*20} {title} {'='*20}[/bold cyan]")
    else:
        print(f"\n{'='*20} {title} {'='*20}")


def print_step(step: int, total: int, description: str):
    """Imprime passo do processo."""
    if RICH_AVAILABLE:
        console.print(f"[bold blue]📋 Passo {step}/{total}:[/bold blue] {description}")
    else:
        print(f"📋 Passo {step}/{total}: {description}")


def print_result(title: str, content: str, success: bool = True):
    """Imprime resultado formatado."""
    if RICH_AVAILABLE:
        if success:
            panel = RichPanel.success_panel(content, title)
        else:
            panel = RichPanel.error_panel(content, title)
        if panel:
            console.print(panel)
    else:
        prefix = "✅" if success else "❌"
        print(f"\n{prefix} {title}")
        print(content)
        print("-" * 40)


def print_config(configs: Dict[str, Any], title: str = "Configurações"):
    """Imprime configurações em formato de tabela."""
    if RICH_AVAILABLE:
        table = RichTable.create_config_table(configs, title)
        if table:
            console.print(table)
    else:
        print(f"\n⚙️  {title}")
        for key, value in configs.items():
            print(f"  • {key}: {value}")
        print("-" * 40)


def print_json_data(data: Dict[str, Any], title: str = "Dados JSON"):
    """Imprime dados JSON formatados."""
    import json
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    if RICH_AVAILABLE:
        try:
            syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
            panel = Panel(
                syntax,
                title=f"[bold green]📋 {title}[/bold green]",
                border_style="green"
            )
            console.print(panel)
        except:
            # Fallback se Syntax falhar
            print(f"\n📋 {title}")
            print("-" * 50)
            print(json_str)
            print("-" * 50)
    else:
        print(f"\n📋 {title}")
        print("-" * 50)
        print(json_str)
        print("-" * 50)


def confirm_action(message: str, default: bool = True) -> bool:
    """Solicita confirmação do usuário."""
    if RICH_AVAILABLE:
        try:
            return Confirm.ask(f"[yellow]❓[/yellow] {message}", default=default, console=console)
        except:
            pass
    
    # Fallback simples
    prompt_text = f"❓ {message} ({'S/n' if default else 's/N'}): "
    response = input(prompt_text).strip().lower()
    if not response:
        return default
    return response in ['s', 'sim', 'y', 'yes']


def prompt_input(message: str, default: str = None) -> str:
    """Solicita entrada do usuário."""
    if RICH_AVAILABLE:
        try:
            return Prompt.ask(f"[cyan]📝[/cyan] {message}", default=default, console=console)
        except:
            pass
    
    # Fallback simples
    prompt_text = f"📝 {message}"
    if default:
        prompt_text += f" [{default}]"
    prompt_text += ": "
    
    response = input(prompt_text).strip()
    return response or default or ""


# Instância global do logger
log = RichLogger()


# Aliases para compatibilidade
def print_info(message: str):
    """Alias para log.info."""
    log.info(message)


def print_success(message: str):
    """Alias para log.success."""
    log.success(message)


def print_error(message: str):
    """Alias para log.error."""
    log.error(message)


def print_warning(message: str):
    """Alias para log.warning."""
    log.warning(message)


# Função auxiliar para imprimir com formatação quando Rich disponível
def print_formatted(text: str, style: str = ""):
    """Imprime texto com formatação Rich se disponível, senão print normal."""
    if RICH_AVAILABLE and style:
        console.print(f"[{style}]{text}[/{style}]")
    else:
        print(text)
