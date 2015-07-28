#! -*- coding:utf-8 -*-

import csv
from bs4 import BeautifulSoup as bs

def parse_contact(filename):
    with open(filename) as myfile:
        contact_data = myfile.read()
    
    soup = bs(contact_data, 'lxml')
    contact_table = soup.find('table', attrs = {'class' : 'table table-striped'})
    for contact_info in contact_table.find_all('tr')[1:]:
        contact_info = contact_info.find_all('td')
        empno = contact_info[0].text
        name = contact_info[1].text.encode('utf-8')
        mail = contact_info[2].text
        dept = contact_info[3].text.encode('utf-8')
        if name.endswith('(disabled)'):
            print name, dept
        

def write_csv(contact_data, out_file):
    pass

def read_csv(in_file):
    with open(in_file, 'rb') as myfile:
        reader = csv.DictReader(myfile)
        for row in reader:
            print row.keys()[0]
    
if __name__ == '__main__':
    contact_file = './contacts.html'
    address_file = './address.csv'
    read_csv(address_file)
    #parse_contact(contact_file)

    
