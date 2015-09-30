#encoding: utf-8
import os
import csv
from collections import OrderedDict
from codecs import open

def get_log_files_list(files_dir):
    files = []
    for file in os.listdir(files_dir):
        if file.endswith(".html"):
            files.append(file)
    return sorted(files)


def read_files():
    my_dir = 'crawled_files/'

    file_list = get_log_files_list(my_dir)
    file_list = file_list[:101]
    matrix = []
    print len(file_list)
    for i, f in enumerate(file_list):
        file_id = i
        title = ''
        time = ''
        quantity = ''
        votes = ''
        file_path = my_dir + f

        content = ''

        with open(file_path, 'rb', "utf-8") as f:
            # Get file lines beginning from start_line
            # file_rows = list(csv.reader(f))[start_line:]
            f_list = list(f)

            for index, row in enumerate(f_list):
                c1 = c2 = c3 = 0

                if '<title>' in row:
                    title = row[7:-24]
                    title = title.encode('ascii','ignore')
                elif 'num preptime' in row:
                    time = f_list[index+1]
                    time = time[:-1]
                    if 'h' not in time:
                        c2 = 1
                    else:
                        c2 = 0
                elif 'num yield' in row:
                    quantity = f_list[index+1]
                    try:
                        quantity = quantity[:-5]+"tions"
                        if 3 >= float(quantity[:quantity.index(' por')]) <= 6 :
                            c3 = 1 
                        else:
                            c3 = 0
                    except:
                        c3 = 0
                        quantity = 'Nenhum'
                elif 'votenum count' in row:
                    votes = f_list[index+1]
                    votes = votes[:-1]
                    try:
                        if float(votes[:votes.index(' voto')]) > 25 :
                            c1 = 1
                        else:
                            c1 = 0
                    except:
                        c1 = 0
                elif 'recipelist' in row:
                    content += f_list[index+1]

        if title and not title.isspace():
            my_dict = OrderedDict()
            my_dict['ID'] = file_id
            my_dict['Titulo'] = title
            my_dict['Tempo de Preparo'] = time
            my_dict['Tempo de preparo abaixo de 1h'] = c2
            my_dict['Quantidade de Porcoes'] = quantity
            my_dict['Quantidade de porcoes entre 3 e 6'] = c3
            my_dict['Votos'] = votes
            my_dict['Votos acima de 25'] = c1
            my_dict['Conteudo'] = content
            matrix.append(my_dict)

    return matrix

my_matrix = read_files()
print len(my_matrix)
# with open('mycsvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
#     w = csv.DictWriter(f, my_matrix[0].keys())
#     w.writeheader()
#     for m in my_matrix:
#         w.writerow(m)

import xml.etree.cElementTree as ET

for item in my_matrix:

    document = ET.Element("Document", docname=str(item["ID"]))
    content = ET.SubElement(document, "Content")
    ET.SubElement(content, "ID").text = str(item['ID'])
    ET.SubElement(content, "Titulo").text = item['Titulo']
    
    receita = ET.SubElement(content, "Receita")
    ET.SubElement(receita, "TempoPreparo").text = item['Tempo de Preparo']
    ET.SubElement(receita, "QuantidadePorcoes").text = item['Quantidade de Porcoes']
    ET.SubElement(receita, "Votos").text = item['Votos']
    ET.SubElement(receita, "Conteudo").text = item['Conteudo']
    tree = ET.ElementTree(document)
    file_name = "corpus/{0}.xml".format(item['Titulo'])
    tree.write(file_name, encoding="UTF-8", xml_declaration=True)
