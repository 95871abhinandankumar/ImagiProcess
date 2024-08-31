import csv

# Define the data
products = [
    {"serial_number": 1, "name": "SKU1", "input_urls": "https://via.placeholder.com/150/0000FF, https://via.placeholder.com/150/FF0000, https://via.placeholder.com/150/FFFF00"},
    {"serial_number": 2, "name": "SKU2", "input_urls": "https://via.placeholder.com/150/00FF00, https://via.placeholder.com/150/FF00FF, https://via.placeholder.com/150/00FFFF"},
]

# Define the CSV file name
csv_file = "products.csv"

# Write the data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["serial_number", "name", "input_urls"])
    writer.writeheader()
    for product in products:
        writer.writerow(product)

print(f"CSV file '{csv_file}' created successfully.")