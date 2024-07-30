import os
import shutil
from filecmp import dircmp

def compare_folders(folder1, folder2):
    """
    Compara duas pastas e retorna um objeto dircmp contendo as diferenças.
    """
    return dircmp(folder1, folder2)

def print_diff(dcmp):
    """
    Exibe as diferenças entre duas pastas.
    """
    for name in dcmp.diff_files:
        print(f"Diferente: {name}")
    for name in dcmp.left_only:
        print(f"Só na pasta de origem: {name}")
    for name in dcmp.right_only:
        print(f"Só na pasta de destino: {name}")
    for sub_dcmp in dcmp.subdirs.values():
        print_diff(sub_dcmp)

def move_missing_files(dcmp, folder1, folder2, moved_files, error_files):
    """
    Move arquivos e subpastas faltantes da pasta de origem para a pasta de destino.
    """
    for name in dcmp.left_only:
        src_path = os.path.join(dcmp.left, name)
        dst_path = os.path.join(dcmp.right, name)
        try:
            if os.path.isdir(src_path):
                shutil.move(src_path, dst_path)
                print(f"Movendo pasta: {src_path} -> {dst_path}")
            else:
                shutil.move(src_path, dst_path)
                print(f"Movendo arquivo: {src_path} -> {dst_path}")
            moved_files.append(src_path)
        except Exception as e:
            print(f"Erro ao mover {src_path}: {e}")
            error_files.append(src_path)

    for sub_dcmp in dcmp.subdirs.values():
        move_missing_files(sub_dcmp, folder1, folder2, moved_files, error_files)

def save_moved_files(moved_files, output_file):
    """
    Salva os caminhos dos arquivos movidos em um arquivo txt.
    """
    with open(output_file, 'w') as f:
        for file in moved_files:
            f.write(file + '\n')

def main():
    folder1 = input("Digite o caminho da pasta de origem: ")
    folder2 = input("Digite o caminho da pasta de destino: ")

    if not os.path.isdir(folder1):
        print(f"Erro: {folder1} não é um diretório válido.")
        return

    if not os.path.isdir(folder2):
        print(f"Erro: {folder2} não é um diretório válido.")
        return

    dcmp = compare_folders(folder1, folder2)

    print("Diferenças entre as pastas:")
    print_diff(dcmp)

    mover = input("Deseja mover os arquivos e subpastas faltantes para a pasta de destino? (s/n): ")
    if mover.lower() == 's':
        moved_files = []
        error_files = []
        move_missing_files(dcmp, folder1, folder2, moved_files, error_files)
        print(f"Total de arquivos movidos com sucesso: {len(moved_files)}")
        print(f"Total de arquivos com erro ao mover: {len(error_files)}")

        # Salva os caminhos dos arquivos movidos em um arquivo txt
        save_moved_files(moved_files, 'arquivos_movidos.txt')
        print("Os caminhos dos arquivos movidos foram salvos em 'arquivos_movidos.txt'.")

    input("Pressione Enter para fechar o sistema.")

if __name__ == "__main__":
    main()
