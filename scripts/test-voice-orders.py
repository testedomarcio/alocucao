from voice_orders import confirmed_counts
import runpy
rank=runpy.run_path('scripts/update-top-voices.py')['rank']
slugs={'aida','aline-mota','fernanda'}
assert confirmed_counts({'verified':False,'source':None,'counts':{}},slugs)=={}
assert confirmed_counts({'verified':True,'source':'Audited export','counts':{'aida':4}},slugs)=={'aida':4}
for counts in [{'unknown':2},{'aida':-1},{'aida':True},{'aida':1.2}]:
 try:confirmed_counts({'verified':True,'source':'Audited export','counts':counts},slugs)
 except ValueError:pass
 else:raise AssertionError('invalid count accepted')
voices=[{'slug':'aida','name':'Aida'},{'slug':'aline-mota','name':'Aline Mota'},{'slug':'fernanda','name':'Fernanda'}]
assert [r['voice'] for r in rank(voices,{'aida':2,'aline-mota':5,'fernanda':2})]==['aline-mota','aida','fernanda']
print('PASS: verified aggregates only, invalid totals refused, no private order records, deterministic ranking.')
