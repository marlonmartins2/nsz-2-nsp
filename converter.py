import subprocess
import os
import threading
import sys

def get_nsz_executable():
    """
    Returns the path to the nsz executable.
    When packaged with PyInstaller, it will use the bundled executable
    or fallback to system command.
    """
    if getattr(sys, 'frozen', False):
        # In a PyInstaller bundle
        return os.path.join(sys._MEIPASS, 'nsz.exe' if os.name == 'nt' else 'nsz')
    return shutil.which('nsz') or 'nsz' # Using nsz from system PATH during development

def extract_keys():
    import base64
    import tempfile
    import zlib
    
    try:
        from keys_data import ENCRYPTED_KEYS
        compressed = base64.b64decode(ENCRYPTED_KEYS)
        decrypted = zlib.decompress(compressed)
    except Exception as e:
        print("Erro ao decodificar chaves embutidas:", e)
        return None

    temp_dir = tempfile.mkdtemp()
    keys_dir = os.path.join(temp_dir, '.switch')
    os.makedirs(keys_dir, exist_ok=True)
    
    keys_path = os.path.join(keys_dir, 'prod.keys')
    with open(keys_path, "wb") as f:
        f.write(decrypted)
        
    return temp_dir

def convert_nsz_to_nsp(input_file, output_dir, progress_callback, completion_callback, error_callback):
    """
    Converts a single NSZ file to NSP format using the 'nsz' tool in a background thread.
    
    Args:
        input_file (str): Path to the .nsz file.
        output_dir (str): Path to the destination directory.
        progress_callback (function): Function to call with status updates (string message).
        completion_callback (function): Function to call when conversion finishes successfully.
        error_callback (function): Function to call if conversion fails.
    """
    def run_conversion():
        try:
            progress_callback(f"Iniciando conversão de: {os.path.basename(input_file)}")
            cmd = [
                sys.executable, "-m", "nsz", "-D", input_file, "-o", output_dir
            ] if not getattr(sys, 'frozen', False) else [get_nsz_executable(), "-D", input_file, "-o", output_dir]
            
            temp_keys_dir = extract_keys()
            env = os.environ.copy()
            if temp_keys_dir:
                env['USERPROFILE'] = temp_keys_dir
                env['HOME'] = temp_keys_dir
            
            # Start process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            # Read output real-time (to keep GUI alive and potentially parse progress)
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    clean_line = line.strip()
                    if clean_line:
                        # Log or parse output if necessary
                        progress_callback(f"Processando... (Veja os logs no terminal se houver erro)")
            
            return_code = process.poll()
            process.wait()

            if temp_keys_dir:
                try:
                    shutil.rmtree(temp_keys_dir)
                except:
                    pass
            
            if process.returncode == 0:
                progress_callback("Conversão finalizada com sucesso!")
                completion_callback()
            else:
                error_callback(f"Erro na conversão. Código de saída: {return_code}")
                
        except Exception as e:
            error_callback(f"Exceção durante conversão: {str(e)}")

    # Start the thread
    thread = threading.Thread(target=run_conversion)
    thread.daemon = True
    thread.start()
