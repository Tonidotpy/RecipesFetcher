from DataClasses.RecipeIngredient      import RecipeIngredient
from DataClasses.RecipeModel           import RecipeModel
from DataClasses.RecipeSummary         import RecipeSummary
from DataClasses.RecipeNutritionalInfo import RecipeNutritionalInfo
from DataClasses.RecipePreparation     import RecipePreparation

import os
import re
import sys
import json
import base64
import requests
import threading
from utils import *
from bs4 import BeautifulSoup


DEBUG      = False
WRITE_LOG  = False
OVERWRITE  = False
PAGE_START = 389

# TODO: Refactoring
class RecipeFetcher:
    siteURL       = ""
    listName      = ""
    pageName      = ""
    numberOfPages = 0
    
    def __init__(self, siteURL, listName, pageName = "page"):
        self.siteURL  = siteURL
        self.listName = listName
        self.pageName = pageName
        self.CountTotalPages()
        
        if DEBUG:
            print(ForeColor.Apply("Link: ", ForeColor.OKBLUE + ForeColor.BOLD)
                  + ForeColor.Apply(siteURL + '/' + listName + '/' + pageName, ForeColor.OKGREEN + ForeColor.UNDERLINE))
            print()
    
    
    def SaveRecipe(self, link):        
        recipe = RecipeModel()
        
        if DEBUG:
            print(ForeColor.Apply("Page link: ", ForeColor.HEADER + ForeColor.BOLD)
                  + ForeColor.Apply(link, ForeColor.OKGREEN + ForeColor.UNDERLINE))
        
        soup   = self.DownloadPage(link)
        
        # Mispelled number in info
        if link == "https://ricette.giallozafferano.it/Cheesecake-cannolo.html":
            infoList = soup.find(attrs={ 'class' : 'gz-list-macros gz-move-content' })
            item = infoList.find(attrs={ 'class' : 'gz-list-macros-name' }, text=lambda s : "Saturi".lower() in s.lower()).parent
            item.find(attrs={ 'class' : 'gz-list-macros-value' }).string.replace_with("27.14")
        elif link == "https://ricette.giallozafferano.it/Cheesecake-al-pistacchio.html":
            infoList = soup.find(attrs={ 'class' : 'gz-list-macros gz-move-content' })
            item = infoList.find(attrs={ 'class' : 'gz-list-macros-name' }, text=lambda s : "Saturi".lower() in s.lower()).parent
            item.find(attrs={ 'class' : 'gz-list-macros-value' }).string.replace_with("24.33")
        elif link == "https://ricette.giallozafferano.it/Biscotti-con-farina-di-riso.html":
            infoList = soup.find(attrs={ 'class' : 'gz-list-macros gz-move-content' })
            item = infoList.find(attrs={ 'class' : 'gz-list-macros-name' }, text=lambda s : "Saturi".lower() in s.lower()).parent
            item.find(attrs={ 'class' : 'gz-list-macros-value' }).string.replace_with("3.91")
        elif link == "https://ricette.giallozafferano.it/Gnocchi-della-Val-Varaita.html":
            infoList = soup.find(attrs={ 'class' : 'gz-list-macros gz-move-content' })
            item = infoList.find(attrs={ 'class' : 'gz-list-macros-name' }, text=lambda s : "Saturi".lower() in s.lower()).parent
            item.find(attrs={ 'class' : 'gz-list-macros-value' }).string.replace_with("31.46")
        elif link == "https://ricette.giallozafferano.it/Agnello-in-umido.html":
            infoList = soup.find(attrs={ 'class' : 'gz-list-macros gz-move-content' })
            item = infoList.find(attrs={ 'class' : 'gz-list-macros-name' }, text=lambda s : "Saturi".lower() in s.lower()).parent
            item.find(attrs={ 'class' : 'gz-list-macros-value' }).string.replace_with("28.44")
        elif link == "https://ricette.giallozafferano.it/Sticky-rice.html":
            infoList = soup.find(attrs={ 'class' : 'gz-list-macros gz-move-content' })
            item = infoList.find(attrs={ 'class' : 'gz-list-macros-name' }, text=lambda s : "Saturi".lower() in s.lower()).parent
            item.find(attrs={ 'class' : 'gz-list-macros-value' }).string.replace_with("42.41")
        elif link == "https://ricette.giallozafferano.it/Mousse-al-caffe.html":
            infoList = soup.find(attrs={ 'class' : 'gz-list-macros gz-move-content' })
            item = infoList.find(attrs={ 'class' : 'gz-list-macros-name' }, text=lambda s : "Saturi".lower() in s.lower()).parent
            item.find(attrs={ 'class' : 'gz-list-macros-value' }).string.replace_with("40.28")
            
 
        recipe.title        = self.FindTitle(soup)
        if not OVERWRITE:
            filename = "Recipes/" + recipe.title.replace(" ", "_").lower() + ".json"
            if os.path.exists(filename):
                return
            
        recipe.image        = self.FindImage(soup)
        recipe.tags         = self.FindTags(soup)
        recipe.ingredients  = self.FindIngredients(soup)
        
        recipe.summary      = self.FindSummary(soup)
        recipe.info         = self.FindNutritionalInfo(soup)
        
        recipe.preparation  = self.FindPreparation(soup)
        recipe.preservation = self.FindPreservation(soup)
        recipe.advice       = self.FindAdvice(soup)
        
        self.CreateFileJson(recipe.toDictionary(), recipe.title)        

    def FindImage(self, soup):
        picture = soup.find('picture', attrs={ 'class' : 'gz-featured-image' })
        # Fallback:
        if picture is None:
            picture = soup.find('div', attrs={ 'class': 'gz-featured-image-video gz-type-photo' })
           
        if DEBUG:
            if picture is None:
                print(ForeColor.Apply("Picture not found!", ForeColor.FAIL))
                exit(1)
            
        imageSrc = picture.find('img')
        imageURL = imageSrc.get('data-src')
        # Fallback
        if imageURL is None:
            imageURL = imageSrc.get('src')
        
        if DEBUG:
            print(ForeColor.Apply("Image link: ", ForeColor.HEADER + ForeColor.BOLD)
                  + ForeColor.Apply(imageURL, ForeColor.OKGREEN + ForeColor.UNDERLINE))
        
        return ImageToBase64(imageURL)
    
    def FindTitle(self, soup):
        title = soup.find(attrs={ 'class' : 'gz-title-recipe gz-mBottom2x' }).text
        if DEBUG:
            print(ForeColor.Apply("Title: ", ForeColor.HEADER + ForeColor.BOLD) + ForeColor.Apply(title, ForeColor.HEADER))
            print()
        return title
    
    def FindTags(self, soup):
        tags = []
        tagsContainer = soup.find(attrs={ 'class' : 'gz-breadcrumb' })
        if DEBUG:
            print(ForeColor.Apply("Tags: ", ForeColor.OKBLUE + ForeColor.BOLD), end="")
        
        # Get all tags in list
        for tag in tagsContainer.find_all('a'):
            if DEBUG:
                if len(tags) > 0:
                    print(", ", end="")
                print(tag.string.lower(), end="")
            tags.append(tag.string.lower())
            
        # Get tags in summary if presents
        tagsContainer = soup.find(attrs={ 'class' : 'gz-list-featured-data-other' })
        if tagsContainer != None:
            for tag in tagsContainer.find_all(attrs={ 'class' : 'gz-name-featured-data-other' }):
                if DEBUG:
                    if len(tags) > 0:
                        print(", ", end="")
                    print(tag.string.lower(), end="")
                tags.append(tag.string.lower())
        else:
            if DEBUG:
                print(ForeColor.Apply("\nAdditional tags not found in summary", ForeColor.WARNING + ForeColor.BOLD))
            
        if DEBUG:
            print()
        return tags
    
    def FindIngredients(self, soup):
        ingredients = []
        if DEBUG:
            print(ForeColor.Apply(FormatStrings(("Ingredients", "name", "info", "quantity", "unit",), "%-20s%-30s%-50s%-10s%-10s"), ForeColor.HEADER + ForeColor.BOLD))
                
        for tag in soup.find_all(attrs={ 'class' : 'gz-ingredient' }):
            contents = tag.span.text.split()
            cLen = len(contents)
            ingredient = RecipeIngredient()
            ingredient.name = tag.a.text;
            info = []
            
            # Ingredients info, quantity and unit of measurement
            if cLen > 1:
                if IsFloat(contents[-1]):
                    if IsFraction(contents[-1]):
                        ingredient.quantity = FractToFloat(contents[-1])
                    else:
                        contents[-1] = contents[-1].replace(',', '.')
                        ingredient.quantity = float(contents[-1])
                    info     = contents[:-1]
                elif IsFloat(contents[-2]):
                    if IsFraction(contents[-2]):
                        ingredient.quantity = FractToFloat(contents[-2])
                    else:
                        contents[-2] = contents[-2].replace(',', '.')
                        ingredient.quantity = float(contents[-2])
                    info     = contents[:-2]
                    ingredient.unit     = contents[-1]
            elif cLen == 1:
                if IsFloat(contents[0]):
                    if IsFraction(contents[0]):
                        ingredient.quantity = FractToFloat(contents[0])
                    else:
                        contents[0] = contents[0].replace(',', '.')
                        ingredient.quantity = float(contents[0])
                else:
                    ingredient.quantity = contents[0]
            
            # Convert info to string
            info = ' '.join(info)
            ingredient.info = info

            if DEBUG:
                print(FormatStrings(("", ingredient.name, ingredient.info, ingredient.quantity, ingredient.unit,), "%-20s%-30s%-50s%-10s%-10s"))
            
            ingredients.append(ingredient)
            
        if DEBUG:
            print()
        return ingredients
    
    def FindSummary(self, soup):
        summary = RecipeSummary()
                
        contents = soup.find(attrs={ 'class' : 'gz-featured-data-recipe gz-recipe-summary' })
        for tag in contents.find_all('span', attrs={ 'class' : 'gz-name-featured-data' }):
            # Get summary item name and value separately
            name = tag.text.rpartition(':')[0].lower()
            val  = tag.strong.text
            
                        
            if "difficoltà" in name:
                summary.difficulty = val
            elif "preparazione" in name:
                # Convert preparation time string to seconds
                summary.preparationTime = StrToSeconds(val)
            elif "cottura" in name:
                # Convert cooking time string to seconds
                summary.cookingTime = StrToSeconds(val)
            elif "dosi" in name:
                # Get doses in format '[number] [unit]'
                p = val.split(' ')
                summary.doses = [int(p[0])]
                if len(p) > 1:
                    summary.doses.append(' '.join([e for e in p[1:]]))
            elif "costo" in name:
                summary.cost = val
            # Notes are in different format
            elif "nota" in tag.strong.text.lower():
                summary.notes = tag.text.split(' ', 1)[1]
        
            
        if DEBUG:
            print(ForeColor.Apply("Summary" , ForeColor.HEADER + ForeColor.BOLD))
            print(ForeColor.Apply(FormatStrings(("Difficulty: " ), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + summary.difficulty)
            print(ForeColor.Apply(FormatStrings(("Preparation: "), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + str(summary.preparationTime))
            print(ForeColor.Apply(FormatStrings(("Cooking: "    ), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + str(summary.cookingTime))
            print(ForeColor.Apply(FormatStrings(("Doses: "      ), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + ' '.join([str(e) for e in summary.doses]))
            print(ForeColor.Apply(FormatStrings(("Cost: "       ), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + summary.cost)
            if summary.notes:
                print(ForeColor.Apply(FormatStrings(("Notes: "), "%-20s")   , ForeColor.OKBLUE + ForeColor.BOLD) + summary.notes)
            print()
            
        return summary
    
    # Return the info based on the name from the list if present, otherwise return None
    def FindInfo(self, infoList, name):
        item = infoList.find(attrs={ 'class' : 'gz-list-macros-name' }, text=lambda s : name.lower() in s.lower())
        if item is None:
            if DEBUG:
                print(ForeColor.Apply("Missing '" + name.lower() + "' info!", ForeColor.WARNING + ForeColor.BOLD))
            return None
        
        li = item.parent
        res = [float(li.find(attrs={ 'class' : 'gz-list-macros-value' }).text),
               li.find(attrs={ 'class', 'gz-list-macros-unit' }).text]
        
        return res
            
    def FindNutritionalInfo(self, soup):
        info = RecipeNutritionalInfo()
        
        # Get nutritional information list if present
        infoList = soup.find(attrs={ 'class' : 'gz-list-macros gz-move-content' })
        if infoList is None:
            if DEBUG:
                print(ForeColor.Apply("Missing nutritional info!", ForeColor.WARNING + ForeColor.BOLD))
                print()
            return None

        l = infoList.find('ul')
        info.energy        = self.FindInfo(l, "Energia")
        info.carbohydrates = self.FindInfo(l, "Carboidrati")
        info.sugars        = self.FindInfo(l, "Zuccheri")
        info.proteins      = self.FindInfo(l, "Proteine")
        info.fat           = self.FindInfo(l, "Grassi")
        info.saturated     = self.FindInfo(l, "Saturi")
        info.fiber         = self.FindInfo(l, "Fibre")
        info.cholesterol   = self.FindInfo(l, "Colesterolo")
        info.sodium        = self.FindInfo(l, "Sodio")
        
        if DEBUG:
            print(ForeColor.Apply(FormatStrings(("Nutritional info", "value", "unit",), "%-20s%-10s%-10s"), ForeColor.HEADER + ForeColor.BOLD))
            print(ForeColor.Apply(FormatStrings(("Energy: ")       , "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.energy]       ), "%-10s%-10s")) if info.energy        != None else ""
            print(ForeColor.Apply(FormatStrings(("Carbohydrates: "), "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.carbohydrates]), "%-10s%-10s")) if info.carbohydrates != None else ""
            print(ForeColor.Apply(FormatStrings(("Sugars: ")       , "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.sugars]       ), "%-10s%-10s")) if info.sugars        != None else ""
            print(ForeColor.Apply(FormatStrings(("Proteins: ")     , "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.proteins]     ), "%-10s%-10s")) if info.proteins      != None else ""
            print(ForeColor.Apply(FormatStrings(("Fat: ")          , "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.fat]          ), "%-10s%-10s")) if info.fat           != None else ""
            print(ForeColor.Apply(FormatStrings(("Saturated: ")    , "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.saturated]    ), "%-10s%-10s")) if info.saturated     != None else ""
            print(ForeColor.Apply(FormatStrings(("Fiber: ")        , "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.fiber]        ), "%-10s%-10s")) if info.fiber         != None else ""
            print(ForeColor.Apply(FormatStrings(("Cholesterol: ")  , "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.cholesterol]  ), "%-10s%-10s")) if info.cholesterol   != None else ""
            print(ForeColor.Apply(FormatStrings(("Sodium: ")       , "%-20s") , ForeColor.OKBLUE + ForeColor.BOLD) + FormatStrings(tuple([str(e) for e in info.sodium]       ), "%-10s%-10s")) if info.sodium        != None else ""
            print()
            
        return info
    
    def FindPreparation(self, soup):
        prep = RecipePreparation()
        prep.images = []
        prep.text   = []

        # Preparation steps
        for step in soup.find_all(attrs={ 'class' : 'gz-content-recipe-step' }):
            prep.totSteps += 1
            
            # Step images if presents
            imageSrc = step.find('img')
            if imageSrc != None:
                imageURL = imageSrc.get('data-src')

                # Fallback
                if imageURL is None:
                    imageURL = imageSrc.get('src')
                    
                # Add site URL if image link is a local path
                if imageURL[0:4] != "http":
                    imageURL = self.siteURL + imageURL
                
                if DEBUG:
                    if imageURL is None:
                        print(ForeColor.Apply("Missing " + prep.totSteps + "° step images!", ForeColor.WARNING))
                
                if imageURL != None:
                    prep.images.append(imageURL)
            else:
                print(ForeColor.Apply("Missing preparation images!", ForeColor.WARNING + ForeColor.BOLD))
                
            # Step text
            [ s.replace_with("[" + s.string + "]") for s in step.find_all(attrs={ 'class' : 'num-step' }) ]
            prep.text.append( re.sub("[\n]+", "\n", ''.join(step.find_all(text=True))).lstrip("\n") )
            
        if DEBUG:
            print(ForeColor.Apply(FormatStrings(("Recipe preparation"), "%-20s"), ForeColor.HEADER + ForeColor.BOLD))
            print(ForeColor.Apply(FormatStrings(("Number of steps: " ), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + str(prep.totSteps))
            print(ForeColor.Apply(FormatStrings(("Number of images: "), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + str(len(prep.images)))
            print(ForeColor.Apply(FormatStrings(("Text length: "     ), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + str(len(' '.join(prep.text))))
            print()
        
        return prep
            
    def FindPreservation(self, soup):
        # Find preservation section
        header = soup.find('h2', text=lambda s : "Conservazione".lower() in s.lower())
        if header is None:
            if DEBUG:
                print(ForeColor.Apply("Missing preservation section!", ForeColor.WARNING + ForeColor.BOLD))
            return None
        
        text = re.sub("[\n]+", "\n", ''.join(header.find_next(attrs={ 'class' : 'gz-text-expanded' }).find_all(text=True)) ).lstrip("\n")
        if DEBUG:
            print(ForeColor.Apply(FormatStrings(("Preservation text length: "), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + str(len(text)))
        return text
    
    def FindAdvice(self, soup):
        # Find advice section
        header = soup.find('h2', text=lambda s : "Consiglio".lower() in s.lower())
        if header is None:
            if DEBUG:
                print(ForeColor.Apply("Missing advice section!", ForeColor.WARNING + ForeColor.BOLD))
                print()
            return None
        
        text = re.sub("[\n]+", "\n", ''.join(header.find_next(attrs={ 'class' : 'gz-text-expanded' }).find_all(text=True)) ).lstrip("\n")
        if DEBUG:
            print(ForeColor.Apply(FormatStrings(("Advice text length: "), "%-20s"), ForeColor.OKBLUE + ForeColor.BOLD) + str(len(text)))
            print()
        return text
    
    
    def CreateFileJson(self, recipe, name):
        compactName = name.replace(" ", "_").lower()
        folderRecipes = "Recipes"
        
        if DEBUG:
            print(ForeColor.Apply("Name: "    , ForeColor.OKBLUE + ForeColor.BOLD) + name)
            print(ForeColor.Apply("Filename: ", ForeColor.OKBLUE + ForeColor.BOLD) + compactName)
            print()
        
        fileName = folderRecipes + '/' + compactName + '.json'
        
        if not os.path.exists(folderRecipes):
            os.makedirs(folderRecipes)
        with open(fileName, 'w') as file:
            file.write(json.dumps(recipe, indent=4, ensure_ascii=False))
    
    def CountTotalPages(self):
        link = self.siteURL + '/' + self.listName
        soup = self.DownloadPage(link)
        self.numberOfPages = int(soup.find(attrs = { 'class' : 'disabled total-pages' }).text)
        if DEBUG:
            print(ForeColor.Apply("Number of pages: ", ForeColor.OKBLUE + ForeColor.BOLD) + ForeColor.Apply(str(self.numberOfPages), ForeColor.BOLD))
        return self.numberOfPages
    
    def DownloadPage(self, link):
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        if DEBUG and soup == '':
            print(ForeColor.Apply("Error 404: page not found!", ForeColor.FAIL + ForeColor.BOLD))
            exit(1)
        return soup
    
    
    loadAnimation = "─\\│/"
    loadTitle = ""
    loadValue = 1
    loadTotal = 1
    loadbarLength = 50
    def PrintProgress(self, index):

        if self.loadValue < 0:
            StdPrint(ForeColor.Apply(" [✗]  ", ForeColor.FAIL + ForeColor.BOLD), end="")
            StdPrint(ForeColor.Apply(FormatStrings(("Error!"), "%-15s"), ForeColor.FAIL + ForeColor.BOLD))
            return
        elif self.loadValue == 0 or self.loadValue >= self.loadTotal:
            StdPrint(ForeColor.Apply(" [✓]  ", ForeColor.OKGREEN + ForeColor.BOLD), end="")
            StdPrint(ForeColor.Apply(FormatStrings(("Finished!"), "%-15s"), ForeColor.OKGREEN + ForeColor.BOLD), end="")
            StdPrint(ForeColor.Apply((self.loadbarLength * "█"), ForeColor.BOLD), end="")
            StdPrint(ForeColor.Apply(" 100.0%", ForeColor.OKGREEN))
            return
        
        threading.Timer(1.0, self.PrintProgress, [(index + 1) % 4]).start()
        
        percentage = self.loadValue * 100.0 / float(self.loadTotal)
        barVal = self.loadValue * self.loadbarLength // self.loadTotal
        StdPrint(ForeColor.Apply(" [" + self.loadAnimation[index] + "]  ", ForeColor.WARNING + ForeColor.BOLD), end="")
        StdPrint(ForeColor.Apply(FormatStrings((self.loadTitle + "  "), "%-15s"), ForeColor.HEADER + ForeColor.BOLD), end="")
        StdPrint(ForeColor.Apply((barVal * "█"), ForeColor.BOLD), end="")
        StdPrint(ForeColor.Apply(((self.loadbarLength - barVal) * "░"), ForeColor.BOLD), end="")
        StdPrint(ForeColor.Apply(" " + FormatStrings((str(round(percentage, 1))), "%5s") + "%", ForeColor.WARNING), end="")
        StdPrint("\r", end="")

    def FetchRecipes(self, fetchLimit=-1):
        steps = 0
        
        self.loadTitle = "Starting..."
        self.loadValue = max(1, PAGE_START) * 15
        self.loadTotal = (self.numberOfPages + 1) * 15
        self.PrintProgress(0)
        
        try:
            for page in range(max(1, PAGE_START), self.numberOfPages + 1):
                self.loadTitle = "Page " + str(page)
                if DEBUG:
                    print(ForeColor.Apply("Page " + str(page), ForeColor.OKCYAN + ForeColor.BOLD))
                    print()
                
                link = self.siteURL + '/' + self.listName + '/' + self.pageName + str(page)
                soup = self.DownloadPage(link)
                
                i = 0
                for tag in soup.find_all(attrs = { 'class' : 'gz-title' }):
                    pageLink = tag.a.get('href')                
                    self.SaveRecipe(pageLink)
                    
                    i += 1
                    if fetchLimit >= 0 and i >= fetchLimit:
                        return
                    
                    if DEBUG:
                        if steps > 0:
                            steps -= 1
                        elif steps == 0:                            
                            s = input(ForeColor.Apply(ForeColor.Apply("Continue?", ForeColor.OKCYAN) + " ["
                                                    + ForeColor.Apply("'y'", ForeColor.OKGREEN) + ", "
                                                    + ForeColor.Apply("'n'", ForeColor.FAIL) + ", "
                                                    + ForeColor.Apply("steps", ForeColor.WARNING) + "]: ",
                                    ForeColor.BOLD))
                            if IsInt(s):
                                steps = int(s)
                            elif s[0].lower() != 'y':
                                return
                            print("\n")
                    self.loadValue += 1
                    
            self.loadValue = 0
        except Exception as e:
            if DEBUG:
                print(ForeColor.Apply("\n" + str(e), ForeColor.FAIL))
            self.loadValue = -1
            exit(1)

if __name__ == '__main__':
    
    if DEBUG and WRITE_LOG:
        sys.stdout = open('RecipeFetcher.log', 'w')
    
    fetcher = RecipeFetcher("https://www.giallozafferano.it", "ricette-cat", "page")
    # fetcher.SaveRecipe("https://ricette.giallozafferano.it/Cheesecake-cannolo.html")
    # fetcher.FindPreparation(fetcher.DownloadPage("https://ricette.giallozafferano.it/Lievito-madre.html")) # TODO: Sistemare la preparazione per il lievito madre
    fetcher.FetchRecipes()

    if DEBUG and WRITE_LOG:
        sys.stdout.close()
