import csv
import os

def read_data_csv(filename):
    data = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
            data.append(row)
    
    if len(data) != 2:
        print("corrupted csv file")
    
    return data[0], data[1]

def save_data_csv(dir, x_data, y_data):
    if len(x_data) != len(y_data):
        print("the dimensions of x_data and y_data are unequal")
    
    filename = dir + "mock_run_1.csv"
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(x_data)
        writer.writerow(y_data)
        file.close()
