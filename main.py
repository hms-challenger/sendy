import json
import requests
import pdfkit
import os
import shutil
from config import *

# logo
with open(("logo.txt"), 'r') as f:
        file_content = f.read()
        print(file_content)

i = 0
j = 0
offset = 0

print("Getting Ecwid Data...")
for i in range(4):
    i += 1
    response = requests.get("https://app.ecwid.com/api/v3/"+str(id)+"/orders?offset="+str(offset)+"&limit=100&token="+str(token))
    data = response.json()
    json_object = json.dumps(data, indent=4, ensure_ascii=False)
    with open("data"+str(i)+".json", "w") as outfile:
        outfile.write(json_object)
    offset += 100
    
  
count = 0

# set html template as infile and pdf as outfile
infile = "htmlTemplate.html"
outfile = "ecwidAddress.pdf"
header = "Hört Hin! GmbH | Wolbecker Str. 62 | 48155 Münster"
options = {
    'page-height': 36,
    'page-width': 89,
    'margin-top': '13px',
    'margin-right': '1px',
    'margin-bottom': '1px',
    'margin-left': '20px', 
    'encoding': "UTF-8", 
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'no-outline': None
    }

# main loop over downloaded json
for j in range(2):
    j += 1
    with open("data"+str(j)+".json", "r") as f:
        data = json.load(f)
        for ship_to_person in data['items']:
            if ship_to_person.get('paymentStatus') == "PAID" and ship_to_person.get('fulfillmentStatus') == "AWAITING_PROCESSING":

                if ship_to_person.get('companyName') != None:
                    companyName = ship_to_person.get('companyName')
                    name = "z.Hd.", ship_to_person.get('shippingPerson')['name']
                else:
                    companyName = ""
                    name = ship_to_person.get('shippingPerson')['name']

                street = ship_to_person.get('shippingPerson')['street']
                city = str(ship_to_person.get('shippingPerson')['postalCode'] + " " + ship_to_person.get('shippingPerson')['city'])

                with open(infile,'a') as f:
                    html = """
                    <html>
                    <head>
                        <title>address label</title>
                    </head>
                    <p style="color: rgb(130,130,130); font-family:Verdana, Arial, sans-serif; font-size: 13px">"""+header+"""</p>
                        <p style="color: black; font-family:Verdana, Arial, sans-serif; font-size: 20px">
                            <b>"""+name+"""</b><br>
                            """+street+"""<br>
                            """+city+"""<br><br>
                        </p>
                    </html>
                    """

                    comphtml = """
                    <html>
                    <head>
                        <title>address with company name label</title>
                    </head>
                    <p style="color: rgb(130,130,130); font-family:Verdana, Arial, sans-serif; font-size: 13px">"""+header+"""</p>
                        <p style="color: black; font-family:Verdana, Arial, sans-serif; font-size: 20px">
                            <b>"""+companyName+"""</b><br>
                            """+name+"""<br>
                            """+street+"""<br>
                            """+city+"""<br><br>
                        </p>
                    </html>
                    """
                    # write pdf file
                    if ship_to_person.get('companyName') != None:
                        f.write(comphtml)
                    else:
                        f.write(html)

                pdfkit.from_file(infile, outfile, options=options)

                count += 1
                print("Packages:", count, "| Name:", name)

f.close()

if count == 0:
    print("Packages:", count)
    try:
        os.remove("../" + ("data"+str(j)+".json"))
    except:
        print("no json available!")
else:
    try:
        shutil.move(("../" + outfile), ("../Desktop/" + outfile))
        os.remove("../" + infile)
        os.remove("../" + ("data"+str(j)+".json"))
    except:
        print("no files found")