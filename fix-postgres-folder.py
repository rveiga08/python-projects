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

def move_missing_files(dcmp, folder1, folder2):
    """
    Move arquivos e subpastas faltantes da pasta de origem para a pasta de destino.
    """
    for name in dcmp.left_only:
        src_path = os.path.join(dcmp.left, name)
        dst_path = os.path.join(dcmp.right, name)
        if os.path.isdir(src_path):
            shutil.move(src_path, dst_path)
            print(f"Movendo pasta: {src_path} -> {dst_path}")
        else:
            shutil.move(src_path, dst_path)
            print(f"Movendo arquivo: {src_path} -> {dst_path}")

    for sub_dcmp in dcmp.subdirs.values():
        move_missing_files(sub_dcmp, folder1, folder2)

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
        move_missing_files(dcmp, folder1, folder2)
        print("Arquivos e subpastas faltantes movidos com sucesso.")

if __name__ == "__main__":
    main()
