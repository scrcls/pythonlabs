#! -*- coding:utf-8 -*-

import csv
from bs4 import BeautifulSoup as bs

def parse_contact(filename):
    with open(filename) as myfile:
        contact_data = myfile.read()
    
    soup = bs(contact_data, 'lxml')
    contact_table = soup.find('table', attrs = {'class' : 'table table-striped'})
    contact_list = []
    for contact_info in contact_table.find_all('tr')[1:]:
        contact_info = contact_info.find_all('td')
        empno = contact_info[0].text
        name = contact_info[1].text.encode('utf-8')
        mail = contact_info[2].text
        dept = contact_info[3].text.encode('utf-8')
        if not name.endswith('(disabled)'):
            contact_list.append({'姓名' : name, 
                                '电子邮件' : mail,
                                '部门' : dept
                                })
    #for item in contact_dict:
    #    for key, val in item.iteritems():
    #        print key, val
    return contact_list
        

def write_csv(contact_header, contact_list, out_file):
    with open(out_file, 'wb') as myfile:
        writer = csv.DictWriter(myfile, fieldnames = contact_header,
                                delimiter = ',', quotechar = '\"',
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for contact_info in contact_list:
            writer.writerow(contact_info)

def read_csv(in_file):
    with open(in_file, 'rb') as myfile:
        reader = csv.reader(myfile, delimiter = ',', quotechar = '"')
        field_names = reader.next()
        return field_names

if __name__ == '__main__':
    contact_file = './contacts.html'
    address_file = './address.txt'
    contact_header = read_csv(address_file)
    contact_list = parse_contact(contact_file)
    write_csv(contact_header, contact_list, 'result.csv')

    
