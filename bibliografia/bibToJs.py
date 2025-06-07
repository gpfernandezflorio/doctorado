import io, sys

def addAuthor(res, autores):
  res['autores'] = []
  for a in autores.split(' and '):
    autor = a.split(",")
    if len(autor) == 2:
      nombre = trim(autor[1])
      nombres = nombre.split(" ")
      if len(nombres) == 2:
        nombre = '["' + nombres[0] + '","'
        if len(nombres[1]) == 2 and nombres[1][1] == ".":
          nombre += nombres[1][0]
        else:
          nombre += nombres[1]
        nombre += '"]'
      res['autores'].append({
        'A':trim(autor[0]),
        'N':nombre
      })
    else:
      autor = trim(a).split(" ")
      if len(autor) == 2:
        res['autores'].append({
          'A':autor[1],
          'N':autor[0]
        })
      elif len(autor) == 3 and len(autor[1]) == 2 and autor[1][1] == ".":
        res['autores'].append({
          'A':autor[2],
          'N':'["' + autor[0] + '","' + autor[1][0] + '"]'
        })
      else:
        res['autores'].append({
          'A':trim(a),
          'N':trim(a)
        })

def addTitle(res, title):
  res['nombre'] = title

def addYear(res, año):
  res['año'] = numero(año)

def addJournalOrBook(res, journalOrBook):
  if 'en' in res:
    res['en']['T'] = journalOrBook
  else:
    res['en'] = {'T':journalOrBook}

def addVolume(res, v):
  nv = numero(v)
  if 'en' in res:
    res['en']['v'] = nv
  else:
    res['en'] = {'v':nv}

def addNumber(res, n):
  nn = numero(n)
  if 'en' in res:
    res['en']['n'] = nn
  else:
    res['en'] = {'n':nn}

def addArticleNo(res, n):
  nn = numero(n)
  if 'en' in res:
    res['en']['a'] = nn
  else:
    res['en'] = {'a':nn}

def addPages(res, p):
  if 'en' in res:
    res['en']['p'] = p
  else:
    res['en'] = {'p':p}

def addPublisher(res, p):
  res['editorial'] = p

def addEditor(res, p):
  if not ('en' in res):
    res['en'] = {}
  addAuthor(res['en'], p)

def addDoi(res, doi):
  res['doi'] = doi

def addISSN(res, issn):
  res['issn'] = issn

def addISBN(res, isbn):
  res['isbn'] = isbn

def addUrl(res, url):
  res['web'] = url

dictData = {
  'author':addAuthor,
  'title':addTitle,
  'year':addYear,
  'journal':addJournalOrBook,
  'booktitle':addJournalOrBook,
  'bookTitle':addJournalOrBook,
  'volume':addVolume,
  'number':addNumber,
  'articleno':addArticleNo,
  'pages':addPages,
  'publisher':addPublisher,
  'editor':addEditor,
  'ISSN':addISSN,
  'issn':addISSN,
  'ISBN':addISBN,
  'isbn':addISBN,
  'doi':addDoi,
  'URL':addUrl,
  'url':addUrl
}

def main(ruta):
  f = io.open(ruta, mode='r', encoding='utf-8')
  contenido = f.read()
  f.close()

  resultado = {}
  for linea in filter(lambda x : len(x) > 0, contenido.split('\n')):
    infoLinea = parseLinea(linea)
    if 'clave' in infoLinea and infoLinea['clave'] in dictData:
      dictData[infoLinea['clave']](resultado, infoLinea['dato'])
    elif 'clave' in infoLinea:
      print("WARN: clave " + infoLinea['clave'] + " no procesada")
  mostrar(resultado)

def parseLinea(linea):
  resultado = {}
  iEq = linea.find("=")
  if iEq < 0:
    print("WARN: no se encuentra un = en la línea: " + linea)
    return resultado
  clave = linea[0:iEq]
  dato = linea[iEq+1:]
  resultado['clave'] = trim(clave)
  resultado['dato'] = trim(dato)
  return resultado

def numero(n):
  try:
    x = int(n)
    return x
  except:
    pass
  return n

def trim(s):
  while len(s) > 0 and s[0] in ["{"," ","'",'"']:
    s = s[1:]
  i = len(s)-1
  while i > 0 and s[i] in [" ","}",",","'",'"']:
    i -= 1
  return s[:i+1]

listShow = [
  'nombre',
  'año',
  'autores',
  'en',
  'editorial',
  'isbn',
  'issn',
  'doi',
  'web'
]

def mostrarAutor(a):
  n = None
  s = None
  if 'N' in a:
    n = a['N']
    if not ('[' in n):
      n = '"' + n + '"'
  if 'A' in a:
    s = a['A']
    if not ('[' in s):
      s = '"' + s + '"'
  return '{A:' + s + ',N:' + n + '}'

listEn = [
  'T',
  'v',
  'n',
  'p',
  'autores',
  'editorial'
]

def mostrarEn(en):
  s = []
  for k in listEn:
    if k in en:
      s.append(k + ":" + ('"' + en[k] + '"' if type(en[k]) == type("") else ("[" + ','.join(map(mostrarAutor,en[k])) + "]" if type(en[k]) == type([]) else str(en[k]))))
  return "{" + ', '.join(s) + "}"

dictShow = {
  'nombre':(lambda x : f'"{x}"'),
  'año':str,
  'autores':(lambda x : "[" + ','.join(map(mostrarAutor,x)) + "]"),
  'en':mostrarEn,
  'editorial':(lambda x : f'"{x}"'),
  'isbn':(lambda x : f'"{x}"'),
  'issn':(lambda x : f'"{x}"'),
  'doi':(lambda x : f'"{x}"'),
  'web':(lambda x : f'"{x}"')
}

def mostrar(b):
  if 'editorial' in b and 'en' in b:
    b['en']['editorial'] = b['editorial']
    del b['editorial']
  s = []
  for k in listShow:
    if k in b:
      s.append(k + ": " + dictShow[k](b[k]))
  print(',\n            '.join(s))

if __name__ == '__main__':
  if len(sys.argv) == 1:
    print("No me pasaste ningún archivo")
    exit()
  main(sys.argv[1])