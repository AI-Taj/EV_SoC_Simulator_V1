import os
import pandas as pd

# === Base Paths ===
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
tripA_dir = os.path.join(base_path, 'Data', 'Raw_Data', 'TripA')
tripB_dir = os.path.join(base_path, 'Data', 'Raw_Data', 'TripB')
report_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_File_Inventory_Report.txt')

# === Expected Files ===
expected_tripA = [f'TripA{str(i).zfill(2)}.csv' for i in range(1, 33)]
expected_tripB = [f'TripB{str(i).zfill(2)}.csv' for i in range(1, 39)]

os.makedirs(os.path.dirname(report_path), exist_ok=True)
report_lines = []

def analyze_folder(folder_path, expected_files, label):
    report_lines.append(f"\n=== {label} ===\n")
    actual_files = os.listdir(folder_path)
    actual_set = set(actual_files)

    missing = [f for f in expected_files if f not in actual_set]
    if missing:
        report_lines.append(f"Missing files: {', '.join(missing)}\n")
    else:
        report_lines.append("✅ All files present.\n")

    corrupt, empty = [], []
    column_sets = {}

    for fname in expected_files:
        full_path = os.path.join(folder_path, fname)
        if not os.path.exists(full_path):
            continue
        try:
            df = pd.read_csv(full_path, encoding='ISO-8859-1', sep=None, engine='python', nrows=1)
            if df.empty:
                empty.append(fname)
                continue
            col_tuple = tuple(df.columns)
            column_sets.setdefault(col_tuple, []).append(fname)
        except Exception as e:
            corrupt.append((fname, str(e)))

    report_lines.append("\n📌 Column Header Groups Detected:\n")
    for i, (cols, files) in enumerate(column_sets.items(), 1):
        report_lines.append(f"[Group {i}] Found in {len(files)} file(s): {', '.join(files)}\n")
        report_lines.append(f"Headers: {cols}\n\n")

    if corrupt:
        report_lines.append("❌ Corrupt Files:\n")
        for f, err in corrupt:
            report_lines.append(f"{f}: {err}\n")
    if empty:
        report_lines.append("⚠️ Empty Files:\n" + ", ".join(empty) + "\n")

# === Execute
analyze_folder(tripA_dir, expected_tripA, "TripA")
report_lines.append("\n" + "="*60 + "\n")
analyze_folder(tripB_dir, expected_tripB, "TripB")

# === Save Report
with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines([line if line.endswith('\n') else line + '\n' for line in report_lines])

print(f"✅ Inventory report saved to:\n{report_path}")
