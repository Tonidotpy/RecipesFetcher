# Model of the summary of the recipe
# Difficulty: difficulty of the preparation of the recipe (from very easy to very hard)
# Preparation time: time needed for the preparation of the recipe (in seconds)
# Cooking time: time needed for cooking (in seconds)
# Doses: list of 2 elements representing the doses of the recipe
#        the first element is the value of the doses
#        the second element is the unit of measurement of the doses
# Cost: cost of the recipe (from very cheap to very expensive)
# Notes: additional notes about the recipe
class RecipeSummary:
    difficulty       = ""
    preparationTime  = 0
    cookingTime      = 0
    doses            = []
    cost             = ""
    notes            = ""

    def __init__(self):
        difficulty       = ""
        preparationTime  = 0
        cookingTime      = 0
        doses            = []
        cost             = ""
        notes            = ""


    def toDictionary(self):
        summary = {
            "Difficulty"  : self.difficulty,
            "Preparation" : self.preparationTime,
            "Cooking"     : self.cookingTime,
            "Doses"       : self.doses,
            "Cost"        : self.cost,
            "Notes"       : self.notes
        }
        return summary