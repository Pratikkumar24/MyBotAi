from PyDictionary import PyDictionary

dictionary=PyDictionary("night","ambush","nonchalant","perceptive")

print("Printing the meaning:")
print(dictionary.printMeanings()) 
print("\nPrinting the meaning according to dictionary")
print(dictionary.getMeanings()) 
print("\nPrinting the Synonyms:")
print (dictionary.getSynonyms())
print("\nTranslating them in hindi:")
print (dictionary.translateTo("hi"))