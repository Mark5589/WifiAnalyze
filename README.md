

## Installation

### Reqierments:
***NOTE*** its good to check that your machine has the following libraries (at least):  `pprint`

1.  * install '*plotly*' library with the command:
        `pip install plotly --upgrade`
    * configure the plotly: run `python` in your terminal, `import plotly`
        add the configuration: 
        `plotly.tools.set_credentials_file(username=‘mark5589’, api_key='5cWyq68Mj868YtbRjGtJ')`
        also you can visit *plotly* to view the chart on https://plot.ly 
        Username: `mark5589`
        password: `recon4412`

2. make sure `mongoDB` python library is installed on your machine. the following import  `import pymongo` should be successful.

   * also check that you can run MongoDB on your local machine.	 cmd: `mongod`

   * if  any error occurs try this 

     documentation: [http://api.mongodb.com/python/current/tutorial.html](http://api.mongodb.com/python/current/tutorial.html)



## Running

To run this program use the following command:

`python app.py <CSV file with wifi records> `

the 3-th argument is the CSV file with wifi records that will be processed.





## TODO LIST

1. ~~make/create/build CSV file.~~
2. ~~Read that file into the program~~
3. ~~create JSON Object from wifi record.~~
4. ~~upload that JSON Object to MongoDB.atlas.WifiAnaylze.root.records~~
5. ~~represent chart of [ Security_Protocal: Amount ] // to do this we have to count the SecurityProtocol : amount relation~~
6. ~~Create some chart~~
7. ~~make Connection with MongoDB Atlas~~
8. ~~Try some connection to MongoDB, with uploading data to the db~~
9. ~~Upload our data to MongoDB Atlas~~
10. ~~Represent our data with Chart~~
11. Avoid duplicates of the data. (With the help of the MAC)
    * This fuctionalty shuold be done in the backend level because once the data is processed, it sends to the chart API and after that to the MongoDB



## Images

### plotly

![alt text](https://github.com/Mark5589/WifiAnalyze/blob/master/image/MongoAtlas.png)

### MongoDB Atlas



![MongoAtlas](/Users/recon/workspace/3-python/1-wifiAnalyz/image/MongoAtlas.png)
