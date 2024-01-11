import json
import csv

f = open('results.json')

data = json.load(f)

good_websites = []
timeout_websites = []
unresolved_websites = []
certificate_error_websites = []

for item in data:
    url = item['url']
    error: str = item['error']

    if error == None or error.find('find any phone number') != -1:
        good_websites.append(url)
    elif error.find('Timeout 30000ms exceeded') != -1:
        timeout_websites.append(url)
    elif error.find('CERT') != -1:
        certificate_error_websites.append(url)
    elif error.find('NAME'):
        unresolved_websites.append(url)
    elif error.find('SSL') != -1 or error.find('CONNECTION') != -1:
        unresolved_websites.append(url)

    with open('good_websites.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for website in good_websites:
            csv_writer.writerow([website])

    with open('timeout_websites.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for website in timeout_websites:
            csv_writer.writerow([website])

    with open('unresolved_websites.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for website in unresolved_websites:
            csv_writer.writerow([website])
        
    with open('certificate_error_websites.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for website in certificate_error_websites:
            csv_writer.writerow([website])