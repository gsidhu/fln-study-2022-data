import tabula
import os
from PyPDF2 import PdfFileWriter, PdfFileReader

# inputpdf = PdfFileReader(open("./pdf/national.pdf", "rb"))
# languages = ["Assamese", "Bengali", "Bodo", "English", "Garo", "Gujarati", "Hindi", "Kannada", "Khasi", "Konkani", "Malayalam", "Manipuri", "Marathi", "Mizo", "Nepali", "Odia", "Punjabi", "Tamil", "Telugu", "Urdu"]

# count = 0
# for i in range(11,70,3):
#   output = PdfFileWriter()
#   pageObj = inputpdf.getPage(i)
#   output.addPage(pageObj)
#   with open("./pdf_pages/%s.pdf" % languages[count], "wb") as outputStream:
#     output.write(outputStream)
#   count += 1

## convert PDF into CSV - Language States
files = os.listdir('./pdf_pages/')
for f in files:
  if f == ".DS_Store":
    continue
  print(f)
  language = f[:-4]
  
  try:
    df = tabula.read_pdf('./pdf_pages/' + language + '.pdf', area=[277.175,26.043,418.553,574.441], pages=1, stream=True)
    df = df[0].to_csv(index=False)
    df = df.replace('\r', ' ')
    df = df.replace('TAMILNADU', 'Tamil Nadu')
    df = df.split('\n')
    fd = ''.join(df[2:len(df)])
    fd = fd.replace('"', '')
    fd = fd.title()
    fd = fd.split(',')
    for i in range(len(fd)):
      fd[i] = fd[i].strip()
    fd = ', '.join(fd)
    with open('./csv/'+language+'-states.csv', 'w+') as f:
      f.write(fd)
  except:
    pass

# ## convert PDF into CSV - Language Tables
# files = os.listdir('./pdf_pages/')
# for f in files:
#   if f == ".DS_Store":
#     continue
#   print(f)
#   language = f[:-4]
  
#   try:
#     df = tabula.read_pdf('./pdf_pages/' + language + '.pdf', area=[230.297,26.043,466.919,569.232], pages=1, stream=True)
#     df = df[0].to_csv()
#     df = df.replace('\r', ' ')
#     df = df.replace(',,,', ',') 
#     df = df.split('\n')
#     df = [df[0], df[4], df[7],df[10]]
#     fd = language + ',' + ','.join(df[0].split(',')[2:6])
#     fd += "\nStudents," + ','.join(df[1].split(',')[2:6])
#     fd += "\nGirls," + ','.join(df[2].split(',')[2:6])
#     fd += "\nBoys," + ','.join(df[3].split(',')[2:6])
#     with open('./csv/'+language+'.csv', 'w+') as f:
#       f.write(fd)
#   except:
#     pass

fd = ''.join(df[2:len(df)])
fd = fd.replace('"', '')
fd = fd.title()
fd = fd.split(',')
for i in range(len(fd)):
  fd[i] = fd[i].strip()
fd = ', '.join(fd)