import os
import qrcode
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import Flask, request, jsonify, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


# Variável de controle para ativar ou desativar os logs
logdebug = False

# Função para adicionar logs com data e hora
def add_log(mensagem):
    if logdebug:  # Verifica se o log está ativado
        with open("logs.txt", "a") as log_file:  # "a" para abrir no modo append
            data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato da data e hora
            log_file.write(f"{data_hora} - {mensagem}\n")
        

# Função para adicionar informações de clientes em ClienteQRcode.txt
def add_cliente_info(texto):
    with open("ClienteQRcode.txt", "a") as cliente_file:  # "a" para abrir no modo append
        cliente_file.write(f"{texto}\n")  # Escreve o texto com quebra de linha
    print("Informação do cliente salva com sucesso!")

# Autenticação no Google Drive
def authenticate_drive():
    try:
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )
        add_log("Autenticado com sucesso no Google Drive.")
        print("Autenticado com sucesso no Google Drive.")
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        add_log(f"Erro na autenticação do Google Drive: {e}")
        print(f"Erro na autenticação do Google Drive: {e}")
        raise

# Função para criar a pasta no Google Drive
def create_folder(client_name, cpf, drive_service):
    folder_name = f"{client_name}_{cpf}"
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"

    try:
        results = drive_service.files().list(q=query).execute()
        if results['files']:
            folder_id = results['files'][0]['id']
            add_log(f"Pasta já existe: {folder_name}")
            print(f"Pasta já existe: {folder_name}")
        else:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = drive_service.files().create(body=file_metadata, fields="id").execute()
            folder_id = folder.get('id')
            add_log(f"Pasta criada: {folder_name}")
            print(f"Pasta criada: {folder_name}")
            add_permission_to_folder(folder_id, drive_service)
            url = f"https://drive.google.com/drive/folders/{folder_id}"
            add_cliente_info(f"Cliente: {client_name} - CPF/CNPJ: {cpf} - URL: {url}")
        
        folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
        return folder_url
    except Exception as e:
        add_log(f"Erro ao criar a pasta: {e}")
        print(f"Erro ao criar a pasta: {e}")
        raise

# Função para adicionar permissões específicas
def add_permission_to_folder(folder_id, drive_service):
    try:
        permission_anyone = {
            'type': 'anyone',
            'role': 'reader',
        }
        permission_gmail = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'topsaudece2024@gmail.com'
        }

        drive_service.permissions().create(
            fileId=folder_id,
            body=permission_anyone,
            fields='id'
        ).execute()
        add_log("Permissão pública de leitura foi adicionada à pasta.")
        print("Permissão pública de leitura foi adicionada à pasta.")

        drive_service.permissions().create(
            fileId=folder_id,
            body=permission_gmail,
            fields='id'
        ).execute()
        add_log(f"Permissão de leitura e edição foi adicionada para o e-mail {permission_gmail['emailAddress']}.")
        print(f"Permissão de leitura e edição foi adicionada para o e-mail {permission_gmail['emailAddress']}.")
    except Exception as e:
        add_log(f"Erro ao adicionar permissões: {e}")
        print(f"Erro ao adicionar permissões: {e}")
        raise

# Função para gerar QR code
def generate_qr_code(data, text, output_file="qrcode.png"):
    try:
        qr = qrcode.make(data).convert("RGB")
        qr_width, qr_height = qr.size
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        text_bbox = font.getbbox(text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        total_height = qr_height + text_height + 10
        new_image = Image.new("RGB", (qr_width, total_height), "white")

        new_image.paste(qr, (0, 0, qr_width, qr_height))

        draw = ImageDraw.Draw(new_image)
        text_x = (qr_width - text_width) // 2
        text_y = qr_height + 5
        draw.text((text_x, text_y), text, font=font, fill="black")

        new_image.save(output_file)
        add_log(f"QR Code com texto salvo como {output_file}")
        print(f"QR Code com texto salvo como {output_file}")
    except Exception as e:
        add_log(f"Erro ao gerar QR Code: {e}")
        print(f"Erro ao gerar QR Code: {e}")
        raise

# Configuração do servidor Flask
app = Flask(__name__)

# Rota para carregar o formulário HTML
@app.route('/')
def home():
    return render_template('index.html')

# Rota para criar a pasta no Google Drive e gerar o QR code
@app.route('/create_folder', methods=['POST'])
def create_folder_route():
    data = request.json
    client_name = data.get('client_name')
    cpf = data.get('cpf')

    try:
        drive_service = authenticate_drive()
        folder_url = create_folder(client_name, cpf, drive_service)
        text = f"   {client_name} - {cpf}"
        generate_qr_code(folder_url, text)
        add_log(f"Cliente: {client_name} - CPF/CNPJ: {cpf} - URL: {folder_url}")

        return jsonify({"message": "Pasta criada e QR Code gerado com sucesso!"})
    except Exception as e:
        add_log(f"Erro ao processar a rota /create_folder: {e}")
        print(f"Erro ao processar a rota /create_folder: {e}")
        return jsonify({"message": "Erro ao criar a pasta ou gerar QR Code"}), 500

# Rota para baixar o QR code para impressão
@app.route('/download_qr', methods=['GET'])
def download_qr():
    path = "qrcode.png"
    try:
        add_log("QR Code enviado para download.")
        print("QR Code enviado para download.")
        return send_file(path, as_attachment=True)
    except Exception as e:
        add_log(f"Erro ao baixar o QR Code: {e}")
        print(f"Erro ao baixar o QR Code: {e}")
        return jsonify({"message": "Erro ao baixar o QR Code"}), 500

if __name__ == '__main__':
    app.run(debug=True)
