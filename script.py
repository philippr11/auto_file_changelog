import os
import difflib


def find_all_files(directory):
    """Sucht rekursiv nach allen Dateien in einem Verzeichnis."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def compare_files(file1, file2):
    """Vergleicht den Inhalt von zwei Dateien und gibt die Unterschiede im Diff-Format zurück."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

    diff = difflib.unified_diff(f1_lines, f2_lines, fromfile=file1, tofile=file2)
    return ''.join(diff)


def compare_directories(dir1, dir2, output_file="diff_output.txt"):
    """Vergleicht alle Dateien in zwei Verzeichnissen und speichert die Unterschiede in einer Datei."""
    dir1_files = find_all_files(dir1)
    dir2_files = find_all_files(dir2)

    with open(output_file, 'w') as output:
        dir2_file_set = set(dir2_files)

        for file1 in dir1_files:
            relative_path = os.path.relpath(file1, dir1)
            file2 = os.path.join(dir2, relative_path)

            if os.path.exists(file2):
                # Vergleiche den Inhalt der beiden Dateien
                diff = compare_files(file1, file2)
                if diff:
                    output.write(f"Unterschiede in {relative_path}:\n")
                    output.write(diff)
                    output.write("\n")
                dir2_file_set.discard(file2)
            else:
                output.write(f"Datei {relative_path} existiert nur in {dir1}\n")

        # Dateien, die nur im zweiten Verzeichnis existieren
        for remaining_file in dir2_file_set:
            relative_path = os.path.relpath(remaining_file, dir2)
            output.write(f"Datei {relative_path} existiert nur in {dir2}\n")


if __name__ == "__main__":
    dir1 = "Pfad_zu_Neuem_Ordner"  # Beispiel: neues Verzeichnis
    dir2 = "Pfad_zu_Backup_Ordner"  # Beispiel: Backup-Verzeichnis
    output_file = "vergleich_output.txt"

    compare_directories(dir1, dir2, output_file)
    print(f"Vergleich abgeschlossen. Unterschiede wurden in {output_file} gespeichert.")
