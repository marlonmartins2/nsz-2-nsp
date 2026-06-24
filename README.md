<div align="center">
  <h1>🎮 NSZ Converter Desktop</h1>
  <p><strong>A fast, lightweight, and cross-platform desktop application for converting NSZ to NSP formats.</strong></p>
  
  <p>
    <a href="https://github.com/duck-psycho/nsz-converter-desktop/releases/latest">
      <img src="https://img.shields.io/github/v/release/duck-psycho/nsz-converter-desktop?style=for-the-badge&color=success" alt="Latest Release">
    </a>
    <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue?style=for-the-badge" alt="Platforms">
    <img src="https://img.shields.io/badge/python-3.11+-yellow?style=for-the-badge" alt="Python">
  </p>
</div>

<br>

**NSZ Converter Desktop** is the PC version of the popular Android NSZ Converter. Its main purpose is to help NSZ (compressed) files work in emulators or systems that cannot open them directly by extracting them back into standard NSP format.

Powered by a beautiful **Dark Mode UI** and leveraging the robust `nsz` library by blawar under the hood, it converts your files reliably without freezing or demanding heavy system resources.

---

## ✨ Features

- 🖥️ **Modern Interface**: Beautiful, responsive, and easy-to-use GUI built with CustomTkinter.
- ⚡ **Non-Blocking Processing**: The conversion runs in the background so your UI never freezes.
- 📦 **Standalone Binaries**: Download and run immediately. No Python installation required if you use the pre-compiled versions.
- 🐧 **Linux Support**: Provided as a portable `.AppImage` (Run it anywhere).
- 🪟 **Windows Support**: Provided as a portable `.exe` (Works out of the box).
- ⚙️ **Automated Builds**: Thanks to GitHub Actions, the binaries are automatically built and published on every new release.

## 📥 Download & Usage

1. Go to the **[Releases](../../releases/latest)** section on the right side of this page.
2. **For Windows:** Download `NSZ-Converter-Windows.zip`, extract it, and run `NSZ-Converter.exe`.
3. **For Linux:** Download `NSZ-Converter-x86_64.AppImage`, make it executable (`chmod +x NSZ-Converter-x86_64.AppImage`), and double click it.
4. Select your `.nsz` file, choose where you want to save the output, and click **"CONVERTER PARA NSP"**.

## 🛠️ Build from Source

If you prefer to run it from source or compile the executables yourself:

### Prerequisites
- Python 3.11 or newer installed.
- Git.

### Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USER/nsz-converter-desktop.git
cd nsz-converter-desktop

# Install dependencies
pip install -r requirements.txt

# Run the app directly
python app.py
```

### Compiling Executables
To create the standalone binaries yourself, simply run the included scripts:
- **Windows:** Double-click on `build_windows.bat`. The `.exe` will be saved in `dist/NSZ-Converter/`.
- **Linux:** Run `./build_appimage.sh`. The script will output an `.AppImage` file in the main folder.

## 🤝 Credits & Acknowledgements

- **[nsz](https://github.com/blawar/nsz)** by blawar - The core engine responsible for parsing and decompressing the Nintendo Switch files.
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - For providing the incredible modern UI widgets.

## ⚠️ Disclaimer

The author does not support or encourage piracy in any form. This application does not include, provide, or explain how to obtain game dumps, firmware files, or any other copyrighted materials. Users are solely responsible for ensuring that their use of this software complies with applicable laws and the rights of content owners.
