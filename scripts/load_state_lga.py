import csv
from base.models import State, LGA

def run():
 
  f = open("utils/data.csv")
  reader = csv.reader(f)
  next(reader)
  
  
  for row in reader:
    state, created = State.objects.get_or_create(name=row[2])
    
    lga, created = LGA.objects.get_or_create(name=row[1], state=state)
    
  