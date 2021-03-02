import re

term = 'tuesday search facebook'
title = re.findall("((?:.* search )(.*))|(.*)", term)[0][1]
print("-> " + str(title))