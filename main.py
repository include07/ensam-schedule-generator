from bs4 import BeautifulSoup
import camelot

table = camelot.read_pdf('emploi.pdf',pages = '1, 2, 3, 4, 5')

for i,p in enumerate(table, 1):
  p.to_html(f'page_{i}.html')

with open('all.html', 'a') as all:
  all.writelines(['<table border="1" class="dataframe">','<tbody>'])
  all_list = []
  for i in range(1,6):
    with open(f'page_{i}.html', 'r') as page:
      content = page.read()
      soup = BeautifulSoup(content, 'lxml')
      tr_elements = soup.findAll('tr')
      for tr in tr_elements:
        tr.th.decompose()
      all_list += soup.select('tbody tr')
  all_html = [tr.prettify() for tr in all_list]
  all.writelines(all_html)
  all.writelines(['</tbody>', '</table>'])

