import os
import difflib


def build_file_dict(directory):
    """Erstellt ein Dictionary mit relativen Dateipfaden als Schlüsseln und absoluten Dateipfaden als Werten."""
    file_dict = {}
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, directory)
            file_dict[rel_path] = abs_path
    return file_dict


def compare_files(file1, file2):
    """Vergleicht den Inhalt von zwei Dateien und gibt die Unterschiede im Diff-Format zurück."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

    diff = difflib.unified_diff(f1_lines, f2_lines, fromfile=file1, tofile=file2)
    return ''.join(diff)


def compare_directories(dir1, dir2, output_file="diff_output.txt"):
    """Vergleicht Dateien in zwei Verzeichnissen mit Hilfe von Dictionaries und speichert Unterschiede in eine Datei."""
    dir1_files = build_file_dict(dir1)
    dir2_files = build_file_dict(dir2)

    with open(output_file, 'w') as output:
        # Dateien, die in beiden Verzeichnissen existieren
        for rel_path, file1 in dir1_files.items():
            file2 = dir2_files.get(rel_path)
            if file2:
                # Vergleiche die beiden Dateien nur, wenn Größe oder Zeitstempel unterschiedlich sind
                if os.path.getsize(file1) != os.path.getsize(file2) or os.path.getmtime(file1) != os.path.getmtime(
                        file2):
                    diff = compare_files(file1, file2)
                    if diff:
                        output.write(f"Unterschiede in {rel_path}:\n")
                        output.write(diff)
                        output.write("\n")
                # Entferne die Datei aus dir2_files, da sie bereits verglichen wurde
                del dir2_files[rel_path]
            else:
                output.write(f"Datei {rel_path} existiert nur in {dir1}\n")

        # Dateien, die nur im zweiten Verzeichnis existieren
        for rel_path, file2 in dir2_files.items():
            output.write(f"Datei {rel_path} existiert nur in {dir2}\n")


if __name__ == "__main__":
    dir1 = "Pfad_zu_Neuem_Ordner"  # Neues Verzeichnis
    dir2 = "Pfad_zu_Backup_Ordner"  # Backup-Verzeichnis
    output_file = "vergleich_output.txt"

    compare_directories(dir1, dir2, output_file)
    print(f"Vergleich abgeschlossen. Unterschiede wurden in {output_file} gespeichert.")
