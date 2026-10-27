from manual_reviews import load_reviews,summarize
from pathlib import Path
import json,tempfile
rows=load_reviews('data/customer-reviews.json',{'aida','aline-mota','diego','enzo','fernanda'})
assert summarize(rows,'diego')==(5,1)
assert summarize(rows,'enzo')==(5,1)
assert summarize(rows,'fernanda')==(3,1)
assert summarize(rows,'aida')==(5,1)
assert summarize(rows,'aline-mota')==(5,1)
assert summarize(rows,'marcio')==(None,0)
assert summarize(rows+[dict(rows[0],id='second',rating=3)],'diego')==(4,2)
for bad in [dict(rows[0],links=[{'label':'Teste','url':'javascript:alert(1)'}]),dict(rows[0],links=[{'label':'Teste','url':'https://user:pass@example.com/'}]),dict(rows[0],rating=6),dict(rows[0],rating=True),dict(rows[0],voice='unknown'),dict(rows[0],image='https://example.com/private.jpg')]:
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'reviews.json';p.write_text(json.dumps([bad]))
  try:load_reviews(p,{'aida','aline-mota','diego','enzo','fernanda'})
  except ValueError:pass
  else:raise AssertionError('Invalid review accepted')
print('PASS: original 5/5/3 scores, empty state, real aggregate mean, invalid data refused.')
