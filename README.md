# Core DMC Web Stack platform

Project containes two branches:
- **soufun** - Implementation using soufun rental listing data set with heat map and interpolation (ML) analysis using overlay grid
- **weibo** - Implementation using weibo social media data set with graph analysis, click events, and animated transitions.

//**FINAL PROJECT**//

## Project Description 
 
 1. Research Topic - what general question or idea are you examining?
-We examined how the consumer behaviour reacts to the change of stock market.

 2. Research Scope - what geographic area are you focusing on?
-We mainly focus on Pearl River delta.

 3. Hypothesis - the specific hypothesis tested by your prototype.
-The consumer behaivor, which is represented by the number of check-ins for the Food/Drinks categories, will change based on the stock market. When the stock market goes up, the total check-ins will go up, vice versa.

 4. Methodology - general description of how your project tests the hypothesis.
-We tried to cluster areas of the region to show the concentration of check-in types. Then we track the total unmbers of check-ins within one cluster during a specific time for a specific check-in category. More generally speaking we tried to represent the overal consumer trend of the region in order to compare this against global stock markets.

 5. Minimum Viable Product - what assumptions or generalizations did you implement in order to generate a working MVP? How would the MVP be extended to create the ultimate product you envision?
 -We had issues running the loop within a responsive timeframe. The requests to the server would take +10 seconds for one check-in and resulted in no response for the range of 10 clusters. Without knowings the exact issues of the dataset, a sample of data would be plotted and color coordinated in order to show spatial diversity of check-ins.
 
 ## Data Processing 
 
 1. Which dataset are you using (soufun or weibo)
 -Weibo 

 2. Describe in detail any processing you did on the data to prepare it for your application. This should include any -pre-processing done outside of runtime, which was hardcoded into the dataset. Include a reference to the actual script in your project files which must be run to generate the proper data set.
 -We want to use cluster to categorize the dataset. This is based on our assumption that there should be clusters for certain type of consumption weibo check-in. So k-means is here to help us. At the beginning, we were to use the checkin to calculate the clusters; but due to the giant amounts of records, we switch to places to get clusters. So the whole process is divided into two parts, one for calculating cluster and writing the cluster id into every place record, one to write cluster id into checkin by matching checkin record to place record. So at the end, we get a date base with cluster id in checkin records and place records. 

 Still, k-means can include a weight to get clusters. Our original thought was to use soufun data and get the property value as the weight. But the thought was too perfect to be doable. So we just simplified this process to get clusters by place instead of political boundaries. 

 Another idea at the beginning stage was to use the network for cluster analysis. This is based on the assumption that strong connection between two places might reveal one kind of consumption behavior. But we gave up this way due to the difficulty.

 ## Server Back End 
 
 Describe how the server interacts with the client, including:
 1. The arguments that are sent from the client and received by the server at the beginning of the request.
 2. Any update messages sent back to the client during the request.
 3. The data sent back to the client at the end of the request, including the data format.

 -The server side gets the map bounds and the time elements from client interface by using request.args.get function. Then all these elements from client will be used in the dynamic query. Due to the large amount of database, we divided the database into several chunk. During the query, we will gradually send back the data to the client side. The group size is xxxxxx(填上具体数字). Therefore, updates on client side will happen everytime the chunk finish query. And at the end of the query, all database will be processed.
 
 Describe how the server interacts with the database, including:
 
 1. The query that is sent to the database.
 2. How the results of the query are processed and formatted for sending back to the client.

 -The query is acquired from client side. The client side will dynamiclly chose the time duration to be quried througn manual interface. The query includes the following elements 1.latitude 2. longitude 3. time 4. category (food/drinks) 5. cluster(preprocessed database) The items will be selected if they meet the query.

 After the query is processed, the server will record the latitude and longtidude of each item and send back to client to display. It will be stored in a np array in respect to their rid. And to calculate the sum of all the checkin, we used an array to serve as a voter. First we convert all the time to the number showing the day in the whole year, and add its votes as we proessed the data.
 
 ## Client Front End [to be completed by Client team]
 
 1. Describe the front end User Interface (UI). What options or parameters are available to the user? 
 -The user is currently able to explore the Pearl River Delta region and see where Weibo users have checked-in for Food/Drink. The code for all categories is live but is slow and not processing properly.

 2. Describe the general User Experience (UX) story or narrative you envision for your MVP.
 -The option to view 'FakeData' shows how the UX would perform with a fully operatative database/ request. Users can see regions of the PRD grow in relation to the check-ins for each category as well as its relation to stock market fluctuation.

 3. Reproduce and explain in detail any requests you are sending to the server, including any arguments in the query string, and how they are communicating the decisions the user has made in the UI
 -The user is able to request data for a specific month or week within the yearly snapshot. 

 4. Describe any further processing that is done to the data received from the server in the front end.
 -Data from the sock market is pulled from an external source to show the relation to the Weibo dataset and is represented with a histogram.

 5. Describe how the data is visualized using JavaScript/D3. How does the visualization work to communicate the important insights of the data to the user.
 -We were not able to implement a color range for each individual cluster although this would be ideal for future implementation as well as the possibility of adding a heat map.
 
=======
final description
>>>>>>> origin/UI_Experiments