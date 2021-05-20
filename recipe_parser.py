import bs4, requests, pprint, re, sys, pyperclip, webbrowser, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

sys.argv
filename = ''
if len(sys.argv) != 0:
    filename = ' '.join(sys.argv[1:])
else:
    filename = pyperclip.paste()
print(filename)

url = 'http://www.google.com/search?q=' + filename + '+recipe'
print(url)

res = requests.get(url, headers=headers).text
soup = bs4.BeautifulSoup(res, 'lxml')

containers = []
for container in soup.findAll('a', href=True):
    containers.append(container['href'])

recipeURL = containers[9]
print(recipeURL)

recipeRes = requests.get(recipeURL)
recipeSoup = bs4.BeautifulSoup(recipeRes.text, 'html.parser')
elems = recipeSoup.select('h2, h3, h4, h5, h6')
header = recipeSoup.select('h1')

for item in elems:
    if item.text == 'Ingredients':
        ingredients = item.find_next(re.compile(r'[ou]l'))
    if item.text == 'Instructions' or item.text == 'Preparation':
        instructions = item.find_next(re.compile(r'[ou]l'))
    print(item.text)
    
ingr = []
for li in ingredients.find_all('li'):
    item = li.text.encode('ascii', 'ignore')
    item = item.decode('utf-8')
    ingr.append(item)

instr = []
for li in instructions.find_all('li'):
    item = li.text.encode('ascii', 'ignore')
    item = item.decode('utf-8')
    instr.append(item)

pprint.pprint(ingr)
pprint.pprint(instr)


file = open('C:\\Users\\maxho\\Documents\\Recipes\\' + filename + '.txt', 'w')
file.write(header[0].text + '\n\n')
file.write('Ingredients:\n')

for item in ingr:
    file.write('-' + item + '\n')

file.write('\nInstructions:\n')

for item in instr:
    file.write('-' + item + '\n')

file.close()
