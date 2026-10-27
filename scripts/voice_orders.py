"""Read public aggregates from a verified order source; never expose order records."""
def confirmed_counts(data, slugs):
 if data.get('verified') is not True or not isinstance(data.get('source'),str) or not data['source'].strip():return {}
 counts=data.get('counts',{})
 if not isinstance(counts,dict):raise ValueError('Order counts must be an object')
 for voice,count in counts.items():
  if voice not in slugs or type(count) is not int or count<0:raise ValueError('Invalid delivered-order aggregate')
 return counts
