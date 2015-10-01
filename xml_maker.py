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
    file_list = file_list
    matrix = []
    print len(file_list)
    for i, f in enumerate(file_list):
        file_id = f[:-5]
        file_path = my_dir + f

        with open(file_path, 'rb', "utf-8") as f:
            # Get file lines beginning from start_line
            # file_rows = list(csv.reader(f))[start_line:]
            f_list = list(f)
            trash_title = '    <meta property="og:title" content="'
            trash_title2 = '" />'
            movie_title = ''
            director_trash = 'itemprop="url"><span class="itemprop" itemprop="name">'
            director_trash_2 = '</span>'
            movie_director = ''
            movie_stars = ''
            movie_description = ''
            stars = float(0)
            movie_genre = ''

            for index, row in enumerate(f_list):
                if "<meta property='og:title' content=" in row:
                    movie_title = row[len(trash_title):row.index(trash_title2)]
                    try:
                        movie_title = movie_title.replace("&quot;", "")
                    except:
                        pass
                if '<h4 class="inline">Director:</h4>' in row:
                    desired_row = f_list[index+2]
                    movie_director = desired_row[len(director_trash):desired_row.index(director_trash_2)]
                if '<h4 class="inline">Stars:</h4>' in row:
                    for i in range(2, 7, 2):
                        star = f_list[index+i]
                        if director_trash[15:] in star:
                            movie_stars += star[len(director_trash):star.index(director_trash_2)]
                            movie_stars += ', '
                if '<p itemprop="description">' in row:
                    desired_row = f_list[index+1]
                    movie_description = desired_row[:desired_row.index('<')]
                if '<div class="titlePageSprite star-box-giga-star">' in row:
                    stars = float(row[row.index('<div class="titlePageSprite star-box-giga-star">')+len('<div class="titlePageSprite star-box-giga-star">'):-1-len('</div>')])
                if '<h4 class="inline">Genres:</h4>' in row:
                    desired_row = f_list[index+2]
                    movie_genre = desired_row[2:desired_row.index('<')]
       
        if ( 
            ( movie_title and not movie_title.isspace() ) and
            ( movie_director and not movie_director.isspace() ) and
            ( movie_stars ) and
            ( movie_description and not movie_description.isspace() ) and
            ( movie_genre and not movie_genre.isspace() ) and
            ( stars != float(0) ) 
            ):
            my_dict = OrderedDict()
            my_dict['id'] = file_id
            my_dict['title'] = movie_title
            my_dict['director'] = movie_director
            my_dict['stars'] = movie_stars[:-2]
            my_dict['description'] = movie_description
            my_dict['rating'] = stars
            my_dict['genre'] = movie_genre
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

    document = ET.Element("doc", docname=str(item["id"]))
    content = ET.SubElement(document, "content")
    ET.SubElement(content, "id").text = str(item['id'])
    ET.SubElement(content, "title").text = item['title']
    ET.SubElement(content, "director").text = item['director']
    ET.SubElement(content, "stars").text = item['stars']
    ET.SubElement(content, "description").text = item['description']
    ET.SubElement(content, "rating").text = str(item['rating'])
    ET.SubElement(content, "genre").text = item['genre']
    tree = ET.ElementTree(document)
    file_name = "corpus/{0}.xml".format(item['id'])
    tree.write(file_name, encoding="UTF-8", xml_declaration=True)
