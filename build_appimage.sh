#!/bin/bash
set -e

echo "Instalando dependências..."
pip3 install -r requirements.txt

echo "Encontrando caminho do customtkinter..."
CTK_PATH=$(python3 -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))")

echo "Encontrando executável nsz..."
NSZ_PATH=$(python3 -c "import shutil; print(shutil.which('nsz'))")

echo "Construindo binário com PyInstaller..."
# Adicionamos pyinstaller local ao PATH
export PATH=$PATH:$HOME/.local/bin
python3 -m PyInstaller --noconfirm --onedir --windowed --name "NSZ-Converter" \
    --add-data "$CTK_PATH:customtkinter/" --add-data "assets/:assets/" --add-binary "$NSZ_PATH:." app.py

echo "Baixando appimagetool..."
wget -qO appimagetool "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
chmod a+x appimagetool

echo "Preparando o diretório AppDir..."
mkdir -p NSZ-Converter.AppDir
cp -r dist/NSZ-Converter/* NSZ-Converter.AppDir/

cat > NSZ-Converter.AppDir/AppRun << 'EOF'
#!/bin/sh
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}:${PATH}"
exec "${HERE}/NSZ-Converter" "$@"
EOF
chmod a+x NSZ-Converter.AppDir/AppRun

cat > NSZ-Converter.AppDir/nsz-converter.desktop << 'EOF'
[Desktop Entry]
Name=NSZ Converter
Exec=AppRun
Icon=nsz-converter
Type=Application
Categories=Utility;
EOF

# Use a dummy icon
touch NSZ-Converter.AppDir/nsz-converter.png

echo "Gerando AppImage..."
# No WSL o FUSE pode não estar ativo, então extraímos e rodamos
./appimagetool --appimage-extract-and-run NSZ-Converter.AppDir nsz-2-nsp.AppImage

echo "Sucesso! AppImage gerado: nsz-2-nsp.AppImage"
