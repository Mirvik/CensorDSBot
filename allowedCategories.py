import pandas as pd

badWords = pd.read_csv('trainData/badWords.csv')


class AllowedCategories:
    __allowed: set
    badWordsCategories = set(badWords['category_1'])
    
    def __init__(self, allowed: set):
        if (isinstance(allowed, set)):
            self.__allowed = allowed
        else:
            print("allowed should be set")
        
    def pushCategory(self, newCategory: str) -> bool: # True - success, False - error (category not exists)
        if newCategory not in AllowedCategories.badWordsCategories:
            return False
        
        self.__allowed.add(newCategory)
        return True
    
    def removeCategory(self, toRemove: str) -> bool: # True - success, False - category not in allowed
        if toRemove not in self.__allowed:
            return False
        
        self.__allowed.remove(toRemove)
        return True

    def getAllowedCategories(self) -> set:
        return self.__allowed
    
    def filterWords(self, offensiveWords: list) -> set | list:
        res = []
        if len(self.__allowed) == 0:
            return offensiveWords
        
        for word in offensiveWords:
            if word[1] in self.__allowed:
                res.append(word)

        return res
    
    def clear(self):
        self.__allowed.clear()