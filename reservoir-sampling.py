import csv
import random

def reservoir_sampling(file_name, sample_size):
    reservoir = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        header = next(reader) # Skip header row

        for i, row in enumerate(reader):
            if i < sample_size: 
                reservoir.append(row)
            else:
                j = random.randint(0, i)
                if j < sample_size:
                    reservoir[j] = row
    return header, reservoir
    
file_name = 'medical_data.csv'
sample_size = 50000
header, sample = reservoir_sampling(file_name, sample_size)

# Write sampled data to a new csv file

new_file = open('sampled_medical_data.csv', 'w+', newline='')

with new_file:
    write = csv.writer(new_file)
    write.writerow(header)
    write.writerows(sample)

