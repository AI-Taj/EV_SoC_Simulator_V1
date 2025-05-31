import os

base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'  # <-- Adjust if needed

folders = [
    "Data/Raw_Data/TripA",
    "Data/Raw_Data/TripB",
    "Data/Processed_Trips",
    "Data/Synthetic_Days_Phase1",
    "Data/Synthetic_Months_Phase2",
    "Data/Synthetic_Years_Phase4",
    "Data/Metadata",

    "Models/LSTM",
    "Models/GAN",
    "Models/Hybrid",
    "Models/Checkpoints",

    "Validation/Plots",
    "Validation/Logs",
    "Validation/Reports",

    "App/GUI",
    "App/Export_Tools",

    "Notebooks/Exploratory",
    "Notebooks/Phase_Reports",

    "Scripts/Phase0_DataPrep",
    "Scripts/Phase1_PhysicalGen",
    "Scripts/Phase2_ProfileGen",
    "Scripts/Phase3_AIModels",
    "Scripts/Phase4_LongTerm",
    "Scripts/Phase5_Validation",
    "Scripts/Phase6_App",

    "Figures",
    "Docs/Publications"
]

for folder in folders:
    full_path = os.path.join(base_path, folder)
    os.makedirs(full_path, exist_ok=True)

print("✅ Project structure created successfully.")
