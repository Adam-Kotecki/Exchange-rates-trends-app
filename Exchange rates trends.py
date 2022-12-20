import requests
import json


currency = input("Please provide currency: ")
start = str(input("Please provide start date (YYYY-MM-DD): "))
end = str(input("Please provide end date: (YYYY-MM-DD): "))
mono = input("type non-decreasing/non-increasing: ")


response = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/a/" + currency + "/" + start + "/" + end + "/")
response.encoding='utf-8-sig'
api = json.loads(response.text)

exchange_rates = []

for element in api['rates']:
    exchange_rates.append(element['effectiveDate'] + ": " + str(element['mid']))
    

def non_decreasing_longest_sequence(rates):
    possibly_longest = []
    longest = []
    
    for start in range(0, len(rates) -1):
        possibly_longest = []
        # range from 0 to 5 so last element with index 6 will never be compared to nonexisted one:
        for i in range(start, len(rates) -1):
            if float(exchange_rates[i][12:17]) <= float(exchange_rates[i+1][12:17]):
                possibly_longest.append(exchange_rates[i])
                # adding last element of list:
                if i+2 == len(rates):
                    possibly_longest.append(exchange_rates[i+1])
                else:
                    if not float(exchange_rates[i+1][12:17]) <= float(exchange_rates[i+2][12:17]):
                        possibly_longest.append(exchange_rates[i+1])
            else:
                break
        if len(possibly_longest) > len(longest):
            longest = possibly_longest
    
    print(longest)


def non_increasing_longest_sequence(rates):
    possibly_longest = []
    longest = []
    
    for start in range(0, len(rates) -1):
        possibly_longest = []
        # range from 0 to 5 so last element with index 6 will never be compared to nonexisted one:
        for i in range(start, len(rates) -1):
            if float(exchange_rates[i][12:17]) >= float(exchange_rates[i+1][12:17]):
                possibly_longest.append(exchange_rates[i])
                # adding last element of list:
                if i+2 == len(rates):
                    possibly_longest.append(exchange_rates[i+1])
                else:
                    if not float(exchange_rates[i+1][12:17]) >= float(exchange_rates[i+2][12:17]):
                        possibly_longest.append(exchange_rates[i+1])
            else:
                break
        if len(possibly_longest) > len(longest):
            longest = possibly_longest
    
    print(longest)
    
if mono == "non-decreasing":
    non_decreasing_longest_sequence(exchange_rates)  
else:
    non_increasing_longest_sequence(exchange_rates)
    
    
    