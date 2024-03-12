import json  #to work with json objects
import boto3 #client used to communicate with AWS services; 

def lambda_handler(event, context):

    print("MyEvent:") #created a seperate line for this text to easily see the event in the next line on CloudWatch
    print(event) #the data that is coming in

#   mycontext = event.get("context")
#   method = mycontext.get("http-method")
    method = event['context']['http-method']

    if method == "GET":
        dynamo_client = boto3.client('dynamodb')
        
        im_invoiceID = event['params']['querystring']['CustomerID']
        print(im_invoiceID)
        response = dynamo_client.get_item(TableName = 'Invoices', Key = {'InvoiceNo':{'N': im_invoiceID}})


        #im_customerID = event['params']['querystring']['CustomerID']
        #print(im_customerID)
        #response = dynamo_client.get_item(TableName = 'Customers', Key = {'CustomerID':{'N': im_customerID}})
        print(response['Item'])
        
        

        #myreturn = "This is where the status code is returned for the GET requests"

        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
           }

    elif method == "POST":

#       mystring = event['params']['querystring']['param1']
        p_record = event['body-json']
        recordstring = json.dumps(p_record)

        client = boto3.client('kinesis')
        response = client.put_record(
            StreamName='APIData',
            Data= recordstring,
            PartitionKey='string'
        )

        return {
            'statusCode': 200,
            'body': json.dumps(p_record)
        }
    else:
        return {
            'statusCode': 501,
            'body': json.dumps("Server Error")
        }
