# Model for the ingredients of a recipe
# Name: the name of the ingredient (e.g. "'Milk', 'Egg', ...")
# Info: further information about the ingredient (e.g. "type, size, ...")
# Quantity: value of the quantity
# Unit: unit of measurement of the quantity
class RecipeIngredient:
    name     = ""
    info     = ""
    quantity = 0.0
    unit     = ""

    def __init__(self):
        name     = ""
        info     = ""
        quantity = 0.0
        unit     = ""


    def toDictionary(self):
        ingredient = {
            "Name"     : self.name,
            "Info"     : self.info,
            "Quantity" : self.quantity,
            "Unit"     : self.unit,
        }
        return ingredient