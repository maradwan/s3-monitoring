# AWS S3 Monitoring

By using aws Lambda, s3,flask and mysql

![](images/S3-monitoring-1.png)
![](images/s3-monitoring-2.png)


## Cloudwatch shows the following: 
-BucketSize (Free)
-NumberOfObjects (Free)
-Requests (PUT, LIST,ALL,4XX Errors,5XX Errors) (Paid service)
-Data transfer (Total request latency, First byte latency,Bytes uploaded,Bytes downloaded) (Paid service)

## S3-Monitoring shows the following:
- BucketSize
- NumberOfObjects
- Grouping objects more than specific size
- Geo location uploaded objects
- Added/Deleted/Removed/Renamed Objects
- Grouping of Objects extensions
- identifier that perform the request


## Installations

Part 1:
* [AWS]
- Create Lambda function, lambda_function.py and change <domain/ip for api backend>
- Add requests.zip as a lambda layer.
- Enable Versioning On S3 bucket.
- On S3 Event, Check on "All object create events"
- On S3 Event, Check on "All object delete events"

Part 2:
* [API Backend]
- Use AWS EC2 or ECS.
- docker-compose up -d
