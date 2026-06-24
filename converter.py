import subprocess
import os
import threading
import sys
import shutil
import keys_data

def get_nsz_executable():
    # Remove get_nsz_executable as we use NSZ_RUNNER_MODE directly via sys.executable
    pass

def extract_keys():
    import base64
    import tempfile
    import zlib
    
    try:
        compressed = base64.b64decode(keys_data.ENCRYPTED_KEYS)
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
                sys.executable, "NSZ_RUNNER_MODE", "-D", input_file, "-o", output_dir
            ] if getattr(sys, 'frozen', False) else [sys.executable, "-m", "nsz", "-D", input_file, "-o", output_dir]
            
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
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                env=env,
                stdin=subprocess.DEVNULL
            )

            last_line = ""
            # Lê a saída linha por linha para atualizar o progresso (se possível)
            for line in process.stdout:
                line_str = line.strip()
                if line_str:
                    last_line = line_str
                    progress_callback(f"Processando... (Veja os logs no terminal se houver erro)")
            
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
                error_callback(f"Erro na conversão. Código: {process.returncode}. Detalhe: {last_line}")
                
        except Exception as e:
            error_callback(f"Exceção durante conversão: {str(e)}")

    # Start the thread
    thread = threading.Thread(target=run_conversion)
    thread.daemon = True
    thread.start()
