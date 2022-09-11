import tabula
import os
from PyPDF2 import PdfFileWriter, PdfFileReader

files = os.listdir('./pdf/')

states_languages = {
  'andaman_and_nicobar_Islands.pdf': ['English', 'Hindi'],
  'andhra_pradesh.pdf': ['English', 'Kannada', 'Odia', 'Telugu', 'Urdu'],
  'arunachal_pradesh.pdf': ['English'],
  'assam.pdf': ['Assamese', 'Bengali', 'Bodo', 'English', 'Garo', 'Hindi'],
  'bihar.pdf': ['English', 'Hindi', 'Urdu'],
  'chandigarh.pdf': ['English', 'Hindi'],
  'chhattisgarh.pdf': ['English', 'Hindi'],
  'dadra_nagar_daman_diu.pdf': ['English', 'Gujarati', 'Marathi'],
  'delhi.pdf': ['English', 'Hindi', 'Urdu'],
  'goa.pdf': ['English', 'Konkani', 'Marathi'],
  'gujarat.pdf': ['English', 'Gujarati', 'Hindi', 'Marathi', 'Urdu'],
  'haryana.pdf': ['English', 'Hindi'],
  'himachal_pradesh.pdf': ['English', 'Hindi'],
  'jammu_and_kashmir.pdf': ['English'],
  'jharkhand.pdf': ['Bengali', 'English', 'Hindi', 'Urdu'],
  'karnataka.pdf': ['English', 'Kannada', 'Marathi', 'Urdu'],
  'kerala.pdf': ['English', 'Kannada', 'Malayalam', 'Tamil'],
  'ladakh.pdf': ['English'],
  'lakshadweep.pdf': ['English'],
  'madhya_pradesh.pdf': ['English', 'Hindi', 'Marathi', 'Urdu'],
  'maharashtra.pdf': ['Bengali', 'English', 'Gujarati', 'Hindi', 'Kannada', 'Marathi', 'Urdu'],
  'manipur.pdf': ['English', 'Manipuri'],
  'meghalaya.pdf': ['Assamese', 'Bengali', 'English', 'Garo', 'Khasi'],
  'mizoram.pdf': ['English', 'Mizo'],
  'nagaland.pdf': ['English'],
  'odisha.pdf': ['English', 'Hindi', 'Odia', 'Urdu'],
  'puducherry.pdf': ['English'],
  'punjab.pdf': ['English', 'Hindi', 'Punjabi'],
  'rajasthan.pdf': ['English', 'Hindi'],
  'sikkim.pdf': ['English'],
  'tamil_nadu.pdf': ['English', 'Tamil', 'Urdu'],
  'telangana.pdf': ['English', 'Telugu', 'Urdu'],
  'tripura.pdf': ['Bengali', 'English'],
  'uttar_pradesh.pdf': ['English', 'Hindi', 'Urdu'],
  'uttarakhand.pdf': ['English', 'Hindi'],
  'west_bengal.pdf': ['Bengali', 'English', 'Hindi', 'Nepali', 'Urdu']
}
done = ["lakshadweep.pdf"]

for file in files:
  print(file)
  if file == ".DS_Store" or file == "national.pdf":
    continue
  # if file in done:
  #   continue
  inputpdf = PdfFileReader(open("./pdf/" + file, "rb"))
  
  start_page = 13
  for x in range(len(states_languages[file])):
    print(start_page)
    output = PdfFileWriter()
    for i in range(start_page,start_page+7):
      pageObj = inputpdf.getPage(i)
      output.addPage(pageObj)

    with open("./pdf_pages/temp.pdf", "wb") as outputStream:
      output.write(outputStream)

    ## convert PDF into CSV - Language
    areas = [[311.479,59.4,388.699,573.953],[280.294,60.885,402.064,568.755],[276.581,63.855,421.369,569.498],[264.701,63.113,428.051,566.528],[265.444,64.598,429.536,569.498],[286.976,64.598,367.166,566.528],[297.371,22.275,517.151,566.528]]

    fd = ""
    for pagenum in range(1, len(areas)):
      print("page: ", pagenum)
      df = tabula.read_pdf('./pdf_pages/temp.pdf', area=areas[pagenum-1], pages=[pagenum], lattice=True)
      df = df[0].to_csv(index=False)
      df = df.replace('\r', ' ')
      fd += df + "\n"

    # last page
    df = tabula.read_pdf('./pdf_pages/temp.pdf', area=areas[len(areas)-1], pages=[len(areas)], lattice=True)
    df = df[0].to_csv(index=False)
    df = df.replace('\r', ' ')
    df = df.replace(',Unnamed: 0', '')
    df = df.replace('Benchmark,', 'Benchmark,,')
    df = df.split('\n')
    df.pop(1)
    df.pop(-1)
    df[-1] = "," + df[-1][:-1]
    df = '\n'.join(df)
    fd += df + "\n"

    with open('./csv/' + file[:-4] + '-' + states_languages[file][x] + '.csv', 'w+') as f:
      f.write(fd)

    start_page += 7

