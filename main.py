from bs4 import BeautifulSoup
import camelot

def days_dictionary_generator(html_file_name):
  """
  this function takes the html file as an input, and returns the corresponding indices
  of each day in the week
  """
  days = {}
  with open(html_file_name, 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    tr_elements = soup.findAll('tr')
    i = 0
    days = {}
    while i < len(tr_elements):
      j = i
      day_cell = tr_elements[j].find('td').get_text(strip=True)
      i = i + 1
      while i < len(tr_elements) and tr_elements[i].find('td').get_text(strip=True) == "":
        i = i + 1
      days[day_cell] = (j, i-1)
  return days

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
      tr_elements = soup.select('tbody tr')
      for tr in tr_elements:
        tr.th.decompose()
      all_list += tr_elements
  all_html = [tr.prettify() for tr in all_list]
  all.writelines(all_html)
  all.writelines(['</tbody>', '</table>'])