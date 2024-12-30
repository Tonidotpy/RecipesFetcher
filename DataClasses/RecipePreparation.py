# Model for the preparation steps of the recipe
# Tot steps: number of steps in the preparation of the recipe
# Images: list of image URLs
# Text: list of paragraphs
class RecipePreparation:
    totSteps = 0
    images   = []
    text     = []

    def __init__(self):
        totSteps = 0
        images   = []
        text     = []


    def toDictionary(self):
        prep = {
            "Steps"  : self.totSteps,
            "Images" : self.images,
            "Text"   : self.text
        }
        return prep