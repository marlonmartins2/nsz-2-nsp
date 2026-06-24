@echo off
echo Instalando dependências...
pip install -r requirements.txt

echo Encontrando o caminho do customtkinter...
for /f "tokens=*" %%I in ('python -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))"') do set CTK_PATH=%%I

echo Encontrando o executável nsz...
for /f "tokens=*" %%I in ('python -c "import shutil; print(shutil.which('nsz'))"') do set NSZ_PATH=%%I

echo Construindo o executável do Windows (NSZ-Converter.exe)...
pyinstaller --noconfirm --onedir --windowed --name "NSZ-Converter" --add-data "%CTK_PATH%;customtkinter/" --add-data "assets/;assets/" --add-binary "%NSZ_PATH%;." app.py

echo.
echo Processo finalizado! O executável está na pasta "dist\NSZ-Converter".
pause
