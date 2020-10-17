import boto3
import csv

dynamodb = boto3.resource('dynamodb','us-east-1')

def batch_write(table_name,rows):
    table = dynamodb.Table(table_name)

    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(Items=row)
    return True

def read_csv(csv_file,list):
    rows = csv.DictReader(open(csv_file))

    for row in rows:
        list.append(row)

if __name__ == '__main__':

    table_name = 'Employee_Feedback'
    file_name = 'Employee_Feedback.csv'
    items = []

    read_csv(file_name, items)
    status = batch_write(table_name,items)

    if(status):
        print("Data is Saved")
    else:
        print("Error")