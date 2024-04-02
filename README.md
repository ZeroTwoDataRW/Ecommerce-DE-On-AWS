# E-Commerce Data Engineering Project Using AWS

# Introduction & Goals
This project was a means to test my data engineering knowledge through the planning & construction of data pipelines, utilizing e-commerce data, with one the most popular webservices: Amazon Webservices (AWS). If you have no clue what I'm talking about 😂, then your in luck! This Github repo was specifically designed to explain exactly what data engineering is and it's purpose in the real world to readers with little technical knowledge.😉

## What Is the Purpose of Data Engineering?

Data Engineering is the process of making data usable for a business, by making it accessible for "data customers," such as BI Analysts, Data Analysts, Data Scientists, etc., who will ultimately analyze this data for business needs. Data customers are only able to access & analyze data, after a data engineer has built a system in which they can retrieve the data from. These systems, specifically referred to as "data pipelines," are an end-to-end process that ingest raw unorganized/organized data, process it, prepare it, store it, and finally visualize the data for the customers to use. I found that the best way to begin designing pipelines, is to begin by creating a blueprint. Below is a blueprint template for which data pipelines can be built upon.

![DS Blueprint](https://user-images.githubusercontent.com/74563990/159792405-7195ed58-7244-44a3-8b55-9719ba720d25.jpg)


## How Does The DS Blueprint Work

A DS Blueprint will always consist of five phases: 
* __Connect__: Databases, Datawarehouses, Web Apps, API's, or other sources that hold the data, are connected  data engineers can easily connect to these sources to ingest it for their pipelines 
* __Buffer__: a temporary holding area for data while it's waiting to be transferred to another location; developed in order to prevent data congestion from an incoming to an outgoing port of transfer
* __Processing__: collecting raw data and translating it into usable information; batch processing & real-time processing are two core processing methods
* __Store__: the location (database, datawarehouse, etc.) where the raw data will be held and the location of where the processed data will be held
* __Visualize__: the representation of data through use of common graphics, such as charts, plots, infographics, and even animations by software tools such as (Tabluea, PowerBI, etc.)


# Table of Contents

- [The Dataset](#the-dataset)
- [Platform Design](#platform-design)
  - [Connect](#connect)
  - [Buffer](#buffer)
  - [Processing](#processing)
  - [Storage](#storage)
  - [Visualization](#visualization)
- [Data Pipelines (Conceptual Planning)](#data-pipelines-(concepts))
  - [Data Ingestion Pipeline](#data-ingestion-pipeline)
  - [Stream To Raw Storage Pipeline](#stream-to-raw-storage-pipeline)
  - [Stream To DynamoDB Pipeline](#stream-to-dynamodb-pipeline)
  - [Visualization API Pipeline](#visualization-API-pipeline)
  - [Visualization Warehouse Pipeline](#visualization-warehouse-pipeline)
  - [Batch Processing Pipeline](#batch-processing-pipeline)
- [Building Ingestion Data Pipeline](#building-data-ingestion-pipeline)
- [Building Stream To Raw Storage Pipeline](#building-data-ingestion-pipeline)
- [Building Stream To DynamoDB Pipeline](#building-stream-to-dynamodb-pipeline)
- [Building Visualization API Pipeline](#building-visualization-api-pipeline)
- [Building Visualization Warehouse Pipeline](#building-visualization-warehouse-pipeline)
- [Building Batch Processing Pipeline](#building-batch-processing-pipeline)
- [Conclusion](#conclusion)
- [Follow Me On](#follow-me-on)


# The Dataset

## Selecting the Dataset
For this project I decided to select a dataset that would closely replicate data that I would work with at an actual company. Since this is my first project, I wanted to make sure to select a csv dataset (to reduce the number of columns that I had to work with) that wasn't too small or too large to handle. So after some browsing on Kaggle, I decided to select a e-commerce dataset that was 43MB in size. Some key factors that this dataset included were descriptive column names (which are much easier to work with if you are using a relational SQL database), customer id's, invoice number's, invoice date's, unit price, and product quantity.

Dataset Link: https://www.kaggle.com/carrie1/ecommerce-data

## Defining the Purpose of the Dataset
Before building a pipeline it is essential to understand what the business requires it for. Will the visualized data be used for business goals or business intelligence goals. Business goals can include processsing transactions from various stores in a single location or give customers access to his/her purchase history. Business intelligence goals can include obtaining data such as average sales, most sold products, and most valuable products per hour/day/month/year. Understanding what results you want you from the data is key to developing the optimal data pipeline.

## Storage Possibilities
The data can either be stored in a relational database or a NoSQL database. If we wanted to create relationships between the columns of data and that data is already strucutred, then it would make sense to use a relational database. Although if there are plans to scale (adding hundreds or thousands of columns to the dataset), then it would make more sense to develop a NoSQL database, so as to avoid the relational database from becoming too complex to understand. Although it would be optimal to design a relational database for this particular dataset, I plan to develop a NoSQL database for my dataset. I will ultimately create two tables. One table for Customer Purchase Overview (primary key would be the CustomerID; each column would hold a different InvoiceNO; each row would hold an amount & date) and another for Invoice Details (primary key would be the InvoiceNo; each column would hold a different Stock Code; each row would include Description, Quantity, & Unit Price). Creating a NoSQL database will prepare myself for having to develop databases at scale in the future.

<img src="https://user-images.githubusercontent.com/74563990/161163691-c65f0d7d-48d0-4a70-992f-2de6086070e0.png" width="600"/>

## Data Model

<img src="https://user-images.githubusercontent.com/74563990/161163550-a3cc584f-27d9-4ad8-a4f8-314ca9b48a33.png" width="350"/>

<img src="https://user-images.githubusercontent.com/74563990/161163569-a2131afe-32af-4bff-8c54-94c2e88dca83.png" width="350"/>

<br />

# Platform Design

## Selecting the Tools
In this section, we will look at the main components of our data pipeline, which model our DS Blueprint listed above.
<img src="https://user-images.githubusercontent.com/74563990/159989202-57605a99-9fe8-4e85-9958-135a6cd5604d.jpg" width="300"/>

## Client
Usually this doesn't need to be created because there would a system or device (a.k.a the client) that is going to send data to the API at a company. But in my case, since there isn't a device that can accomplish that task, I have created a Python Client using AWS SDK (Boto3) that takes the csv and it selects data either on a row basis, basis of number of lines, or date that is going to be sent to my API. The Python Client will also transform each of my rows into a JSON string before sending, becuase JSON is more of an organized format to analyze the data.

## Connect
My client is sending data to the API Gateway that is hosting a URL. Once the data is sent there, living in the background is a Lambda function that is getting triggered by the API Gateway and is processing the JSON that we have. Ultimately the Lambda function will send it into some system, such as a database or database buffer. In my case the data will be sent to a database buffer first.

<img src="https://user-images.githubusercontent.com/74563990/160052778-18b56aac-705b-4b5d-86b2-aea2b9f40389.png" width="600"/>

## Buffer
Kinesis, also known as a message queue (consist of two parts: a producer which sends data into the message queue and a consumer which takes data out of the message queue). In my case the producer is the Lambda function that sits behind the API Gateway becuase it is ultimately "producing" (or sending) my processed data into the message queue. On the consumer end can be either another Lambda function or a tool such as Kinesis firehose which takes the data back out.

<img src="https://user-images.githubusercontent.com/74563990/160053165-b92a0869-5ad5-48ae-bd11-67449cecdbd3.png" width="600"/>

## Processing
There are two ways of processing data. Stream processing or Batch processing.

Stream processing is a continuous process that begins with a <b>source</b> that is sending data into <b>processing</b>, in which then it is processed, and sent to it's <b>destination</b>. In my case the source would begin with Kinesis, that is sending data into the processing (Lambda function) and sends it into it's destination.

<img src="https://user-images.githubusercontent.com/74563990/160053624-b35b734d-9c72-40bb-9609-156f9f1a7a43.png" width="600"/>

Batch processing begins with the <b>scheduler</b> that activates the <b>processing</b>, which then connects to the data <b>source</b>, and ultimately writes it to it's <b>destination</b>. In my case the source would begin with a scheduler tool such as "CloudWatch" or "Airflow" that activates the processing (Lambda function), which then connects to the data source Kinesis and ultimately writes it to it's destination.

<img src="https://user-images.githubusercontent.com/74563990/160053663-e6eb5068-9b4a-405d-80c3-721763821f06.png" width="600"/>

## Store
For my file storage I'm going to use AWS S3 becuase it is widely used and simple to understand. For my NoSQL database, which is going to store my transactions, I'm going to use DynamoDB. For my analytical layer, I will be using the datawarehouse AWS Redshift, because it allows for distributed storage (which is great for data that scales).

## Visualize
For visualization purposes I will be using the business intelligence tool Tableau becuase it is popular and easily connects to AWS Redshift. 

<br />

# Data Pipelines (Concepts)

## Data Ingestion Pipeline
The Python Client is going to send csv rows as JSON into the API Gateway. The Lamda function will process the JSON file and send it into Kinesis.

<img src="https://user-images.githubusercontent.com/74563990/160485088-a7aeaa81-5bf1-4806-918d-e049332e72dd.png" width="600"/>

## Stream To Raw Storage Pipeline
Data that is lying in the Kinesis stream will trigger another Lambda function, which takes the data and dumps it into a S3 bucket. The main use case for this is to put data into a data lake or another storage that can be used later. 
*To prevent a lot of files from being dumped into the S3 bucket at one time, I configured the Lambda function to wait for a specified amount of time after each transaction. 

<img src="https://user-images.githubusercontent.com/74563990/160485547-57b446d5-4fa6-4998-aca9-b06d5b88a6c1.png" width="600"/>

## Stream To DynamoDB Pipeline
Kinesis insert triggers the Lambda function for DynamoDB. The Lambda is responsible for reformatting/preprocessing the data, writing the customer data (customer + invoices), and writing invoice data (invoice + stockcode)

<img src="https://user-images.githubusercontent.com/74563990/160489461-4ade4019-f8ad-4f7a-9e9a-d379904cf733.png" width="600"/>

## Visualization API Pipeline
Created an API as the client's UI. It is responsible for querying Items from an Invoice. Since the data rests in the DynamoDB table "Invoices," the client can request Items for the "InvoiceNo (request parameter)." Lambda triggered by the API queries Dynamo with InvoiceNo

<img src="https://user-images.githubusercontent.com/74563990/160490552-15de3b59-5474-4588-bfac-9305cfb8a9c3.png" width="600"/>

## Visualization Datawarehouse Pipeline
Kinesis Firehose Delivery Stream connects to the Kinesis Data Stream. Once connected, Kinesis Firehose stores data into an S3 Bucket for intermediate storage. Firehose then copies data from the Bucket into the Redshift Table. Once in Redshift, Tableau can connect and be open for analyst to use.

<img src="https://user-images.githubusercontent.com/74563990/160491466-bf878116-48c1-4616-a622-54b651b7f0be.png" width="600"/>

## Batch Processing Pipeline
A bulk of files will be stored in S3 and a Lambda function will take the data and move it into the DynamoDB tables or the Redshift table. Before all this can happen, Cloudwatch (a scheduler) will trigger the process.

<img src="https://user-images.githubusercontent.com/74563990/160494091-ac1fa5d1-2c85-4fae-9b5e-365fb7543903.png" width="600"/>


# Building Data Ingestion Pipeline

## Creating Lambda Functions
I created 3 Lamda functions using AWS Lamda. Those three are:
* Read-Write-To-Kinesis (USING THIS FUNCTION ONLY FOR INGESTION PIPELINE)
* Write-Kinesis-To-S3
* Write-To-DynamoDB

<img src="https://user-images.githubusercontent.com/74563990/161352691-f8c0d2f6-9a17-42a8-ac45-0c0897f2f76c.png" width="600"/>

## Setting Up Kinesis
Created a Kinesis Stream to take in my data named APIData

<img src="https://user-images.githubusercontent.com/74563990/161132891-1a48292a-4420-4e07-a606-07077a074827.png" width="600"/>

## Established IAM Roles For Function
Read-Write-To-Kinesis Roles:
* FULL ACCESS Read Functions to Kinesis
* Write Functions: PutRecord (write one request), PutRecords (write multiple request); Allowed writing access to APIData Kinesis Stream
<img src="https://user-images.githubusercontent.com/74563990/161111128-5c76e629-f2b8-4f74-a9a1-cb2781949201.png" width="600"/>

## Creating API Gateway
Created an API named "E-commerce", created a resource named "e-commerce", and created two HTTP methods: GET (to read the data from DynamoDB table later) & POST (to write the data to Kinesis) *What is a Resource? - consists of a url, an HTTP method, a response type, a JSON Schema describing the input(s) to the API Resource, and a JSON Schema describing the output

<img src="https://user-images.githubusercontent.com/74563990/161112549-07254b3a-4a45-4046-82dd-5c6409c992dc.png" width="600"/>

Set Mapping (API Gateway uses mapping templates to transform requests before they are sent)

<img src="https://user-images.githubusercontent.com/74563990/161141341-00eccce9-4f41-4d45-bafd-8f0dd27a36ec.png" width="600"/>

## Lamda Code
Developed Code for the Lambda Function where I create the Boto3 client and use an if/elif/else decision structure to decide what to do if it is a GET or POST request.

<img src="https://user-images.githubusercontent.com/74563990/161139810-2eda0049-8fea-4f96-b276-a207973186af.png" width="600"/>

Created a test event that mimicks the JSON that I want the output to display

<img src="https://user-images.githubusercontent.com/74563990/161140169-f8ef12cc-0c61-430b-91ca-c2dd8b8246b6.png" width="600"/>

## Python Script To Send Data
Created a python script which uses a for loop to iterate through my "TestSample" (which includes the first 9 rows of my csv file)

TestSample:

<img src="https://user-images.githubusercontent.com/74563990/161142153-e7b2f0c6-205d-44e5-9922-0c1ab2fcaeea.png" width="600"/>

Python Script:

<img src="https://user-images.githubusercontent.com/74563990/161141954-7acd3621-ddd5-4c78-9436-743dd21c704b.png" width="600"/>

## Testing the Pipeline
After running the Python Script, you can assume from the Response 200's that the data was sent into Kinesis as a JSON

<img src="https://user-images.githubusercontent.com/74563990/161142673-e50edc8c-0f13-4fd3-b7b0-6791d9e5c214.png" width="600"/>

But I wanted to make sure, so I checked the log in CloudWatch & Kinesis activity graph:

<img src="https://user-images.githubusercontent.com/74563990/161143420-6d77ba90-0488-495b-af12-f4c7d2071c32.png" width="600"/>

<img src="https://user-images.githubusercontent.com/74563990/161143732-d1baad15-24c6-448d-b002-26c763efe5e5.png" width="600"/>

# Building Stream To Raw Storage Pipeline

## Setup S3 bucket
Created an S3 bucket named e-comm bucket

## IAM Roles for Write-To-S3 Function
* FULL ACCESS to S3
* FULL ACCESS Read Functions to Kinesis

## Create Lambda Code for S3 Insert

<img src="https://user-images.githubusercontent.com/74563990/161152740-9c76804a-3e54-4181-a027-40fbd29af0c6.png" width="600"/>

## Testing the Pipeline
Enabled Kinesis to trigger APIData. Created a new test event called myS3TestEvent to test my code. Test result should return: "Hello, this is a test 123."

<img src="https://user-images.githubusercontent.com/74563990/161158444-de57a8c1-932a-4445-b6ef-16ee5f917402.png" width="600"/>

<img src="https://user-images.githubusercontent.com/74563990/161152988-b4a9ddf3-f1e9-411a-8abe-539ddc25b289.png" width="600"/>

<img src="https://user-images.githubusercontent.com/74563990/161154392-9b16feaa-3406-4a86-be35-305570db2341.png" width="600"/>

<img src="https://user-images.githubusercontent.com/74563990/161157086-6bab36cc-e953-4079-8f99-2ae47aa61c3f.png" width="600"/>

# Building Stream To DynamoDB Pipeline

## Setup DynamoDB
Created a Customers table with CustomerID & Invoices table with InvoiceID. I set to recieve one row at a time

<img src="https://user-images.githubusercontent.com/74563990/161165552-847a741d-ba82-414b-969f-1c4ee4d72c06.png" width="600"/>

## Setup IAM For DynamoDB Stream
What is update item? - *Update Item: new data is added to the end of the table and not replacing other data*

<img src="https://user-images.githubusercontent.com/74563990/161165691-5b8dccc1-b706-4aa0-b59a-2778bb6e35f9.png" width="600"/>

## Creating DynamoDB Lambda
Created Write-To-DynamoDB Lambda code. Then I run the same Python Script again to get data into DynamoDB

<img src="https://user-images.githubusercontent.com/74563990/161390781-c27406cc-b8b5-47f3-bd75-df5302ace148.png" width="600"/>

Python Script:

<img src="https://user-images.githubusercontent.com/74563990/161390624-b4603baf-60db-4722-8ad0-77aba56371db.png" width="600"/>

Customers Table:

<img src="https://user-images.githubusercontent.com/74563990/161400220-6137e625-6090-47d0-88df-e1ecd5aa7be4.png" width="600"/>

Invoices Table:

<img src="https://user-images.githubusercontent.com/74563990/161404185-c8ee48df-c706-4dba-a094-a5dd52394a36.png" width="600"/>

# Building Visualization API Pipeline

## Creating API & Lambda For Access
The Read-Write-To-Kinesis Lambda function also has a GET request method implemented, where the client requests the items for the InvoiceNo to get the description in the table.

<img src="https://user-images.githubusercontent.com/74563990/161403800-ec5c4317-b048-4148-91c0-a722d13e7b25.png" width="600"/>

## Tested API
I tested the API with Postman but can also use AWS querystring to quickly test the API. The format is not great but the Stock Codes are displayed within the body section, under the "Description" column name.

<img src="https://user-images.githubusercontent.com/74563990/161403763-42efd3a1-b6a0-49f3-bb0b-f61532546523.png" width="600"/>

# Building Visualization Warehouse Pipeline

## Create Redshift Datawarehouse
I created a cluster in Redshift called "redshift-firehose" which will recieve data from Kinesis firehose

## Setup IAM for Redshift
I attached the AmazonRedshiftAllCommandsFullAccess defualt policy. This policy includes permissions to run SQL commands to COPY, UNLOAD, and query data with Amazon Redshift. The policy also grants permissions to run SELECT statements for related services, such as Amazon S3, Amazon CloudWatch logs, Amazon SageMaker, and AWS Glue.

## Security Group for Firehose
This step is important to make sure that Firehose can actually send data into Redshift (becuase Redshift is in its on Virtual Private Cloud). To make sure I went to EC2 -> Security Groups -> clicked on the only security group that was listed. Then I clicked on "inbound rules" to make sure that all traffic was allowed (this means that all types of internet data can be sent through) and all ports were allowed. The "Source" was set to the US-east-1 VPC number indicated in the image below, because this is the service that I'm using. 

<img src="https://user-images.githubusercontent.com/74563990/161995434-75bd9428-89ed-4e11-87e0-e7514ed90a70.png" width="600"/>

<img src="https://user-images.githubusercontent.com/74563990/161990539-822bf182-95b2-45bd-8849-913d84fa3fcb.png" width="600"/>

## Create Redshift Tables
Created a table called "firehosetransactions" to hold the data

<img src="https://user-images.githubusercontent.com/74563990/162001840-244dfbb9-f40c-4219-a368-42a908135abb.png" width="600"/>

## S3 & JSON Paths
Created an S3 bucket named "firehoseredshift1" for temporary storage of my Kinesis Firehose Delivery Stream Data. I also added a file called "jsonpaths.json" to my bucket. This file is responsible for helping firehose to detect the objects (InvoiceNo, StockCode, etc.) within the string.

<img src="https://user-images.githubusercontent.com/74563990/162041507-53e1083a-f4ff-440e-b260-0f94243f7484.png" width="600"/>

## Configure Firehose
First I went to the Kinesis service and selected "Delivery Streams" on the left side of the screen. This allows to access the Kinesis Firehose Delivery Stream service. Next, I click on "Create Delivery Stream" and I configure the settings below:

<img src="https://user-images.githubusercontent.com/74563990/162045330-774e09ed-7c5e-402c-ab0b-cdbfc0550a7a.png" width="600"/>

<img src="https://user-images.githubusercontent.com/74563990/162045336-898efccf-3c64-4367-91a0-2dee56faadc3.png" width="600"/>

As you see above, I circled the important parts in the images that make up the delivery stream:
Source: Kinesis Data Stream (APIData) --> Intermediate Storage: S3 (firehoseredshift1) --> Destination: Redshift (Database name: redshift-firehose; Table name: firehosetransactions)

*The Copy Command (which copies my data from S3 into the table) which is created by default, is updated with an additional command in the OPTIONAL textbox in the image above. This command allows the json paths file to be read*

## Tableau



# Building Batch Processing Pipeline

## Components:

### Scheduler (CloudWatch):
Utilized CloudWatch as a scheduler to trigger the batch processing tasks at predefined intervals.

### Lambda Function (Batch Processing):
Wrote a Lambda function which is created to handle the batch processing tasks. It's triggered by the CloudWatch scheduler.

### Data Source (S3):
The batch processing pipeline typically involves handling large volumes of data stored in an S3 bucket.

### Destination (DynamoDB, Redshift):
Processed data is loaded into the destination, into a DynamoDB table for NoSQL storage and into a Redshift table for analytical purposes, similarly to what was done for the streaming pipeline

# Conclusion

In conclusion, this E-Commerce Data Engineering Project using AWS has provided a comprehensive exploration of data engineering principles and practices. Through the conceptual planning and implementation of various data pipelines, the project aimed to showcase the intricacies of handling e-commerce data efficiently. The journey began with the selection and understanding of a relevant dataset, emphasizing the importance of aligning data engineering efforts with specific business goals.

The DS Blueprint served as a guiding framework, outlining essential phases such as connecting to data sources, buffering for smooth data flow, processing raw data, storing it appropriately, and finally, visualizing the insights derived. The chosen dataset, an e-commerce dataset from Kaggle, presented an opportunity to simulate real-world scenarios and address considerations regarding storage options, whether relational or NoSQL.

The platform design involved the selection of tools like AWS S3 for file storage, DynamoDB for NoSQL database needs, and Redshift for analytical purposes. The data pipelines, both in conceptual planning and implementation, covered various scenarios such as data ingestion, streaming to raw storage, streaming to DynamoDB, visualization API, visualization warehouse, and batch processing. Each pipeline was meticulously crafted using AWS services like Lambda functions, Kinesis streams, and Firehose delivery streams.

The project also delved into the development of a data ingestion pipeline, stream to raw storage pipeline, stream to DynamoDB pipeline, visualization API pipeline, visualization warehouse pipeline, and batch processing pipeline. Each step involved the creation of Lambda functions, setting up Kinesis streams, configuring buffers, and establishing connections with storage and database services.

The Visualization API pipeline allowed for easy access to specific data items through a well-designed API, while the Visualization Warehouse pipeline demonstrated the integration of Redshift for analytical purposes. The entire process was brought to life through detailed code snippets, IAM role setups, security group configurations, and thorough testing using tools like Postman.

In the realm of batch processing, considerations for CloudWatch as a scheduler, the orchestration of data movement, and integration with DynamoDB and Redshift were explored. The implementation of IAM roles and security groups played a crucial role in ensuring seamless communication between services.

Ultimately, this project has not only showcased the technical aspects of data engineering on AWS but also emphasized the strategic thinking required in aligning data engineering efforts with business objectives. As the journey concludes, the newfound knowledge and hands-on experience serve as a valuable asset in navigating the dynamic landscape of data engineering.

For those interested in staying connected and exploring further insights, you can follow me on LinkedIn: [Ralph Worley](https://www.linkedin.com/in/ralph-worley-6a8944213/). Thank you for joining me on this data engineering adventure!
