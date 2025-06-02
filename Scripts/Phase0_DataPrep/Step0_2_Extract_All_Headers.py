import os

# === Base Paths ===
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
tripA_dir = os.path.join(base_path, 'Data', 'Raw_Data', 'TripA')
tripB_dir = os.path.join(base_path, 'Data', 'Raw_Data', 'TripB')
output_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_All_Headers_List.txt')

os.makedirs(os.path.dirname(output_path), exist_ok=True)

# === Function to clean and extract header line ===
def extract_header(filepath):
    with open(filepath, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            # Return first non-empty line
            if line.strip():
                return line.strip()
    return ""

# === Main Extraction ===
lines = []

for folder, label, count in [(tripA_dir, "TripA", 32), (tripB_dir, "TripB", 38)]:
    lines.append(f"\n=== {label} HEADERS ===\n")
    for i in range(1, count + 1):
        fname = f"{label}{str(i).zfill(2)}.csv"
        path = os.path.join(folder, fname)
        if os.path.exists(path):
            header_line = extract_header(path)
            lines.append(f"{fname}:\n{header_line}\n")
        else:
            lines.append(f"{fname}:\n⚠️ File not found\n")

# === Write result
with open(output_path, 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line if line.endswith('\n') else line + '\n')

print(f"✅ Header extraction completed. Output saved to:\n{output_path}")
