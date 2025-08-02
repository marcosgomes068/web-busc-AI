# 📘 Integração Python-C# - Sistema de Análise Web

## 🎯 Visão Geral

Este documento fornece o **guia completo** para integrar o sistema Python de análise web com aplicações C#. O sistema Python atua como um **serviço de análise inteligente** que pode ser consumido por aplicações C# através de diferentes métodos de integração.

---

## 🏗️ Arquitetura de Integração

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Aplicação C#  │◄──►│   Interface     │◄──►│  Sistema Python │
│                 │    │   (Processo/    │    │  (Análise Web)  │
│  • Windows Forms│    │    API/Files)   │    │                 │
│  • WPF          │    │                 │    │  • Web Scraping │
│  • Console      │    │                 │    │  • IA Multi-    │
│  • Web API      │    │                 │    │    Agente       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🚀 Métodos de Integração

### 1️⃣ **Integração por Processo (Recomendado)**
Execute o Python como processo filho e capture a saída.

### 2️⃣ **Integração por Arquivos**
Troque dados através de arquivos JSON.

### 3️⃣ **Integração via API REST**
Sistema Python como serviço web (Flask/FastAPI).

### 4️⃣ **Integração via Named Pipes**
Comunicação direta entre processos.

---

## 📋 Pré-requisitos

### Sistema Python
```bash
# 1. Python 3.8+ instalado
python --version

# 2. Dependências instaladas
cd python/
pip install -r requirements.txt

# 3. Configurar variável de ambiente
# Criar arquivo .env com:
COHERE_API_KEY=sua_chave_aqui
```

### Sistema C#
```xml
<!-- NuGet Packages recomendados -->
<PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
<PackageReference Include="System.Diagnostics.Process" Version="4.3.0" />
```

---

## 🔧 Implementação C# - Método 1: Processo

### Classe de Integração Principal

```csharp
using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using Newtonsoft.Json;

public class PythonAnalysisService
{
    private readonly string _pythonPath;
    private readonly string _scriptPath;
    
    public PythonAnalysisService(string pythonPath, string scriptPath)
    {
        _pythonPath = pythonPath ?? throw new ArgumentNullException(nameof(pythonPath));
        _scriptPath = scriptPath ?? throw new ArgumentNullException(nameof(scriptPath));
    }
    
    /// <summary>
    /// Executa análise completa usando o sistema Python
    /// </summary>
    /// <param name="searchQuery">Termo de busca para análise</param>
    /// <returns>Resultado da análise em formato estruturado</returns>
    public async Task<AnalysisResult> ExecuteAnalysisAsync(string searchQuery)
    {
        try
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = _pythonPath,
                Arguments = $"\"{_scriptPath}\" \"{searchQuery}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                WorkingDirectory = Path.GetDirectoryName(_scriptPath)
            };
            
            using var process = new Process { StartInfo = processInfo };
            
            var outputTask = Task.Run(() => process.StandardOutput.ReadToEnd());
            var errorTask = Task.Run(() => process.StandardError.ReadToEnd());
            
            process.Start();
            
            var output = await outputTask;
            var error = await errorTask;
            
            await process.WaitForExitAsync();
            
            if (process.ExitCode != 0)
            {
                throw new InvalidOperationException($"Python process failed: {error}");
            }
            
            return ParseAnalysisOutput(output);
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Failed to execute Python analysis: {ex.Message}", ex);
        }
    }
    
    private AnalysisResult ParseAnalysisOutput(string output)
    {
        // Processa a saída do Python e converte para objeto C#
        var lines = output.Split('\n', StringSplitOptions.RemoveEmptyEntries);
        
        return new AnalysisResult
        {
            Status = "Success",
            SearchTerms = ExtractSearchTerms(lines),
            CollectedUrls = ExtractUrls(lines),
            SynthesisFile = ExtractSynthesisFile(lines),
            ProcessingStats = ExtractStats(lines)
        };
    }
    
    // Métodos auxiliares de extração
    private string[] ExtractSearchTerms(string[] lines) { /* implementação */ }
    private string[] ExtractUrls(string[] lines) { /* implementação */ }
    private string ExtractSynthesisFile(string[] lines) { /* implementação */ }
    private ProcessingStats ExtractStats(string[] lines) { /* implementação */ }
}

// Modelos de dados
public class AnalysisResult
{
    public string Status { get; set; }
    public string[] SearchTerms { get; set; }
    public string[] CollectedUrls { get; set; }
    public string SynthesisFile { get; set; }
    public ProcessingStats ProcessingStats { get; set; }
}

public class ProcessingStats
{
    public int TermsProcessed { get; set; }
    public int UrlsCollected { get; set; }
    public bool MultiAgentCompleted { get; set; }
    public TimeSpan ProcessingTime { get; set; }
}
```

### Script Python Modificado para C#

```python
# analysis_service.py
import sys
import json
import os
from main import search

def main():
    """Ponto de entrada para integração C#"""
    if len(sys.argv) != 2:
        print("Uso: python analysis_service.py <search_query>")
        sys.exit(1)
    
    search_query = sys.argv[1]
    
    try:
        # Executa análise
        terms, pages, data = search(search_query)
        
        # Retorna resultado estruturado para C#
        result = {
            "status": "success",
            "search_terms": terms,
            "collected_urls": sum(len(urls) for urls in pages.values()),
            "data_file": f"dados_{search_query.replace(' ', '_').lower()}.json",
            "synthesis_files": {
                "partial": f"resumos_parciais_{search_query.replace(' ', '_').lower()}.txt",
                "final": f"sintese_final_{search_query.replace(' ', '_').lower()}.txt"
            },
            "stats": {
                "terms_processed": len(terms),
                "urls_collected": sum(len(urls) for urls in pages.values()),
                "multi_agent_completed": True
            }
        }
        
        # Output estruturado para C#
        print("=== PYTHON_OUTPUT_START ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("=== PYTHON_OUTPUT_END ===")
        
    except Exception as e:
        error_result = {
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }
        print("=== PYTHON_ERROR_START ===")
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        print("=== PYTHON_ERROR_END ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 🔧 Implementação C# - Método 2: Arquivos

### Classe para Integração via Arquivos

```csharp
public class FileBasedPythonService
{
    private readonly string _inputPath;
    private readonly string _outputPath;
    private readonly string _pythonExecutor;
    
    public FileBasedPythonService(string workingDirectory, string pythonExecutor = "python")
    {
        _inputPath = Path.Combine(workingDirectory, "input.json");
        _outputPath = Path.Combine(workingDirectory, "output.json");
        _pythonExecutor = pythonExecutor;
    }
    
    public async Task<AnalysisResult> ProcessAsync(AnalysisRequest request)
    {
        // 1. Escreve requisição para arquivo
        await WriteRequestAsync(request);
        
        // 2. Executa script Python
        await ExecutePythonScriptAsync();
        
        // 3. Lê resultado do arquivo
        return await ReadResultAsync();
    }
    
    private async Task WriteRequestAsync(AnalysisRequest request)
    {
        var json = JsonConvert.SerializeObject(request, Formatting.Indented);
        await File.WriteAllTextAsync(_inputPath, json);
    }
    
    private async Task ExecutePythonScriptAsync()
    {
        var processInfo = new ProcessStartInfo
        {
            FileName = _pythonExecutor,
            Arguments = "file_processor.py",
            UseShellExecute = false,
            CreateNoWindow = true,
            WorkingDirectory = Path.GetDirectoryName(_inputPath)
        };
        
        using var process = Process.Start(processInfo);
        await process.WaitForExitAsync();
        
        if (process.ExitCode != 0)
        {
            throw new InvalidOperationException("Python processing failed");
        }
    }
    
    private async Task<AnalysisResult> ReadResultAsync()
    {
        if (!File.Exists(_outputPath))
        {
            throw new FileNotFoundException("Output file not found");
        }
        
        var json = await File.ReadAllTextAsync(_outputPath);
        return JsonConvert.DeserializeObject<AnalysisResult>(json);
    }
}

public class AnalysisRequest
{
    public string SearchQuery { get; set; }
    public Dictionary<string, object> Options { get; set; }
    public DateTime RequestTime { get; set; }
}
```

---

## ⚙️ Configuração de Ambiente

### 1. Estrutura de Diretórios

```
projeto/
├── csharp/
│   ├── izaai-utils/
│   │   ├── Program.cs
│   │   ├── Services/
│   │   │   ├── PythonAnalysisService.cs
│   │   │   └── FileBasedPythonService.cs
│   │   └── Models/
│   │       ├── AnalysisResult.cs
│   │       └── AnalysisRequest.cs
│   └── izaai-utils.csproj
└── python/
    ├── main.py
    ├── analysis_service.py
    ├── file_processor.py
    ├── core/
    ├── utils/
    └── requirements.txt
```

### 2. Variáveis de Ambiente C#

```csharp
// appsettings.json
{
  "PythonIntegration": {
    "PythonExecutable": "python",
    "ScriptPath": "..\\python\\analysis_service.py",
    "WorkingDirectory": "..\\python",
    "TimeoutSeconds": 300,
    "EnableLogging": true
  },
  "FileIntegration": {
    "InputDirectory": "..\\shared\\input",
    "OutputDirectory": "..\\shared\\output",
    "CleanupAfterProcess": true
  }
}

// Configuration class
public class PythonConfig
{
    public string PythonExecutable { get; set; } = "python";
    public string ScriptPath { get; set; }
    public string WorkingDirectory { get; set; }
    public int TimeoutSeconds { get; set; } = 300;
    public bool EnableLogging { get; set; } = true;
}
```

### 3. Injeção de Dependência

```csharp
// Program.cs ou Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    services.Configure<PythonConfig>(Configuration.GetSection("PythonIntegration"));
    services.AddScoped<IPythonAnalysisService, PythonAnalysisService>();
    services.AddScoped<IFileBasedPythonService, FileBasedPythonService>();
}
```

---

## 📝 Exemplos de Uso

### Console Application

```csharp
class Program
{
    static async Task Main(string[] args)
    {
        var config = new PythonConfig
        {
            PythonExecutable = "python",
            ScriptPath = @"..\python\analysis_service.py",
            WorkingDirectory = @"..\python"
        };
        
        var service = new PythonAnalysisService(
            config.PythonExecutable, 
            config.ScriptPath
        );
        
        try
        {
            Console.WriteLine("Iniciando análise...");
            
            var result = await service.ExecuteAnalysisAsync("Python programação");
            
            Console.WriteLine($"Status: {result.Status}");
            Console.WriteLine($"Termos processados: {result.ProcessingStats.TermsProcessed}");
            Console.WriteLine($"URLs coletadas: {result.ProcessingStats.UrlsCollected}");
            Console.WriteLine($"Arquivo de síntese: {result.SynthesisFile}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Erro: {ex.Message}");
        }
    }
}
```

### Windows Forms Application

```csharp
public partial class AnalysisForm : Form
{
    private readonly IPythonAnalysisService _analysisService;
    
    public AnalysisForm(IPythonAnalysisService analysisService)
    {
        InitializeComponent();
        _analysisService = analysisService;
    }
    
    private async void btnAnalyze_Click(object sender, EventArgs e)
    {
        try
        {
            btnAnalyze.Enabled = false;
            progressBar.Visible = true;
            lblStatus.Text = "Processando...";
            
            var searchQuery = txtSearchQuery.Text;
            var result = await _analysisService.ExecuteAnalysisAsync(searchQuery);
            
            // Atualiza UI com resultados
            DisplayResults(result);
            
            lblStatus.Text = "Análise concluída!";
        }
        catch (Exception ex)
        {
            MessageBox.Show($"Erro na análise: {ex.Message}", "Erro", 
                          MessageBoxButtons.OK, MessageBoxIcon.Error);
            lblStatus.Text = "Erro na análise";
        }
        finally
        {
            btnAnalyze.Enabled = true;
            progressBar.Visible = false;
        }
    }
    
    private void DisplayResults(AnalysisResult result)
    {
        listBoxTerms.Items.Clear();
        foreach (var term in result.SearchTerms)
        {
            listBoxTerms.Items.Add(term);
        }
        
        lblStats.Text = $"Processados: {result.ProcessingStats.TermsProcessed} termos, " +
                       $"{result.ProcessingStats.UrlsCollected} URLs";
        
        // Abrir arquivo de síntese se existir
        if (File.Exists(result.SynthesisFile))
        {
            txtSynthesis.Text = File.ReadAllText(result.SynthesisFile);
        }
    }
}
```

---

## 🔒 Tratamento de Erros

### Classe de Exceções Customizadas

```csharp
public class PythonIntegrationException : Exception
{
    public string PythonError { get; }
    public int ExitCode { get; }
    
    public PythonIntegrationException(string message, string pythonError = null, int exitCode = -1) 
        : base(message)
    {
        PythonError = pythonError;
        ExitCode = exitCode;
    }
}

public static class ErrorHandler
{
    public static void HandlePythonError(string error, int exitCode)
    {
        var errorMessage = exitCode switch
        {
            1 => "Erro de configuração da API Cohere",
            2 => "Erro de conectividade de rede",
            3 => "Erro de processamento de dados",
            _ => "Erro desconhecido no processo Python"
        };
        
        throw new PythonIntegrationException(errorMessage, error, exitCode);
    }
}
```

---

## 📊 Monitoramento e Logs

### Sistema de Logging

```csharp
public class PythonAnalysisService
{
    private readonly ILogger<PythonAnalysisService> _logger;
    
    public PythonAnalysisService(ILogger<PythonAnalysisService> logger, /* outros params */)
    {
        _logger = logger;
    }
    
    public async Task<AnalysisResult> ExecuteAnalysisAsync(string searchQuery)
    {
        _logger.LogInformation("Iniciando análise para: {SearchQuery}", searchQuery);
        
        var stopwatch = Stopwatch.StartNew();
        
        try
        {
            var result = await InternalExecuteAsync(searchQuery);
            
            _logger.LogInformation("Análise concluída em {Duration}ms. Termos: {Terms}, URLs: {Urls}",
                stopwatch.ElapsedMilliseconds, 
                result.ProcessingStats.TermsProcessed,
                result.ProcessingStats.UrlsCollected);
            
            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Falha na análise para: {SearchQuery}", searchQuery);
            throw;
        }
        finally
        {
            stopwatch.Stop();
        }
    }
}
```

---

## 🚀 Deploy e Distribuição

### 1. Build Script PowerShell

```powershell
# build_and_deploy.ps1

param(
    [string]$Environment = "Development",
    [string]$OutputPath = ".\dist"
)

Write-Host "=== BUILD E DEPLOY SISTEMA INTEGRADO ===" -ForegroundColor Green

# 1. Build aplicação C#
Write-Host "Building C# application..." -ForegroundColor Yellow
dotnet build .\izaai-utils\izaai-utils.csproj --configuration Release --output $OutputPath\csharp

# 2. Preparar ambiente Python
Write-Host "Preparing Python environment..." -ForegroundColor Yellow
Copy-Item .\python\* $OutputPath\python\ -Recurse -Force

# 3. Instalar dependências Python
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
Set-Location $OutputPath\python
pip install -r requirements.txt --target .\lib

# 4. Criar scripts de inicialização
Write-Host "Creating startup scripts..." -ForegroundColor Yellow
@"
@echo off
cd /d %~dp0
python.exe analysis_service.py %*
"@ | Out-File -FilePath "$OutputPath\run_analysis.bat" -Encoding ASCII

# 5. Gerar documentação
Write-Host "Generating documentation..." -ForegroundColor Yellow
# ... comandos para gerar docs

Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Output directory: $OutputPath" -ForegroundColor Cyan
```

### 2. Dockerfile para Containerização

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/dotnet/runtime:8.0 AS base
WORKDIR /app

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy and restore C# project
COPY ["izaai-utils/izaai-utils.csproj", "izaai-utils/"]
RUN dotnet restore "izaai-utils/izaai-utils.csproj"

# Copy source code
COPY . .
WORKDIR "/src/izaai-utils"
RUN dotnet build "izaai-utils.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "izaai-utils.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

# Copy Python scripts
COPY python/ ./python/
WORKDIR /app/python
RUN pip3 install -r requirements.txt

WORKDIR /app
ENTRYPOINT ["dotnet", "izaai-utils.dll"]
```

---

## 🔍 Troubleshooting

### Problemas Comuns

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| `Python not found` | Python não instalado ou não no PATH | Verificar instalação e configurar PATH |
| `Module not found` | Dependências não instaladas | Executar `pip install -r requirements.txt` |
| `API Key error` | COHERE_API_KEY não configurada | Criar arquivo .env com a chave |
| `Timeout error` | Processamento muito longo | Aumentar timeout ou otimizar consulta |
| `File not found` | Caminhos incorretos | Verificar paths relativos/absolutos |

### Diagnóstico

```csharp
public class DiagnosticService
{
    public async Task<DiagnosticResult> RunDiagnosticsAsync()
    {
        var result = new DiagnosticResult();
        
        // Verificar Python
        result.PythonAvailable = await CheckPythonAsync();
        
        // Verificar dependências
        result.DependenciesInstalled = await CheckDependenciesAsync();
        
        // Verificar API Key
        result.ApiKeyConfigured = CheckApiKey();
        
        // Verificar arquivos
        result.ScriptsExist = CheckScriptFiles();
        
        return result;
    }
}
```

---

## 📚 Referências e Recursos

### Documentação Adicional
- [Documentação Python Integration](./docs/python-integration.md)
- [API Reference](./docs/api-reference.md)
- [Exemplos Completos](./examples/)

### Links Úteis
- [Cohere API Documentation](https://docs.cohere.ai/)
- [.NET Process Class](https://docs.microsoft.com/en-us/dotnet/api/system.diagnostics.process)
- [Python subprocess](https://docs.python.org/3/library/subprocess.html)

---

## 🤝 Suporte

Para suporte e dúvidas:
1. Consulte a seção de Troubleshooting
2. Verifique os logs de erro
3. Execute o diagnóstico do sistema
4. Abra uma issue no repositório

---

**Versão do Documento:** 1.0  
**Última Atualização:** Agosto 2025  
**Autor:** Marco
