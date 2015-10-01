#encoding: utf-8
import mmap
import os
import csv
import operator
from collections import OrderedDict
from codecs import open

def get_log_files_list(files_dir):
	files = []
	for file in os.listdir(files_dir):
		if file.endswith(".xml"):
			files.append(file)
	return sorted(files)



my_dir = 'corpus_id/'
file_list = get_log_files_list(my_dir)

movies = []

q1_priority = {}
q2_priority = {}
q3_priority = {}

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

		# Q1 = 'movies of Kevin McKidd'
		# Q2 = 'Martin Freeman and Nick Frost'
		# Q3 = 'World War'

		if ('movie' in read_file) or ('movies' in read_file) or ('of' in read_file) or ('kevin' in read_file) or ('mckidd' in read_file) or ('kevin mckidd') in read_file:
			priority = 0
			priority += read_file.count('movie')
			priority += read_file.count('movies')
			priority += read_file.count('of')
			priority += read_file.count('kevin')
			priority += read_file.count('mckidd')
			priority += read_file.count('kevin mckidd')*5
			q1_priority[f] = priority
			q1_counter += 1
			c1 = 1
		
		if ('martin' in read_file) or ('freeman' in read_file) or ('and' in read_file) or ('nick' in read_file) or ('frost' in read_file) \
		or ('martin freeman' in read_file) or ('nick frost' in read_file):
			priority = 0
			priority += read_file.count('martin')
			priority += read_file.count('freeman')
			priority += read_file.count('and')
			priority += read_file.count('nick')
			priority += read_file.count('frost')
			priority += read_file.count('martin freeman')*5
			priority += read_file.count('nick frost')*5
			q2_priority[f] = priority
			q2_counter += 1
			c2 = 1
		
		if ('world' in read_file) or ('war' in read_file):
			priority = 0
			priority += read_file.count('world')
			priority += read_file.count('war')
			priority += read_file.count('world war')*5
			q3_priority[f] = priority
			q3_counter += 1
			c3 = 1
	
	my_dict = OrderedDict()
	my_dict['ID'] = f
	my_dict['Movies of Kevin MdKidd'] = c1
	my_dict['Martin Freeman and Nick Frost'] = c2
	my_dict['World War'] = c3

	movies.append(my_dict)


with open('relation_matrix.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, movies[0].keys())
    w.writeheader()
    for m in movies:
        w.writerow(m)


my_range = [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]

print 'Consulta 1 - Movies of Kevin Mckidd'
print 'Total de Filmes: %d' % q1_counter
print 'Top 10:'
movies = sorted(q1_priority.items(), key=operator.itemgetter(1))
for i in my_range:
	print '%d - %s (Score: %d)' % (i+1, movies[i][0], movies[i][1])


print 'Consulta 2 - Martin Freeman and Kevin Frost'
print 'Total de Filmes: %d' % q2_counter
print 'Top 10:'
movies = sorted(q2_priority.items(), key=operator.itemgetter(1))
for i in my_range:
	print '%d - %s (Score: %d)' % (i+1, movies[i][0], movies[i][1])


print 'Consulta 1 - World War'
print 'Total de Filmes: %d' % q3_counter
print 'Top 10:'
movies = sorted(q3_priority.items(), key=operator.itemgetter(1))
for i in my_range:
	print '%d - %s (Score: %d)' % (i+1, movies[i][0], movies[i][1])

