from pathlib import Path
import csv
from energy.models.models import EnergyUnit


path = Path(".").resolve() / "energy" / "static"
for csv_file in path.glob("*long_format.csv"):
    print(f"uploading {csv_file.stem}...")
    entries = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            row = {k.lower(): v for k, v in zip(headers, row)}
            _ = row.pop(""), row.pop("region"), row.pop("municipality")
            row["province_id"] = "PV28"
            entries.append(EnergyUnit(**row))

    EnergyUnit.objects.bulk_create(entries)
