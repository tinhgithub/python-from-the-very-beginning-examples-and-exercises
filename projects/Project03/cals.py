#Mention in text that dictionaries are ordered -- update to Python 3.6
import sys
import os
import datetime

# List a file to screen
def table_of_file(filename):
    with open(filename) as f:
        table = {}
        for l in f.readlines():
            fields = l.split()
            if len(fields) == 0:
              print(f'malformed table in {filename}')
              return table
            else:
              key = fields[0]
              values = fields[1:]
              table[key] = values
        return table

# List the weights, or foods eaten for a day. List calories by calculation.
# cals list eaten <name> <date>
# cals list weights <name>
def list_eaten(name, date):
    for k, vs in table_of_file(os.path.join(name, date) + '.txt').items():
        print(f'{k} {vs[0]}')

def list_weights(name):
    for k, vs in table_of_file(os.path.join(name, 'weight.txt')).items():
        print(f'{k} {vs[0]}')
    
# List the dates for which we have calorie counts
# cals list dates
def list_dates(name):
    for filename in sorted(os.listdir(name)):
        if filename != 'weight.txt': print(filename[:-4])

# List the calorie data itself.
# cals list foods
def list_foods():
    for k, vs in table_of_file('calories.txt').items():
        print(k, end=' ')
        for v in vs: print(v, end=' ')
        print('')

# lookup a) calories for a type of food b) weight for a day. Today if missing.
# cals lookup calories <food>
# cals lookup weight <date>
def lookup_calories(food):
    table = table_of_file('calories.txt')
    vs = table[food]
    if vs == None:
        print(f'Food {food} not found')
    else:
        if len(vs) > 1:
            weight = vs[0]
            calories = vs[1]
            print(f'There are {calories} calories in {weight}g of {food}')
        else:
            print(f'Malformed calorie entry for {food} in calories file')

def lookup_weight(name, date):
    table = table_of_file(os.path.join(name, 'weight.txt'))
    vs = table[date]
    if vs == None:
        print(f'No weight found for {date}')
    elif len(vs) > 0:
        print(f'Weight at {date} was {vs[0]}')

# Print the total calories for just a given day.
# cals total <date>
def total_date(name, date):
    calories = table_of_file('calories.txt')
    table = table_of_file(os.path.join(name, date) + '.txt')
    total = 0
    for k, vs in table.items():
        print(f'food is {k}, grams is {vs[0]}')
        weight_and_calories = calories[k]
        reference_weight = int(weight_and_calories[0])
        reference_calories = int(weight_and_calories[1])
        calories_per_gram = reference_calories / reference_weight
        total += int(vs[0]) * calories_per_gram
    print(f'Total calories for {date}: {int(total)}')

# Create and initialise new user
# cals newuser <name>
def new_user(name):
    os.mkdir(name)
    with open(os.path.join(name, 'weight.txt'), 'w'):
        pass

def date_today():
   d = datetime.datetime.now()
   return (f'{d.day:02}-{d.month:02}-{d.year}')

# Add data for today - food and grams
# cals eaten <name> <food> <grams>
def eaten(name, food, grams):
    with open(os.path.join(name, date_today()) + '.txt', 'a') as f:
        print(f'{food} {grams}', file=f)

# Main program. Read args and dispatch.
if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if cmd == 'list':
        if len(sys.argv) > 3 and sys.argv[2] == 'eaten':
            list_eaten(sys.argv[3], sys.argv[4])
        else:
            if sys.argv[2] == 'weights' and len(sys.argv) > 3:
                list_weights(sys.argv[3])
            elif sys.argv[2] == 'dates' and len(sys.argv) > 3:
                list_dates(sys.argv[3])
            elif sys.argv[2] == 'foods':
                list_foods()
    elif cmd == 'lookup':
        if len(sys.argv) > 2:
            if sys.argv[2] == 'calories':
                lookup_calories(sys.argv[3])
            elif sys.argv[2] == 'weight' and len(sys.argv) > 3:
                lookup_weight(sys.argv[3], sys.argv[4])
    elif cmd == 'total':
        if len(sys.argv) > 3:
            total_date(sys.argv[2], sys.argv[3])
    elif cmd == 'newuser':
        if len(sys.argv) > 2:
            new_user(sys.argv[2])
    elif cmd == 'eaten':
        if len(sys.argv) > 4:
            eaten(sys.argv[2], sys.argv[3], sys.argv[4])
