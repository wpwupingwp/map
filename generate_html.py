#!/usr/bin/python3

from glob import glob

with open('list','r') as _:
    species_list = _.readlines()
species_list = [i.strip() for i in species_list]
genera = {i.split(' ')[0] for i in species_list}
genus_species = dict()
for i in species_list:
    genus = i.split(' ')[0]
    if genus not in genus_species:
        genus_species[genus] = [i, ]
    else:
        genus_species[genus].append(i)
with open('./template.html', 'r') as _:
    template = _.read()

title_template = '\t<h1>{genus}</h1>\n'
species_template = ('{name} (<a href="./png/{name}.png">png</a>|<a'
                    ' href="./svg/{name}.svg">svg</a>)\t')
content = ''
for i in genus_species:
    title = title_template.format(genus=i)
    species = '\t<p>'
    for j in genus_species[i]:
        species += species_template.format(name=j)
    species += '</p>\n'
    content = ' '.join([content, title, species])
with open('./index.html', 'w') as out:
    out.write(template.format(content=content))
