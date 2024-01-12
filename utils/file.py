import csv
import json

def read_csv(file):
    data = set()

    with open(file, mode='r') as f:
        csv_reader = csv.reader(f,)
        for lines in csv_reader:
            if lines[0] == 'domains': continue
            data.add(lines[0])
    
    return list(data)

def save_to_csv(json_file,csv_file = 'test.csv'):
    with open(csv_file,'w') as cf:
        csv_writer = csv.writer(cf)
        with open(json_file,'r') as jf:
            data = json.load(jf)

            for d in data:
                if not d.keys(): continue
                if 'phone' not in d.keys():
                    csv_writer.writerow([d['home_url'],''])
                    continue
                for p in d['phone']:
                    csv_writer.writerow([d['home_url'],p])

