@echo off
cd C:\gerarQRcodeCliente\
rem Ativar ambiente virtual, se necessário
call venv\Scripts\activate

rem Iniciar o navegador com a URL
"C:\Program Files\Google\Chrome\Application\chrome.exe" http://127.0.0.1:5000/

rem Iniciar o servidor Django
python app.py runserver
