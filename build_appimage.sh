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
python3 -m PyInstaller --noconfirm --onedir --windowed --name "nsz-2-nsp" \
    --add-data "$CTK_PATH:customtkinter/" --add-data "assets/:assets/" --add-binary "$NSZ_PATH:." app.py

echo "Baixando appimagetool..."
wget -qO appimagetool "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
chmod a+x appimagetool

echo "Preparando o diretório AppDir..."
mkdir -p nsz-2-nsp.AppDir
cp -r dist/nsz-2-nsp/* nsz-2-nsp.AppDir/

cat > nsz-2-nsp.AppDir/AppRun << 'EOF'
#!/bin/sh
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}:${PATH}"
exec "${HERE}/nsz-2-nsp" "$@"
EOF
chmod a+x nsz-2-nsp.AppDir/AppRun

cat > nsz-2-nsp.AppDir/nsz-2-nsp.desktop << 'EOF'
[Desktop Entry]
Name=nsz-2-nsp
Exec=AppRun
Icon=nsz-2-nsp
Type=Application
Categories=Utility;
EOF

# Use a dummy icon
touch nsz-2-nsp.AppDir/nsz-2-nsp.png

echo "Gerando AppImage..."
# No WSL o FUSE pode não estar ativo, então extraímos e rodamos
./appimagetool --appimage-extract-and-run nsz-2-nsp.AppDir nsz-2-nsp.AppImage

echo "Sucesso! AppImage gerado: nsz-2-nsp.AppImage"
