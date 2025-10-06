# 📊 Conversor XML para XLSX - Sistema Profissional

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Sistema completo e modular para conversão de **Notas Fiscais Eletrônicas (XMLs)** em planilhas **Excel formatadas**, desenvolvido especialmente para escritórios de contabilidade.

## 🎯 Principais Funcionalidades

### ✨ Upload e Processamento
- 📤 **Upload múltiplo** de arquivos XML
- 📦 **Suporte a ZIP** com extração automática
- ⚡ **Processamento em lote** de até 1000 XMLs
- 🔍 **Validação automática** de formato e tamanho

### 🎨 Formatação Profissional
- 💰 **Valores monetários** formatados (R$ #.##0,00)
- 📅 **Datas** no padrão brasileiro (DD/MM/YYYY)
- 🆔 **CPF/CNPJ** formatados automaticamente
- 🎨 **Excel estilizado** com cabeçalhos coloridos e bordas

### 📊 Dashboard Interativo
- 📈 **Gráfico de evolução** temporal dos valores
- 🏆 **Ranking** dos principais emitentes
- 📊 **Histograma** de distribuição de valores
- 📋 **Tabela interativa** com todos os dados

### 🔧 Filtros Avançados
- 📆 Filtro por **período** (data inicial e final)
- 💵 Filtro por **faixa de valores** (mínimo e máximo)
- 🔍 Busca por **texto** em qualquer coluna
- 🗑️ **Remoção de duplicatas** automática

---

## 🏗️ Arquitetura do Projeto

```
xml-to-xlsx-converter/
│
├── 📄 app.py                      # Aplicação principal Streamlit
├── ⚙️ config.py                   # Configurações globais
├── 📋 requirements.txt            # Dependências Python
├── 📖 README.md                   # Este arquivo
├── 🚫 .gitignore                  # Arquivos ignorados
│
├── 📁 modules/                    # Módulos principais
│   ├── __init__.py
│   ├── 📤 upload_handler.py       # Gerenciamento de uploads
│   ├── 🔄 xml_parser.py           # Conversão XML → DataFrame
│   ├── 🔍 data_filter.py          # Aplicação de filtros
│   ├── ✨ data_formatter.py       # Formatação de dados
│   ├── 📊 excel_exporter.py       # Geração de Excel
│   └── 📈 dashboard_builder.py    # Construção de dashboards
│
├── 📁 utils/                      # Utilitários
│   ├── __init__.py
│   ├── 📝 logger.py               # Sistema de logging
│   ├── ✅ validators.py           # Validações
│   └── 🛠️ helpers.py              # Funções auxiliares
│
└── 📁 temp/                       # Arquivos temporários
```

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Local

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/xml-to-xlsx-converter.git
cd xml-to-xlsx-converter

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute a aplicação
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

---

## ☁️ Deploy no Streamlit Cloud

### Passo a Passo

1. **Faça push do código para o GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/seu-usuario/xml-to-xlsx-converter.git
   git push -u origin main
   ```

2. **Acesse** [share.streamlit.io](https://share.streamlit.io)

3. **Conecte seu repositório GitHub**

4. **Configure o deploy:**
   - Repository: `seu-usuario/xml-to-xlsx-converter`
   - Branch: `main`
   - Main file: `app.py`

5. **Clique em "Deploy"** e aguarde (2-5 minutos)

6. **Pronto!** Sua aplicação estará disponível em uma URL pública

---

## 📖 Como Usar

### 1️⃣ Upload de Arquivos

- Arraste arquivos **XML** ou **ZIP** para a área de upload
- Ou clique para selecionar do seu computador
- Aguarde a validação automática

### 2️⃣ Configuração (Sidebar)

**Processamento:**
- ☑️ Remover duplicatas
- ☑️ Incluir aba de resumo no Excel

**Filtros (Opcional):**
- 📅 Período: Define data inicial e final
- 💰 Valores: Define valor mínimo e máximo

### 3️⃣ Processamento

- Clique em **"🚀 Processar Arquivos"**
- Acompanhe o progresso em tempo real
- Sistema processa: Extração → Parse → Filtros → Formatação

### 4️⃣ Visualização

Explore as abas:
- **📈 Evolução:** Valores ao longo do tempo
- **🏆 Top Emitentes:** Principais fornecedores
- **📊 Distribuição:** Histograma de valores
- **📋 Dados:** Tabela completa

### 5️⃣ Exportação

- Defina o nome do arquivo
- Clique em **"📥 Baixar Excel"**
- Arquivo será baixado com formatação profissional

---

## 🔧 Personalização

### Adicionar Novos Campos XML

Edite `config.py`:

```python
DEFAULT_XML_FIELDS = {
    'Seu Novo Campo': ['caminho.no.xml', 'caminho.alternativo'],
    'Outro Campo': ['outro.caminho'],
    # ... campos existentes
}
```

### Alterar Cores do Excel

Edite `config.py`:

```python
EXCEL_CONFIG = {
    'header_style': {
        'bg_color': '#FF5733',  # Nova cor de fundo
        'font_color': '#FFFFFF'  # Cor da fonte
    }
}
```

### Adicionar Novo Gráfico

Em `modules/dashboard_builder.py`:

```python
def create_custom_chart(self, df: pd.DataFrame) -> go.Figure:
    """Seu gráfico personalizado"""
    fig = px.scatter(df, x='campo1', y='campo2')
    return fig
```

---

## 📦 Dependências

| Biblioteca | Versão | Função |
|-----------|--------|---------|
| streamlit | 1.31.0 | Interface web |
| pandas | 2.2.0 | Manipulação de dados |
| openpyxl | 3.1.2 | Leitura/escrita Excel |
| xmltodict | 0.13.0 | Parse de XML |
| plotly | 5.18.0 | Gráficos interativos |
| python-dateutil | 2.8.2 | Manipulação de datas |

---

## 🎓 Exemplos de Uso

### Exemplo 1: Conversão Básica
```
1. Upload de 50 XMLs
2. Clicar em "Processar"
3. Baixar Excel formatado
```

### Exemplo 2: Análise de Fornecedores
```
1. Upload dos XMLs do trimestre
2. Visualizar aba "Top Emitentes"
3. Exportar com resumo
```

### Exemplo 3: Filtro por Período
```
1. Upload de XMLs do ano
2. Ativar filtros
3. Definir: 01/01/2025 até 31/03/2025
4. Processar e exportar
```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"
**Solução:** Instale as dependências
```bash
pip install -r requirements.txt
```

### Erro: "File not found"
**Solução:** Verifique a estrutura de pastas e execute do diretório raiz

### Aplicação Lenta
**Soluções:**
- Processe menos arquivos por vez (máx. 1000)
- Desative gráficos não utilizados
- Use filtros para reduzir dados

### XML não Reconhecido
**Solução:** Ajuste o mapeamento em `config.py` para seu tipo de XML

---

## 📊 Tipos de XML Suportados

### Padrão: NFe (Nota Fiscal Eletrônica)
Sistema configurado por padrão para NFe

### Outros Tipos Fiscais
Pode ser adaptado para:
- **NFCe** - Nota Fiscal Consumidor
- **CTe** - Conhecimento de Transporte
- **MDFe** - Manifesto Eletrônico

**Como adaptar:** Edite os campos em `config.py` conforme a estrutura do seu XML

---

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📝 Roadmap

### Próximas Funcionalidades
- [ ] Suporte a múltiplos tipos de XML simultâneos
- [ ] Exportação para PDF
- [ ] Integração com banco de dados
- [ ] Histórico de conversões
- [ ] API REST para integração
- [ ] Agendamento de processamentos
- [ ] Notificações por email

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

Desenvolvido para escritórios de contabilidade

**Contato:**
- 📧 Email: seuemail@exemplo.com
- 💼 LinkedIn: [seu-perfil](https://linkedin.com/in/seu-perfil)
- 🌐 Website: [seusite.com](https://seusite.com)

---

## 🙏 Agradecimentos

- [Streamlit](https://streamlit.io) - Framework incrível para apps de dados
- [Plotly](https://plotly.com) - Biblioteca de visualização
- Comunidade Python

---

## 📞 Suporte

Encontrou um bug ou tem uma sugestão?

- 🐛 **Bugs:** Abra uma [issue](https://github.com/seu-usuario/xml-to-xlsx-converter/issues)
- 💡 **Sugestões:** Use as [discussions](https://github.com/seu-usuario/xml-to-xlsx-converter/discussions)
- 📧 **Email:** suporte@seudominio.com

---

## ⭐ Se este projeto foi útil para você, considere dar uma estrela!

<div align="center">

### 🚀 Desenvolvido com ❤️ para contadores

**[⬆ Voltar ao topo](#-conversor-xml-para-xlsx---sistema-profissional)**

</div>