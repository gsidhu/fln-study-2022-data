import tabula
import os
from PyPDF2 import PdfFileWriter, PdfFileReader

files = os.listdir('./pdf/')

numeracy_pages = {
  "andaman_and_nicobar_Islands.pdf" : 50,
  "andhra_pradesh.pdf" : 70,
  "arunachal_pradesh.pdf" : 42,
  "assam.pdf" : 78,
  "bihar.pdf" : 56,
  "chandigarh.pdf" : 50,
  "chhattisgarh.pdf" : 50,
  "dadra_nagar_daman_diu.pdf" : 56,
  "delhi.pdf" : 56,
  "goa.pdf" : 56,
  "gujarat.pdf" : 70,
  "haryana.pdf" : 50,
  "himachal_pradesh.pdf" : 50,
  "jammu_and_kashmir.pdf" : 42,
  "jharkhand.pdf" : 64,
  "karnataka.pdf" : 64,
  "kerala.pdf" : 64,
  "ladakh.pdf" : 42,
  "lakshadweep.pdf" : 42,
  "madhya_pradesh.pdf" : 64,
  "maharashtra.pdf" : 84,
  "manipur.pdf" : 50,
  "meghalaya.pdf" : 70,
  "mizoram.pdf" : 50,
  "nagaland.pdf" : 42,
  "odisha.pdf" : 64,
  "puducherry.pdf" : 42,
  "punjab.pdf" : 56,
  "rajasthan.pdf" : 50,
  "sikkim.pdf" : 42,
  "tamil_nadu.pdf" : 56,
  "telangana.pdf" : 56,
  "tripura.pdf" : 50,
  "uttar_pradesh.pdf" : 56,
  "uttarakhand.pdf" : 50,
  "west_bengal.pdf" : 70
}
done = ["lakshadweep.pdf","bihar.pdf","maharashtra.pdf","ladakh.pdf","haryana.pdf","telangana.pdf","kerala.pdf","andaman_and_nicobar_Islands.pdf","andhra_pradesh.pdf"]

for file in files:
  print(file)
  if file == ".DS_Store" or file == "national.pdf":
    continue
  if file in done:
    continue
  inputpdf = PdfFileReader(open("./pdf/" + file, "rb"))

  output = PdfFileWriter()
  for i in range(numeracy_pages[file],numeracy_pages[file]+14):
    pageObj = inputpdf.getPage(i)
    output.addPage(pageObj)

  with open("./pdf_pages/temp.pdf", "wb") as outputStream:
    output.write(outputStream)

  ## convert PDF into CSV - Language States
  areas = [[274.354,58.658,412.459,570.983],[277.324,64.598,416.171,570.983],[235.001,62.37,439.931,317.79],[213.469,62.37,445.871,320.018],[264.701,60.143,408.004,567.27],[266.186,60.143,405.034,568.013],[265.444,62.37,402.806,565.785],[263.959,62.37,403.549,568.013],[261.731,63.113,376.076,568.013],[262.474,63.113,407.261,566.528],[232.774,64.598,423.596,568.013],[258.019,59.4,406.519,565.785],[268.414,66.083,406.519,566.528],[297.371,24.503,486.709,569.498]]

  fd = ""
  for pagenum in range(1, len(areas)):
    print("page: ", pagenum)
    df = tabula.read_pdf('./pdf_pages/temp.pdf', area=areas[pagenum-1], pages=[pagenum], lattice=True)
    df = df[0].to_csv(index=False)
    df = df.replace('\r', ' ')
    fd += df + "\n"

  # last page
  df = tabula.read_pdf('./pdf_pages/temp.pdf', area=areas[13], pages=[14], lattice=True)
  df = df[0].to_csv(index=False)
  df = df.replace('\r', ' ')
  df = df.replace(',Unnamed: 0', '')
  df = df.replace('Benchmark,', 'Benchmark,,')
  df = df.split('\n')
  df.pop(1)
  df.pop(-1)
  df[-1] = "," + df[-1]
  df = '\n'.join(df)
  fd += df + "\n"

  with open('./csv/' + file[:-4] + '-numeracy.csv', 'w+') as f:
    f.write(fd)

