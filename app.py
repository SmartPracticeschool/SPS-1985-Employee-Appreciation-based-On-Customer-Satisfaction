from flask import Flask,render_template,url_for,request
import os
from credential_id import *
import boto3



app = Flask(__name__)
db = boto3.resource('dynamodb',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )
client = boto3.client('dynamodb',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )
table = db.Table("Employee_Feedback")
final_table = db.Table("Employee_count")#employee count table used for updating.(second table)
comprehend_client = boto3.client('comprehend',aws_access_key_id = access_key_id,aws_secret_access_key = secret_access_key,aws_session_token = session_token,region_name = region )

emp1 = final_table.get_item(
        Key={
            'emp_id':'Emp_001'
        }
    )
emp2 = final_table.get_item(
        Key={
            'emp_id':'Emp_002'
        }
    )
emp3 = final_table.get_item(
        Key={
            'emp_id':'Emp_003'
        }
    )

emp4 = final_table.get_item(
        Key={
            'emp_id':'Emp_004'
        }
    )
emp5 = final_table.get_item(
        Key={
            'emp_id':'Emp_005'
        }
    )

emp1_reviews = emp1["Item"]['no_of_reviews']
emp2_reviews = emp2["Item"]['no_of_reviews']
emp3_reviews = emp3["Item"]['no_of_reviews']
emp4_reviews = emp4["Item"]['no_of_reviews']
emp5_reviews = emp5["Item"]['no_of_reviews']

emp1_score = emp1["Item"]['score']
emp2_score = emp2["Item"]['score']
emp3_score = emp3["Item"]['score']
emp4_score = emp4["Item"]['score']
emp5_score = emp5["Item"]['score']

@app.route('/')
def index():

    


    return render_template('Customer_feedback.html',r1 = emp1_reviews,r2=emp2_reviews,r3=emp3_reviews,r4 = emp4_reviews,r5 = emp5_reviews,s1 = emp1_score,s2 = emp2_score,s3 = emp3_score,s4 = emp4_score,s5 = emp5_score)

@app.route('/',methods = ['POST','GET'])
def getvalue():
    customer_name = request.form['customer_name'] 
    employee_id = request.form['emp_id']
    feedback = request.form['feedback']
    
    if employee_id == 'Emp_001':
        employee_name = "Employee 1"
    elif employee_id == "Emp_002":
        employee_name = "Employee 2"
    elif employee_id == "Emp_003":
        employee_name = "Employee 3"
    elif employee_id == "Emp_004":
        employee_name = "Employee 4"
    elif employee_id == "Emp_005":
        employee_name = "Employee 5"
    
    print("The name ofthe customer :",customer_name)
    print("The employee id:",employee_id)
    print("The feedback is : ",feedback)
    print("The name of the employee : ",employee_name)

    
    ItemCount = client.describe_table(TableName='Employee_Feedback')
    no_of_item_in_employee_review = ItemCount['Table']['ItemCount']
    count = 33
    items = [count,customer_name,feedback,employee_id,employee_name]

    table.put_item(
        Item  = {
            'order_id':items[0],
            'customer_name':items[1],
            'feedback':items[2],
            'emp_id':items[3],
            'emp_name':items[4]
        }
        
    )
    
    #print("The number  of element in the first data base : ",ItemCount)

    
    
    get_employee_id = employee_id

    count_table_response = final_table.get_item(
        Key={
            'emp_id':get_employee_id
        }
    ) # it gives the responses of the Employee count table

    review_count = count_table_response["Item"]['no_of_reviews']  # second table
    score = count_table_response["Item"]['score'] # second table

    comprehend_response = comprehend_client.detect_sentiment(Text= feedback,LanguageCode="en")
    result = comprehend_response['Sentiment']
    
    if result == 'POSITIVE':
        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET no_of_reviews = :val1',
            
            ExpressionAttributeValues={
                ':val1' : review_count + 1
            }
        )
        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET score = :val2',
            
            ExpressionAttributeValues={
                ':val2' : score + 30
            }
        )

    elif (result == 'NEGATIVE'):
        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET no_of_reviews = :val1',
            
            ExpressionAttributeValues={
                ':val1' : review_count + 1,
            }

        )

        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET score = :val2',
            
            ExpressionAttributeValues={
                ':val2' : score - 15
            }
        )
        
    else:
        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET no_of_reviews = :val1',
            
            ExpressionAttributeValues={
                ':val1' : review_count + 1,
                
            }
        )

        final_table.update_item(
            Key={
                'emp_id':get_employee_id
            },
            UpdateExpression='SET score = :val2',
            
            ExpressionAttributeValues={
                ':val2' : score + 15
            }
        )
    print("Updated suceesfully")










    return render_template('Customer_feedback.html',r1 = emp1_reviews,r2=emp2_reviews,r3=emp3_reviews,r4 = emp4_reviews,r5 = emp5_reviews,s1 = emp1_score,s2 = emp2_score,s3 = emp3_score,s4 = emp4_score,s5 = emp5_score)


if __name__ == '__main__':
    app.run(debug= True)
