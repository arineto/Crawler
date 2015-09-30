#encoding: utf-8
import mmap
import os
import csv
from collections import OrderedDict
from codecs import open

def get_log_files_list(files_dir):
	files = []
	for file in os.listdir(files_dir):
		if file.endswith(".xml"):
			files.append(file)
	return sorted(files)



my_dir = 'corpus/'
file_list = get_log_files_list(my_dir)

matrix = []

q3_counter = 0
q2_counter = 0
q1_counter = 0

for f in file_list:
	c1 = 0
	c2 = 0
	c3 = 0
	file_path = my_dir + f

	with open(file_path, 'rb', 'utf-8') as opened_file:
		read_file = opened_file.read()
		read_file = read_file.lower()

		if 'ovo' in read_file and 'manteiga' in read_file and 'leite' in read_file:
			c1 = 1
			q1_counter += 1
		if (' bolo' in read_file or 'bolo ' in read_file) and 'chocolate' in read_file:
			q2_counter += 1
			c2 = 1
		if ">4 portions" in read_file or ">5 portions" in read_file:
			q3_counter += 1
			c3 = 1

	my_dict = OrderedDict()
	my_dict['Titulo'] = f
	my_dict['Contem ovo, manteiga e leite'] = c1
	my_dict['Bolo de chocolate'] = c2
	my_dict['Serve 5 porcoes'] = c3

	matrix.append(my_dict)


with open('relation_matrix.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, matrix[0].keys())
    w.writeheader()
    for m in matrix:
        w.writerow(m)

print 'total q1 %d' % q1_counter
print 'total q2 %d' % q2_counter
print 'total q3 %d' % q3_counter

