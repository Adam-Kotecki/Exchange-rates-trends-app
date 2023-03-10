import requests
import json
import tkinter as tk
from tkinter import ttk
from tkinter import Entry
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
from datetime import datetime

root = tk.Tk()

root.geometry('400x500')
root.resizable(False, False)
root.title('Exchange rates trends app')
root.configure(bg="#e3e3cb")

image1 = Image.open("Great rate.png").resize((400, 100))
test = ImageTk.PhotoImage(image1)

label1 = ttk.Label(image=test)
label1.place(x = 0, y = 0)

label2 = ttk.Label(text="Select currency:", background="#e3e3cb")
label2.place(x=5 , y=120)

selected_currency = tk.StringVar()
currency = ttk.Combobox(root, textvariable=selected_currency)
currency['values'] = ('EUR', 'USD', 'CZK', 'JPY', 'AUD', 'GBP', 'UAH')
currency['state'] = 'readonly'
currency.place(x=5 , y=140)

label3 = ttk.Label(text="Start date:", background="#e3e3cb")
label3.place(x=5 , y=170)

date1 = tk.StringVar()
cal = DateEntry(root, width= 16, background= "green", foreground= "white",bd=2, textvariable=date1)
cal.place(x=5 , y=190)

label4 = ttk.Label(text="End date:", background="#e3e3cb")
label4.place(x=5 , y=220)

date2 = tk.StringVar()
cal2 = DateEntry(root, width= 16, background= "green", foreground= "white",bd=2,  textvariable=date2)
cal2.place(x=5 , y=240)

label5 = ttk.Label(text="Monotonicity of the sequence:", background="#e3e3cb")
label5.place(x=5 , y=270)

monotonicity = tk.StringVar()
mono = ttk.Combobox(root, textvariable=monotonicity)
mono['values'] = ('non-decreasing', 'non-increasing')
mono['state'] = 'readonly'
mono.place(x=5 , y=290)


def send_request():
    
    if selected_currency.get() == "":
        tk.messagebox.showinfo(message="Please select currency")
        return
    
    if monotonicity.get() == "":
        tk.messagebox.showinfo(message="Please select monotonicity")
        return
    
    date1 = datetime.strptime(str(cal.get_date()), "%Y-%m-%d")
    date2 = datetime.strptime(str(cal2.get_date()), "%Y-%m-%d")
    
    currency = selected_currency.get()
    start = str(date1).split()[0]
    end = str(date2).split()[0]
    mono = monotonicity.get()
    
    response = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/a/" + currency + "/" + start + "/" + end + "/")
    response.encoding='utf-8-sig'
    
    try:
        api = json.loads(response.text)
    except:
        tk.messagebox.showinfo(message="Please select different time range.")
        return
    
    exchange_rates = []
    
    for element in api['rates']:
        exchange_rates.append(element['effectiveDate'] + ": " + str(element['mid']))
        
    output = tk.Text(root, width= 22, height= 20, wrap= tk.WORD)
        
    
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
                
        output.place(x=200, y=120)
        
        for rate in longest:
            output.insert(tk.END, rate + "\n")
    
    
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
        
        output.place(x=200, y=120)

        for rate in longest:
            output.insert(tk.END, rate + "\n")
            
        if output.get("1.0", "end-1c") == "":
            output.insert(tk.END, "No sequence matching specified criteria. Please select different time range.")  
        
    if mono == "non-decreasing":
        non_decreasing_longest_sequence(exchange_rates)  
    else:
        non_increasing_longest_sequence(exchange_rates)
    
def help():
    tk.messagebox.showinfo(message="This app displays the longest exchange rates sequence of specified monotonicity, based on selected currency and date range. App uses NBP web API. Please note that in some cases not every date is covered, so the sequence may consist of non-consecutive dates.")

button = tk.Button(root, text="Submit", command=lambda: send_request(), width=10, bg="#7c9c84", fg="#e3e3cb", font=("ariel", 12, "bold") )
button.place(x=5, y=460)

button2 = tk.Button(root, text="Help", command=lambda: help(), width=10, bg="#7c9c84", fg="#e3e3cb", font=("ariel", 12, "bold") )
button2.place(x=285, y=460)

root.mainloop()