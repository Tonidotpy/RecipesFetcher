from DataClasses.RecipeIngredient      import RecipeIngredient
from DataClasses.RecipeSummary         import RecipeSummary
from DataClasses.RecipeNutritionalInfo import RecipeNutritionalInfo
from DataClasses.RecipePreparation     import RecipePreparation

# Model for the recipe
# Image: image of the recipe converted to base64
# Title: name of the recipe
# Tags: categories to which the recipe belongs (e.g. "'primi piatti', 'dolci', ...")
# Ingredients: list of the ingredients
# Summary: summary of the recipe
# Info: nutritional information of the recipe
# Preparation: preparation of the recipe
# Preservation: advice on preserving the recipe
# Advice: general advice
class RecipeModel:
    image       = ""
    title       = ""
    tags        = []
    ingredients = []
    
    summary = RecipeSummary()
    info    = RecipeNutritionalInfo() 
    
    preparation  = RecipePreparation()
    preservation = ""
    advice       = ""

    def __init__(self):
        image       = ""
        title       = ""
        tags        = []
        ingredients = []
        
        summary = RecipeSummary()
        info    = RecipeNutritionalInfo() 
        
        preparation  = RecipePreparation()
        preservation = ""
        advice       = ""


    def toDictionary(self):
        recipe = {
            "Image"            : self.image,
            "Title"            : self.title,
            "Tags"             : self.tags,
            "Ingredients"      : [i.toDictionary() for i in self.ingredients],
            
            "Summary"          : self.summary.toDictionary(),
            "Nutritional Info" : None if self.info is None else self.info.toDictionary(),
            
            "Preparation"      : self.preparation.toDictionary(),
            "Preservation"     : self.preservation,
            "Advice"           : self.advice
        }
        return recipe
    