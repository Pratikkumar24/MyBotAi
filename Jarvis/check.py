
import re
query = "thursday search ddf"
title = re.findall("((?:.* search )(.*))|(.*)", query)[0][1]
if not len(title)>2:
    print("need to say")
else:
    print("-> " + title)