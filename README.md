<h1 style="text-align: center;">Partiu - Aplicativo de Pacotes de Viagens Para Quem Quer Escapar das Visitas Indesejadas</h1>


![partiu_image](./images/.backgound/capa1.png)

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

O projeto utiliza uma série de pacotes para diferentes finalidades, organizados da seguinte forma:

### 1. Desenvolvimento de Aplicações Web e Frameworks
- **streamlit**: Principal pacote para construção de aplicações web interativas baseadas em dados.
- **fastapi**: Framework leve para construção de APIs web.
- **uvicorn**: Servidor ASGI rápido utilizado para rodar aplicações FastAPI.

### 2. Análise de Dados e Visualização
- **numpy**: Biblioteca fundamental para computação numérica.
- **pandas**: Manipulação e análise de dados em formato de tabelas.
- **matplotlib**: Biblioteca de gráficos e visualizações.
- **plotly**: Criação de gráficos interativos.

### 3. Manipulação de Configurações e Banco de Dados
- **toml**: Utilizado para leitura de arquivos de configuração, como `secrets.toml`.
- **pymongo**: Interface Python para o MongoDB, permitindo manipulação de bancos de dados NoSQL.

### 4. Modelagem de Dados e Validação
- **pydantic**: Utilizado para validação de dados e definição de modelos no FastAPI.

### 5. Web Scraping e HTTP
- **requests**: Biblioteca para requisições HTTP, facilitando a comunicação com APIs.

Esses pacotes compõem o núcleo funcional do projeto, cobrindo desde a criação de APIs web até a manipulação de dados e interações com bancos de dados NoSQL.

## Estrutura do Repositório

```bash
partiu/
├── app/
│   ├── api.py
│   ├── app.py
│   ├── components/
│   ├── config/
│   ├── pages/
│   └── utils/
├── data/
│   ├── external/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── images/
├── notebooks/
│   ├── exploratory/
│   └── final/
├── tests/
├── LICENSE
├── README.md
├── setup.py
└── requirements.txt


### Justificativa: o tal do CRISP-DM

- **`app/`**: Diretório que contém o código principal da aplicação.
  - **`api.py`**: Arquivo que define as rotas e funções da API construída com FastAPI.
  - **`app.py`**: Principal arquivo da aplicação Streamlit.
  - **`components/`**: Armazena componentes reutilizáveis da interface do usuário.
  - **`config/`**: Armazena variáveis de ambiente para diferentes ambientes (dev, val, prod).
  - **`pages/`**: Organização para as diferentes páginas da aplicação.
  - **`utils/`**: Funções utilitárias como manipulação de dados e interação com o banco de dados.

- **`data/`**:
  - **`raw/`**: Dados brutos.
  - **`processed/`**: Dados processados.
  - **`interim/`**: Armazena dados e arquivos intermediários, como documentação do projeto.

- **`images/`**: Diretório para armazenar imagens utilizadas no projeto.

- **`notebooks/`**: Notebooks Jupyter para exploração de dados e análise.

- **`tests/`**: Diretório dedicado a testes automatizados.

- **`LICENSE`**, **`README.md`**, **`setup.py`**: Documentação do projeto e arquivos de configuração.

Essa organização segue as diretrizes do **CRISP-DM** e as boas práticas de desenvolvimento de software, separando de forma clara as funções da aplicação e mantendo a modularidade para facilitar a colaboração e manutenção.

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
