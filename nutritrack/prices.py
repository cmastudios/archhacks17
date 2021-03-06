import csv
import re
from fuzzywuzzy import process, fuzz


def _to_grams(value):
    m = re.search(r'(\d+) (.+)', value)
    if m is not None:
        number = int(m.group(1))
        unit = m.group(2)
        if unit == 'oz':
            return number * 30
        if unit == 'lbs':
            return number * 450
        if unit == 'fl oz':
            return number * 30
        if unit == 'gal':
            return number * 3785
    return None


def _to_money(value):
    m = re.search(r'\$(.+)', value)
    if m is not None:
        return float(m.group(1))
    else:
        return None


prices = {}
with open('prices.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        g = _to_grams(row[2].strip())
        d = _to_money(row[1].strip())
        if g is not None and d is not None:
            prices[row[0]] = {'unit': d / g, 'package': d}


def get_price(item: str):
    item = item.replace('ounces', '').replace('teaspoons', '').replace('teaspoon', '').replace('dash', '') \
        .replace('ounce', '').replace('tablespoons', '').replace('tablespoon', '').replace('oz', '').replace('cups', '').replace('cup', '')
    choices = prices.keys()
    result, confidence = process.extractOne(item, choices)
    if confidence < 70:
        return None

    o = prices[result]
    o['keyw'] = result
    return o
