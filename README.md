# GovBuster
## Plataforma de Transparência e Análise de Processos para Candidatos Políticos
GovBuster é uma plataforma desenvolvida para promover a transparência e a conscientização política, fornecendo aos eleitores informações detalhadas sobre candidatos e processos judiciais relacionados. O sistema permite que o usuário consulte dados de candidatos, partidos e processos associados, utilizando informações públicas e ferramentas de inteligência artificial.

### 1. Consulta de Dados e Processos de Candidatos
GovBuster facilita o acesso aos dados de candidatos por meio de arquivos CSV fornecidos pelo governo. A plataforma permite consultas rápidas sobre:

- Partidos e coligações,
- Processos judiciais associados ao candidato,
- Imagens e informações complementares.

A consulta é feita em uma base local, utilizando CSVs, e pode ser complementada com a API do Escavador, que retorna informações atualizadas sobre processos e movimentações.

### 2. Controle de Requisições e Segurança
Para garantir a estabilidade do sistema, implementamos um Controle de Taxa de Requisições:

- Cada IP tem um limite de requisições por hora para evitar sobrecarga e abusos.
- Requisições além do limite recebem uma mensagem de erro indicando a taxa excedida.

### Tecnologias Utilizadas:
- Flask para o desenvolvimento do backend e das APIs,
- Python para manipulação de dados e integração com a API do Escavador,
- Escavador API para obter dados de processos judiciais e movimentações,
- Pandas para manipulação dos arquivos CSV,
- HTML, CSS e JavaScript para o frontend.

### Estrutura de Pastas:
- Template: Contém os arquivos HTML para as páginas da aplicação.
- Static: Contém os arquivos CSS e JavaScript para estilização e funcionalidades.
- Static/img: Armazena imagens dos candidatos. Se não houver foto de um candidato, a aplicação utiliza uma imagem padrão.

### Fluxo de Funcionamento:
1. O usuário acessa a página inicial para realizar a consulta de um candidato.
2. O sistema verifica o nome do candidato nos arquivos CSV locais. Se o candidato for encontrado, o sistema retorna os dados do partido e realiza uma busca por processos na API do Escavador.
3. A aplicação exibe a imagem do candidato (caso disponível) e informações detalhadas dos processos, incluindo a última movimentação.

Com essas funcionalidades, GovBuster oferece aos eleitores uma forma acessível e confiável de se informar sobre candidatos e suas implicações judiciais, promovendo decisões políticas mais conscientes.
