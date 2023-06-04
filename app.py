from flask import Flask
import json
from datetime import datetime

def format_date(date_str):
    date_string = date_str
    date_object = datetime.strptime(date_string, "%B %d, %Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    
    return formatted_date
      
def txt_to_json(txt_file_path, json_file_path):
    # Opening the text file in read mode
    with open(txt_file_path, 'r') as txt_file:
        # Reading the contents of the file
        txt_data = txt_file.read()

    # Spliting the data based on a delimiter or format of the text file
    # Assuming each line represents a separate record
    records = txt_data.split('\n')

    # Creating data structure to store the extracted data
    extracted_record = {}
    customer_data = {}
    delivery_details = {}
    line_item_list = []
    line_item_data = {}
    count1=0
    
    # Iterating over the records and extract and extracting relevant information
    for record in records:
        # Here, we split each record assuming it contains comma-separated values
        values = record.split(':')
        # track data rows
        count1 = count1 + 1
        
        if (count1 == 6):
            extracted_record['DeliveryNoteNo']=values[1][1:]
        
        if (count1 == 9):
            customer_data["Name"] = values[0]
        if (count1 == 10):
            customer_data["Address"] = values[0]
        if (count1 == 11):
            customer_data[values[0]] = values[1][1:]
            extracted_record['Customer']=customer_data
        
        if (count1 == 15):
            delivery_details["DeliveryDate"]= format_date(values[1][1:])
        if (count1 == 16):
            delivery_details["DeliveryAddress"]=values[1][1:]
        if (count1 == 17):
            delivery_details["VehicleNo"]=values[1][1:]
            extracted_record['DeliveryDetails']=delivery_details
            
        if "Item No" in values:
            line_item_data["ItemNo"] = values[1][1:4]
            temp_val=values[2][:-6]
            line_item_data["Description"] = temp_val[1:]
            temp_val2=values[3][:-10]
            line_item_data["Unit"] = temp_val2[1:]
            line_item_data["Quantity"] = int(values[4][1:])
            
            line_item_list.append(line_item_data)
            line_item_data = {}
            extracted_record["LineItems"] = line_item_list
        
    # Opening the JSON file in write mode
    with open(json_file_path, 'w') as json_file:
        # Converting the extracted data to JSON format and writing it to the file
        json.dump(extracted_record, json_file, indent=4)

app = Flask(__name__)

@app.route('/')
def index():
    # Specify the paths to your text file and the desired JSON file
    txt_file_path = 'data.txt'
    json_file_path = 'data.json'
    
    # Calling the function to convert the text file to JSON
    txt_to_json(txt_file_path, json_file_path)

    return ("Success")

if __name__ == '__main__':
    app.run()