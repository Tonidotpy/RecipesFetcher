import base64
import requests
import sys

class ForeColor:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    
    def Apply(s, col):
        return col + s + ForeColor.ENDC

# Print to original standard output (Usually a terminal)
def StdPrint(s, sep='', end="\n", flush=False):
    print(s, sep=sep, end=end, file=sys.__stdout__, flush=flush)

# Check if a string is an integer number
def IsInt(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

# Check if string is a unicode character fractions
def IsFraction(s):
    return s == "½" or s == "¼" or s == "¾" or s == "⅐" or s == "⅑" or s == "⅒" or s == "⅓" or s == "⅔" or s == "⅕" or s == "⅖" or s == "⅗" or s == "⅘" or s == "⅙" or s == "⅚" or s == "⅛" or s == "⅜" or s == "⅝" or s == "⅞"

# Check if a string is a floating point number (asserted format: 'x.y' or 'x,y' where 'x' and 'y' are integers)
def IsFloat(s):
    if IsFraction(s):
        return True
    
    num = s.replace(",", ".")
    integer, _, decimal = num.rpartition(".")
    if integer == "":
        return IsInt(decimal)
    
    # Decimal cannot be negative
    return IsInt(integer) and decimal.isdigit()

# Convert a fraction unicode characters to float
def FractToFloat(s):
    if s == "½":
        return 0.5
    if s == "¼":
        return 0.25
    if s == "¾":
        return 0.75
    if s == "⅐":
        return 1.0 / 7.0
    if s == "⅑":
        return 1.0 / 9.0
    if s == "⅒":
        return 0.1
    if s == "⅓":
        return 1.0 / 3.0
    if s == "⅔": 
        return 2.0 / 3.0
    if s == "⅕":
        return 0.2
    if s == "⅖":
        return 0.4
    if s == "⅗":
        return 0.6
    if s == "⅘":
        return 0.8
    if s == "⅙":
        return 1.0 / 6.0
    if s == "⅚":
        return 5.0 / 6.0
    if s == "⅛":
        return 0.125
    if s == "⅜":
        return 0.375
    if s == "⅝":
        return 0.625
    if s == "⅞":
        return 0.875
    return None

# Convert string to seconds (asserted format '[num] min', '[num] h')
def StrToSeconds(s):
    p = s.split(' ')
    seconds = int(p[0])
    if "min" in p[1]:
        seconds *= 60
    elif "h" in p[1]:
        seconds *= 3600
        
    return seconds

# Formats a tuple of strings
def FormatStrings(s, f):
    return f % s

def ImageToBase64(imageURL):
    image = str(base64.b64encode(requests.get(imageURL).content))
    # Remove byte string python prefix and suffix (e.g. b'image' -> image)
    image = image[2:len(image) - 1]
    return image