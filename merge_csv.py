import os
files = os.listdir('./csv/')

fd = ""
for f in files:
  if 'states' in f:
    print(f)
    language = f[:-11]
    with open('./csv/'+language+'-states.csv', 'r') as ff:
      data = ff.read()
      fd += language + "," + data + "\n"

with open('./csv/Language-states.csv', 'w+') as f:
  f.write(fd)