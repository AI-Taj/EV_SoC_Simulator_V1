import os
import re
from collections import Counter, defaultdict

# === Paths ===
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
headers_file = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_All_Headers_List.txt')
output_recommended = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Recommended_Header_Set.txt')
output_discrepancy = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Header_Discrepancy_Report.txt')

# === Fix map for known malformed headers
fix_map = {
    "Cabin Temperature Sensor [°C": "Cabin Temperature Sensor [°C]",
    "Temperature Vent right [°C": "Temperature Vent right [°C]",
    "max. SoC [%)": "max. SoC [%]",
    "Regenerative Braking Signal ": "Regenerative Braking Signal",
    "Velocity [km/h]]]": "Velocity [km/h]",
}

# === Utility: clean a header list
def clean_headers(raw_line):
    parts = [col.strip().strip(';') for col in raw_line.split(';')]
    cleaned = []
    for col in parts:
        if not col:
            continue
        col = fix_map.get(col, col)
        col = re.sub(r'\]+$', ']', col)  # fix extra closing brackets
        cleaned.append(col)
    return cleaned

# === Read header file
with open(headers_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

file_headers = {}
current_file = None

for line in lines:
    if line.endswith(".csv:\n"):
        current_file = line.strip().replace(":", "")
    elif current_file and line.strip():
        header_list = clean_headers(line.strip())
        file_headers[current_file] = header_list
        current_file = None

# === Count header frequencies
header_counter = Counter()
for headers in file_headers.values():
    header_counter.update(headers)

# === Determine recommended set (present in ≥20 files or essential)
mandatory_headers = {"Time [s]"}
recommended = {h for h, count in header_counter.items() if count >= 20}
recommended.update(mandatory_headers)
recommended = sorted(recommended)

# === Write recommended header set
with open(output_recommended, 'w', encoding='utf-8') as f:
    f.write("Recommended Header Set (cleaned, majority-based)\n")
    for h in recommended:
        f.write(h + "\n")

# === Write discrepancy report
with open(output_discrepancy, 'w', encoding='utf-8') as f:
    for fname, headers in file_headers.items():
        missing = sorted(set(recommended) - set(headers))
        extra = sorted(set(headers) - set(recommended))
        f.write(f"{fname}:\n")
        f.write(f"  ❌ Missing: {', '.join(missing) if missing else 'None'}\n")
        f.write(f"  ⚠️  Extra:   {', '.join(extra) if extra else 'None'}\n\n")

print("✅ Recommended headers and discrepancy report generated.")
