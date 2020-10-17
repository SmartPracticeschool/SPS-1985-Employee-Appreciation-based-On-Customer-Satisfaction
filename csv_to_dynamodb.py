import boto3
from credential_id import *

db = boto3.resource('dynamodb',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )

items = [0,"Samuel","he doesnt come in the time. I have been waiting for a long time.","Emp_001","Employee 1"]

table = db.Table("Employee_Feedback")
table.put_item(
    Item  = {
        'order_id':items[0],
        'customer_name':items[1],
        'feedback':items[2],
        'emp_id':items[3],
        'emp_name':items[4]
    }
)
