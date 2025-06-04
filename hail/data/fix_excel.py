import pandas as pd
import os

def main():
    # Path to the Excel file
    excel_path = os.path.join(os.path.dirname(__file__), 'NoordHollandii3050scenarios.xlsx')
    
    # Create a mapping dictionary from municipality names to codes
    municipality_mapping = {
        'Aalsmeer': 'GM0358',
        'Alkmaar': 'GM0361',
        'Amstelveen': 'GM0362',
        'Amsterdam': 'GM0363',
        'Beemster': 'GM0370',  # Note: Beemster merged with Purmerend in 2022
        'Bergen (NH.)': 'GM0373',
        'Beverwijk': 'GM0375',
        'Blaricum': 'GM0376',
        'Bloemendaal': 'GM0377',
        'Castricum': 'GM0383',
        'Diemen': 'GM0384',
        'Edam-Volendam': 'GM0385',
        'Enkhuizen': 'GM0388',
        'Haarlem': 'GM0392',
        'Haarlemmermeer': 'GM0394',
        'Heemskerk': 'GM0396',
        'Heemstede': 'GM0397',
        'Heerhugowaard': 'GM0398',  # Now part of Dijk en Waard
        'Heiloo': 'GM0399',
        'Den Helder': 'GM0400',
        'Hilversum': 'GM0402',
        'Hoorn': 'GM0405',
        'Huizen': 'GM0406',
        'Landsmeer': 'GM0415',
        'Langedijk': 'GM0416',  # Now part of Dijk en Waard
        'Laren': 'GM0417',
        'Medemblik': 'GM0420',
        'Oostzaan': 'GM0431',
        'Opmeer': 'GM0432',
        'Ouder-Amstel': 'GM0437',
        'Purmerend': 'GM0439',
        'Schagen': 'GM0441',
        'Texel': 'GM0448',
        'Uitgeest': 'GM0450',
        'Uithoorn': 'GM0451',
        'Velsen': 'GM0453',
        'Weesp': 'GM0457',  # Note: Weesp merged with Amsterdam in 2022
        'Zandvoort': 'GM0473',
        'Zaanstad': 'GM0479',
        'Drechterland': 'GM0498',
        'Stede Broec': 'GM0532',
        'Waterland': 'GM0852',
        'Wormerland': 'GM0880',
        'Koggenland': 'GM1598',
        'Wijdemeren': 'GM1696',
        'Hollands Kroon': 'GM1911',
        'Gooise Meren': 'GM1942',
        'Dijk en Waard': 'GM1980'  # New municipality from merger of Heerhugowaard and Langedijk
    }
    
    # Read the Excel file
    print(f"Reading Excel file: {excel_path}")
    excel_file = pd.ExcelFile(excel_path)
    
    # Create a new Excel writer
    output_path = os.path.join(os.path.dirname(__file__), 'NoordHollandii3050scenarios_fixed.xlsx')
    writer = pd.ExcelWriter(output_path, engine='openpyxl')
    
    # Process each sheet in the Excel file
    for sheet_name in excel_file.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        
        # Read the sheet
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        # Replace municipality names with codes
        # Assuming the municipality name is in the second column (index 1)
        for i, row in df.iterrows():
            municipality_name = row.iloc[1]
            if municipality_name in municipality_mapping:
                df.iloc[i, 1] = municipality_mapping[municipality_name]
            else:
                print(f"Warning: No mapping found for municipality: {municipality_name}")
        
        # Write the modified dataframe to the new Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Save the Excel file
    writer.close()
    print(f"Modified Excel file saved to: {output_path}")

if __name__ == "__main__":
    main()
