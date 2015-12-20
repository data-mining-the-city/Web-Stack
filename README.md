# DM Weibo

Logan Clark | Shengye Guo | Zhiyuan Han | Yuhan Ke | Emily Kerns Minougou | Sinae Lee | Jialei Wu

## Introduction

This MVP (minimum viable products) examines the patterns of check-ins in restaurants in Shenzhen for each day of the week, time of day (sorted by morning, day, evening, and night), and density of the check-ins. It also looks at the distribution of the check-ins, such as trying to detect whether there are clusters of restaurants. 

## Research Scope 

The area this project focuses on is downtown Shenzhen (Futian District and Luohu District).

## Hypothesis

It is hypothesised that there is a difference in the pattern of restaurant check-ins between the weekdays and weekends as well as day and night. The differences may help detect where activity is taking place in the city and different times and may show how people move throughout the city during the day and night and the week and weekend. 

## Methodology 

This product explores checkins using the Weibo database on Orient DB. A query was setup to select all the “Food” category checkins and based on the time the check in occurred, it is then categorized as morning, day, evening, or night. By using the MVP, a user can select a day of the week and time of day they would like to study. They may also examine the density of checkins by selecting the optional heatmap. The user may toggle between different days and times of day to see the differences between checkins.

## Minimum Viable Product 

In order to create the MVP the following items were assumed:
-	People may eat in the downtown business area during the day
-	At night, the checkins may spread out from the downtown since people may be eating elsewhere
-	People are mostly checking in to restaurants and not checking into the their homes or office so “Food” was selected as the checkin category
-	People may eat at restaurants and check in using Weibo often enough to generate enough data to analyze the region
-	Checkins on the weekends may be different from checkin patterns during the week

Ways to extend the MVP
-	Create an animation to show how the checkins move throughout the day in a quick format
-	Figure out how to query data more quickly
-	Show two or more queries of time of day and day of week at one time to show comparison

## Data Processing 

Dataset Used

Weibo database 

Describe in detail any processing you did on the data to prepare it for your application

In order to query the “Food” checkins and time of day, a category needed to be created for the type of checkin and a separate checkin needed to be created for time of day. This was queried from the time category and time of day was separated based on the following time periods:
5am - 11am: Morning
11am - 4pm: Day
4pm - 9pm: Evening
9pm - 5am: Nigh

## Server Back End

Arguments that are sent from the client and received by the server

The arguments are given by the inputs of the client interface. As the user zooms to a particular portion of the map, the new bounding latitudinal and longitudinal coordinates are generated. The other options checked by the user on the interface form the basis of the query that is passed to the database through the flask. The server then passes the results back to the client side.

Update messages

Our update messages show the number of records returned by the query. The user is then informed that the records are being matched. Finally the user is informed when the operation is complete and the application is idle.

Data sent back to the client at the end of the request

The data is sent back to the client through an SSE event stream using the Flask’s response command. The data is converted back into javascript and passed to the user interface.

## Server interacts with the database

Query that is sent to the database

The local host server receives the query and passes it through to the database using the app.py file. OrientDB then opens the appropriate database and parses through the correct properties.
	
Results of the query are processed and formatted for sending back to the client

The query results are passed back through the server and formatted into JSON to appear on the user interface.

## Client Front End
	
Front end User Interface (UI)

The user interface allows a person to view the Food checkins by different time periods and days. It includes seven days  a week and is divided each day into “morning” “day” “evening”“night”

General User Experience (UX) story or narrative

A user may want view the patterns of “Food” checkins if they are planning on opening a restaurant, a new club, shop, or trendy place. They may analyze the patterns to understand where people are traveling throughout the city and from there they may make an informed decision where to open their new business. A city may use the data to plan a new project that they want to have a lot of publicity and high amount of visibility. By using the MVP, they can choose where to place the project based on the density of checkins. If they are looking to attract business people then they may use the query to see check ins on a weekday during the day.


Reproduce and explain in detail any requests you are sending to the server, including any arguments in the query string, and how they are communicating the decisions the user has made in the UI

Describe how the data is visualized using JavaScript/D3

We used different color of background for different time period. (i.e. Black for evening and night, white for morning and day). We also used heat map to convey the important information on clusters of restaurants that with check ins. The information will occurs when the mouse pointer is over the selected restaurants.
