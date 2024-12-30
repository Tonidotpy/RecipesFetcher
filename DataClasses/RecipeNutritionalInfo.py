# Model for the nutritional info ot the recipe
# Each attribute of the class is a list of 2 values
# The first value is the value of the info
# The second value is the unit of measurement of the info
class RecipeNutritionalInfo:
    energy        = []
    carbohydrates = []
    sugars        = []
    proteins      = []
    fat           = []
    saturated     = []
    fiber         = []
    cholesterol   = []
    sodium        = []

    def __init__(self):
        energy        = []
        carbohydrates = []
        sugars        = []
        proteins      = []
        fat           = []
        saturated     = []
        fiber         = []
        cholesterol   = []
        sodium        = []


    def toDictionary(self):
        info = {
            "Energy"        : self.energy,
            "Carbohydrates" : self.carbohydrates,
            "Sugars"        : self.sugars,
            "Proteins"      : self.proteins,
            "Fat"           : self.fat,
            "Saturated"     : self.saturated,
            "Fiber"         : self.fiber,
            "Cholesterol"   : self.cholesterol,
            "Sodium"        : self.sodium
        }
        return info
