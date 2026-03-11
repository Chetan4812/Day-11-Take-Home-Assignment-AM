import csv
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Step 1: Locate all CSV files automatically
data_folder = Path(".")  # current directory
csv_files = list(data_folder.glob("data*.csv"))

all_rows = []

# Step 2: Read and merge all rows
for file in csv_files:
    with open(file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # convert numeric fields
            row["qty"] = int(row["qty"])
            row["price"] = float(row["price"])
            all_rows.append(row)

# Step 3: Remove duplicate rows
unique_rows = []
seen = set()

for row in all_rows:
    key = (row["date"], row["product"], row["qty"], row["price"])
    if key not in seen:
        seen.add(key)
        unique_rows.append(row)

# Step 4: Sort rows by date
unique_rows.sort(key=lambda x: x["date"])

# Step 5: Calculate revenue per product
revenue_by_product = defaultdict(float)
total_revenue = 0

for row in unique_rows:
    revenue = row["qty"] * row["price"]
    revenue_by_product[row["product"]] += revenue
    total_revenue += revenue

# Step 6: Export merged CSV
with open("merged_sales.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "product", "qty", "price"])
    writer.writeheader()
    writer.writerows(unique_rows)

# Step 7: Create JSON summary
output = {
    "metadata": {
        "files_processed": len(csv_files),
        "total_rows": len(unique_rows),
        "total_revenue": round(total_revenue, 2),
        "generated_at": datetime.now().isoformat()
    },
    "revenue_by_product": {
        product: round(revenue, 2)
        for product, revenue in revenue_by_product.items()
    }
}

# Step 8: Write JSON file
with open("revenue_summary.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("Pipeline complete.")
print("Generated: merged_sales.csv and revenue_summary.json")