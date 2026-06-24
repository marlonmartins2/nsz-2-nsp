#!/bin/bash
set -e

echo "Instalando dependências..."
pip3 install -r requirements.txt

echo "Encontrando caminho do customtkinter..."
CTK_PATH=$(python3 -c "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))")



echo "Construindo binário com PyInstaller..."
# Adicionamos pyinstaller local ao PATH
export PATH=$PATH:$HOME/.local/bin
python3 -m PyInstaller --noconfirm --onedir --windowed --name "nsz-2-nsp" --icon=icon.ico --hidden-import nsz \
    --add-data "$CTK_PATH:customtkinter/" app.py

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

# Copy the icon
cp icon.png nsz-2-nsp.AppDir/nsz-2-nsp.png

echo "Gerando AppImage..."
# No WSL o FUSE pode não estar ativo, então extraímos e rodamos
./appimagetool --appimage-extract-and-run nsz-2-nsp.AppDir

# O appimagetool costuma gerar com nome nsz-2-nsp-x86_64.AppImage
if [ -f "nsz-2-nsp-x86_64.AppImage" ]; then
    mv nsz-2-nsp-x86_64.AppImage nsz-2-nsp.AppImage
fi

echo "Sucesso! AppImage gerado: nsz-2-nsp.AppImage"
