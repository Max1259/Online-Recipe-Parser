import bs4, requests, pprint, re, sys, pyperclip, webbrowser, lxml, docx, os

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

##sys.argv
##filename = ''
##if len(sys.argv) != 0:
##    filename = ' '.join(sys.argv[1:])
##else:
##    filename = input("Search for a recipe: ")
filename = input("Search for a recipe: ")

url = 'http://www.google.com/search?q=' + filename + '+recipe'

res = requests.get(url, headers=headers).text
soup = bs4.BeautifulSoup(res, 'lxml')

containers = []
for container in soup.findAll('a', href=True):
    containers.append(container['href'])

recipeURL = containers[9]

recipeRes = requests.get(recipeURL)
recipeSoup = bs4.BeautifulSoup(recipeRes.text, 'html.parser')
elems = recipeSoup.select('h2, h3, h4, h5, h6')
header = recipeSoup.select('h1')
ingredients = []
instructions = []

for item in elems:
    if item.text == 'Ingredients':
        ingredients = item.find_next(re.compile(r'[ou]l'))
    if item.text == 'Instructions' or item.text == 'Preparation' or item.text == 'Directions' or item.text == 'Method':
        instructions = item.find_next(re.compile(r'[ou]l'))

if len(ingredients) > 0: 
    ingr = []
    for li in ingredients.find_all('li'):
        item = li.text.encode('ascii', 'ignore')
        item = item.decode('utf-8')
        ingr.append(item.strip())

    if len(instructions) > 0:
        instr = []
        for li in instructions.find_all('li'):
            item = li.text.encode('ascii', 'ignore')
            item = item.decode('utf-8')
            item = item.strip()
            item = item.replace('\n', ' ')
            instr.append(item)
            
            

    pprint.pprint(ingr)
    pprint.pprint(instr)

    filepath = os.path.join(os.path.expandvars("%userprofile%"), "documents\\Recipes")

    if not os.path.isdir(filepath):
        os.mkdir(filepath)

    if os.path.isfile(filepath + '\\Recipes.docx'):
        doc = docx.Document(filepath + '\\Recipes.docx')
        doc.add_page_break()
    else:
        doc = docx.Document()
    
    file = open(filepath + '\\' + filename + '.txt', 'w')
    file.write(header[0].text + '\n')
    file.write(recipeURL + '\n')
    file.write('Ingredients:\n')

    doc.add_heading(header[0].text, 0)
    doc.add_paragraph(recipeURL + '\n\n')
    doc.add_heading('Ingredients:', 2)

    for item in ingr:
        file.write('-' + item + '\n')
        doc.add_paragraph(item, style='Bullet')

    file.write('\nInstructions:\n')
    doc.add_heading('\nInstructions:', 2)

    for item in instr:
        file.write('-' + item + '\n')
        doc.add_paragraph(item, style='Bulletalt')
        
    file.close()
    doc.save(filepath + '\\Recipes.docx')
    
else:
    print('No ingredients found, try again')
