# Gerador de QR Code para Pastas de Clientes no Google Drive

## Descrição do Projeto
Este projeto tem como objetivo criar um sistema que automatiza a criação de pastas no Google Drive para cada cliente, usando como identificador o nome e CPF ou CNPJ do cliente. Após criar a pasta, o sistema gera um QR Code que, ao ser escaneado, leva diretamente ao link da pasta no Google Drive. Este QR Code também pode ser baixado para impressão, com a identificação do cliente e o URL da pasta incluídos abaixo do código. O sistema foi desenvolvido com Flask, integrado com a API do Google Drive e permite um controle completo dos registros de logs.

## Funcionalidades
- **Autenticação**: Autentica automaticamente com a API do Google Drive usando um arquivo de credenciais.
- **Criação de Pasta**: Verifica se uma pasta para o cliente já existe; se não, cria uma nova e gera o link de acesso.
- **Permissões**: Define permissões de leitura pública para o link e de edição para um email específico.
- **Geração de QR Code**: Cria um QR Code com o link da pasta e adiciona os dados do cliente para fácil identificação.
- **Registro de Logs**: Possui um sistema de logs ativável para registro de cada ação e evento no sistema.

## Estrutura do Projeto
```bash
GERARQRCODECLIENTE/
├── app.py              # Código principal do Flask
├── chave api.txt       # Arquivo de API opcional
├── credentials.json    # Arquivo de credenciais do Google
├── ClienteQRcode.txt   # Registro dos dados do cliente e URLs
├── logs.txt            # Registro dos logs do sistema
└── templates/
    └── index.html      # Interface HTML para entrada de dados do cliente
```
## Como o Projeto Funciona
- **Recebimento de Dados**: A interface HTML coleta o nome e CPF/CNPJ do cliente e os envia ao Flask.
- **Criação da Pasta no Google Drive**: O sistema verifica se a pasta para o cliente existe. Caso não, cria a pasta e registra o link para o Google Drive.
- **Geração do QR Code**: Gera o QR Code do link da pasta e inclui a identificação do cliente, salvando o QR Code para possível download.
- **Permissões**: Define permissões de leitura pública e, se configurado, permissões adicionais para um email específico.
- **Registro de Logs e Dados do Cliente**: Grava cada evento (como criação de pastas e geração de QR Codes) nos arquivos `logs.txt` e `ClienteQRcode.txt`.

## Como Implantar

### Pré-requisitos
- **Python 3** instalado
- **Bibliotecas necessárias**:
  - Flask
  - google-auth
  - google-auth-oauthlib
  - google-auth-httplib2
  - google-api-python-client
  - qrcode[pil]
  - Pillow

### Instalação das Dependências
```bash
pip install Flask google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client qrcode[pil] Pillow
```
### Configuração do Google Drive
1. Crie um projeto no Google Cloud e habilite a API do Google Drive.
2. Gere um arquivo de credenciais JSON e nomeie-o como `credentials.json`.
3. Adicione o email da conta de serviço como colaborador com permissões apropriadas, conforme necessário.

### Execução do Servidor Flask
```bash
python app.py
```
Para iniciar o servidor, execute o seguinte comando:

### Acesso à Interface

1. Abra o navegador e vá para [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
2. Preencha o formulário com os dados do cliente e clique para criar a pasta e gerar o QR Code.

### Verificação de Logs e Informações de Clientes
- Acompanhe as atividades no arquivo `logs.txt`.
- Verifique os registros de URLs e clientes em `ClienteQRcode.txt`.
