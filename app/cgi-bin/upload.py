#!/usr/bin/env python3

import io
import cgi
import zlib
import PIL.Image
import pyzbar.pyzbar
import base45
import cbor2
import pprint

print('Status: 200 OK')
print('Content-Type: text/plain; charset=utf-8')
print('')

form = cgi.FieldStorage()
pp = pprint.PrettyPrinter()

fileitem = form['pass']
if fileitem.filename:
  img = PIL.Image.open(io.BytesIO(fileitem.file.read()))
  data = pyzbar.pyzbar.decode(img)
  cert = data[0].data.decode()
  b45data = cert.replace("HC1:", "")
  zlibdata = base45.b45decode(b45data)
  cbordata = zlib.decompress(zlibdata)
  decoded = cbor2.loads(cbordata)
  results = cbor2.loads(decoded.value[2])

  pp.pprint(results)
