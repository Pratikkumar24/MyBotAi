from PyDictionary import PyDictionary
import re
dic = PyDictionary()

# result = dic.meaning("telephone")
# print(result['Noun'])

query = " what does phsdfsf means "
useless = re.findall("(?:)(.*what)", query)[0]
query = query.replace(useless,"")
query = re.findall(r"(\w{3,})( means?)", query)[0][0]


print(query)
# dictionary=PyDictionary("hotel","ambush","nonchalant","perceptive")

# print()
# print("Printing the meaning:")
# print(dictionary.printMeanings()) 
# print("\nPrinting the meaning according to dictionary")
# print(dictionary.getMeanings()) 
# print("\nPrinting the Synonyms:")
# print (dictionary.getSynonyms())
# print("\nTranslating them in hindi:")
# print (dictionary.translateTo("hi"))
