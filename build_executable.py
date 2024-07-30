import subprocess
import os

# Caminho do script Python que você deseja compilar
script_name = "fix-postgres-folder.py"

# Diretório onde o executável será gerado
output_dir = "exe"

# Cria o diretório de saída se ele não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Comando para compilar o script usando Nuitka
command = [
    "python",  # Certifique-se de que 'python' está no PATH
    "-m", "nuitka",
    "--follow-imports",  # Seguir importações para criar um executável completo
    "--onefile",  # Criar um único executável
    f"--output-dir={output_dir}",  # Diretório de saída
    script_name
]

# Executa o comando
subprocess.run(command, check=True)
