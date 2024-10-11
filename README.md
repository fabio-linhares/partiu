<h1 style="text-align: center;">Partiu - Aplicativo de Pacotes de Viagens Para Quem Quer Escapar das Visitas Indesejadas</h1>


![partiu_image](./static/images/.backgound/capa1.png)

<div style="text-align: right;">
Imagem criada por Inteligência Artificial.
</div>


## Visão Geral

"Partiu" é um aplicativo web inovador desenvolvido com Streamlit, projetado para simplificar a busca e reserva de pacotes de viagens acessíveis. Este projeto faz parte de um estudo acadêmico alinhado ao Objetivo de Desenvolvimento Sustentável 8 (ODS 8) da ONU: Trabalho Decente e Crescimento Econômico.

O aplicativo visa resolver a dificuldade que muitas pessoas enfrentam ao procurar pacotes de viagens que se ajustem ao seu orçamento e preferências, promovendo simultaneamente o turismo sustentável e apoiando economias locais.

## Objetivos

- Facilitar a busca e reserva de pacotes de viagens acessíveis
- Aumentar o número de viagens realizadas pelos usuários
- Promover o turismo em regiões menos conhecidas
- Contribuir para o crescimento econômico local através do turismo sustentável
- Melhorar a experiência do usuário na pesquisa e planejamento de viagens

## Principais Pacotes Utilizados

O projeto utiliza uma série de pacotes para diversas finalidades, organizados da seguinte forma:

### 1. Desenvolvimento de Aplicações Web e Frameworks
- **streamlit** (1.38.0): Principal pacote para construção de aplicações web interativas baseadas em dados.
- **streamlit-aggrid** (1.0.5): Componente adicional para incorporar tabelas interativas no Streamlit.
- **streamlit-folium** (0.18.0): Integração do Streamlit com o Folium para visualização de mapas.

### 2. Análise de Dados
- **numpy** (1.26.4): Biblioteca fundamental para computação numérica.
- **pandas** (2.2.3): Manipulação e análise de dados em formato de tabelas.
- **scipy** (1.12.0): Biblioteca para computação científica.
- **scikit-learn** (1.4.1.post1): Pacote para modelagem de aprendizado de máquina.
- **seaborn** (0.13.2): Visualizações estatísticas.
- **matplotlib** (3.8.3): Biblioteca de gráficos e visualizações.
- **altair** (4.2.2): Biblioteca para visualização de dados declarativa.
- **joblib** (1.4.2): Ferramenta para serialização e execução paralela de jobs.
- **plotly** (5.20.0): Criação de gráficos interativos.
- **folium** (0.15.1): Visualização de dados geoespaciais.
- **geopandas** (0.14.3): Manipulação de dados geoespaciais.

### 3. Web Scraping e HTTP
- **Scrapy** (2.11.2): Framework de web scraping.
- **beautifulsoup4** (4.12.3): Extração de dados de arquivos HTML e XML.
- **requests** (2.31.0): Biblioteca para requisições HTTP.
- **aiohttp** (3.10.6): Cliente HTTP assíncrono.
- **httpx** (0.27.2): Alternativa ao `requests`, com suporte a requisições HTTP assíncronas.

### 4. Aprendizado de Máquina e Ciência de Dados
- **numba** (0.60.0): Otimização de código numérico em Python, utilizando compilação JIT.
- **onnxruntime** (1.19.2): Para executar modelos treinados em ONNX.
- **pyarrow** (17.0.0): Manipulação de dados tabulares e integração com armazenamento de dados.
- **rembg** (2.0.59): Remoção de fundo de imagens utilizando aprendizado de máquina.

### 5. Visualização de Dados
- **mplsoccer** (1.4.0): Visualização de dados esportivos.
- **shapely** (2.0.6): Manipulação e análise de formas geométricas.
- **wordcloud** (1.9.3): Geração de nuvens de palavras.

### 6. Testes e Qualidade do Código
- **pytest** (8.1.1): Framework de testes.
- **flake8** (7.0.0): Verificador de estilo de código Python.
- **black** (24.3.0): Formatador automático de código Python.

### 7. Segurança e Criptografia
- **cryptography** (43.0.1): Implementações de protocolos criptográficos.

Esses pacotes compõem o núcleo funcional do projeto, cobrindo desde a manipulação de dados até a criação de interfaces web interativas e automação de tarefas, como web scraping.

## Estrutura do Repositório

```bash
partiu/
├── app/
│   ├── main.py
│   ├── components/
│   ├── pages/
│   └── utils/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── business_understanding/
│   └── data_understanding/
├── notebooks/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── visualization/
├── .streamlit/
│   └── secrets.toml
├── tests/
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```

### Justificativa: o tal do CRISP-DM

- **`app/`**: Diretório que contém o código principal da aplicação, que pode ser uma interface interativa construída com o Streamlit.
     - **`main.py`**: Arquivo de entrada principal da aplicação.
     - **`components/`**: Para armazenar componentes reutilizáveis da interface do usuário, como widgets personalizados ou layouts.
     - **`pages/`**: Organização para múltiplas páginas da aplicação, facilitando o gerenciamento de diferentes seções ou visões da interface.
     - **`utils/`**: Funções utilitárias gerais, usadas em diferentes partes da aplicação para abstrair funcionalidades recorrentes.

- **`data/`**:
  - **`raw/`**: Diretório destinado a armazenar os dados brutos, não tratados, como recebidos de fontes externas.
  - **`processed/`**: Armazena os dados após serem limpos, transformados e preparados para uso no projeto.
  
- **`docs/`**:
  - **`business_understanding/`**: Contém a documentação relacionada ao entendimento do problema de negócio, os objetivos gerais do projeto e as premissas adotadas.
  - **`data_understanding/`**: Relatórios e análises que explicam a origem, a estrutura e a qualidade dos dados, além de insights iniciais sobre os dados usados.

- **`notebooks/`**: Armazena notebooks Jupyter para exploração de dados, análise inicial e desenvolvimento de protótipos, permitindo fácil compartilhamento e documentação de processos exploratórios.

- **`src/`**: Diretório principal de código-fonte modular do projeto.
  - **`data/`**: Scripts para a coleta, limpeza e transformação de dados.
  - **`features/`**: Implementação de funções para a extração e engenharia de features, fundamentais para o treinamento de modelos.
  - **`models/`**: Implementações dos algoritmos de machine learning, incluindo treinamento, validação e avaliação dos modelos.
  - **`visualization/`**: Funções e scripts para gerar gráficos e visualizações, que auxiliam na análise e interpretação dos dados.

- **`.streamlit/`**:
  - **`secrets.toml`**: Arquivo de configuração que armazena segredos e credenciais, como chaves de API, de forma segura para uso dentro da aplicação Streamlit.

- **`tests/`**: Diretório dedicado a testes automatizados, incluindo testes unitários e de integração, para garantir a robustez e qualidade do código à medida que ele evolui.

- **`.gitignore`**: Arquivo que define quais arquivos e diretórios devem ser ignorados pelo sistema de controle de versão git, como dados sensíveis ou artefatos gerados automaticamente.

- **`README.md`**: Documentação principal do projeto, onde são descritas as instruções de instalação, uso, e uma visão geral do propósito e estrutura do projeto.

- **`requirements.txt`**: Lista de dependências de bibliotecas e pacotes Python necessários para rodar o projeto, facilitando a configuração do ambiente.

- **`setup.py`**: Arquivo de configuração utilizado para empacotar o projeto como um pacote Python, permitindo sua fácil distribuição e instalação.


Nossa ideia com essa organização, além de respeitar as diretrizes do **CRISP-DM**, é fornecer uma organização clara e modular para o projeto, separando claramente a aplicação web (**`app/`**), o processamento de dados e modelagem (**`src/`**), documentação (**`docs/`**), e testes (**`tests/`**), o que, a nosso ver, segue as boas práticas de desenvolvimento de software em ciência de dados, permitindo fácil manutenção, colaboração e escalabilidade do projeto.



## Instalação e Configuração

1. Clone o repositório:

   `git clone https://github.com/fabio-linhares/partiu.git`

   `cd partiu`

2. Crie um ambiente virtual:

   `python -m venv venv`

   `source venv/bin/activate  # No Windows use venv\Scripts\activate`

3. Instale as dependências:

   `pip install -r requirements.txt`

## Executando a Aplicação

Para iniciar o aplicativo Streamlit, execute:

   `streamlit run app/main.py`

Acesse o aplicativo em seu navegador através do endereço: `http://localhost:8501`

## Funcionalidades Principais

- Busca de pacotes de viagens com filtros por preço, destino e datas
- Visualização detalhada de pacotes de viagens
- Recomendações personalizadas baseadas nas preferências do usuário
- Análise de tendências de viagens e destinos populares
- Interface responsiva para uso em dispositivos móveis e desktop

## Contribuição

Contribuições são bem-vindas! Por favor, leia o arquivo CONTRIBUTING.md para detalhes sobre nosso código de conduta e o processo para enviar pull requests.

## Licença

Este projeto está licenciado sob a Licença GPL V.3 - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.


<h3 style="text-align: center;">Contato</h3>
<p style="text-align: center; font-size: smaller;">
    Fábio Linhares - <a href="mailto:fabio.linhares@al.infnet.edu.br">fabio.linhares@al.infnet.edu.br</a><br>
    Link do Projeto: <a href="https://github.com/fabio-linhares/partiu">https://github.com/fabio-linhares/partiu</a>
</p>


---
<p style="text-align: center; font-size: smaller;">
Desenvolvido como parte do curso de Ciência de Dados Aplicada no Instituto Infnet.
</p>
