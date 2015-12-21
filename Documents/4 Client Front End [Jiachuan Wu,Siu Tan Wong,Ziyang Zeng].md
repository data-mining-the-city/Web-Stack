Client Front End 


#Client Front End [Jiachuan Wu,Siu Tan Wong,Ziyang Zeng]

##Describe the front end User Interface (UI). What options or parameters are available to the user?

According to server side’s data, different layers of weibo check in data are within the geo coordination, latitude between 22.929935 and 22.961751, longitude between 113.639837 and 113.693017, and the time range between 2014-09-03 03:00:00 to 2014-09-04 04:00:00. Through the density of these weibo check in points and connected lines between different sets of checkin points, user can understand the spatial relationship between Houjie and other spaces in Dongguan.
Basically two types of UI have been created, data visualization and interactive tip map. In the part of data visualization, user can see the sequences of check in points in Houjie, check in points in other spaces under same weibo users, and the connection between these spaces per weibo user. Apart from static map, a mouse over function has been created that user can see the details in the check in points they choose.

##Describe the general User Experience (UX) story or narrative you envision for your MVP.

Going through the representations above, we intend to create an UX in which clients can clearly understand the density of connection between different spaces, such as shopping malls, residues, and so on, to our identified sites in Houjie. Other than just showing statistics or infographics, the static and interactive maps we created will present an easily understanding image of spatial connection between one area to other areas. More than mapping, using the check in data, this platform also visual the social connection from one space to other spaces. This is our MVP, which is a prototype, layering and sub setting weibo check in data as human movements and preferences, in order to visualize spatial connections between different city nodes within urban area.

##Reproduce and explain in detail any requests you are sending to the server, including any arguments in the query string, and how they are communicating the decisions the user has made in the UI

To achieve our goals, the communications in terms of data query and data visualization work in high rate. Firstly we wanted to tackle into the specific ‘yellow’ related geo visualization, finding a direct way to point out all the ‘yellow’ points and show their spatial movements. Client side firstly requested for the weibo check in data with time and key words which include ‘yellow’ related sentences, in order to get the specific data check ins. However, the requirements constrained the dataset too much that only few checks in has been found. With our MVP changing, just using weibo check in data in different time under same users, client side requested for check in data set in one time, and another check in data set under the same users in another time.
Describe any further processing that is done to the data received from the server in the front end.

##Describe how the data is visualized using JavaScript/D3. How does the visualization work to communicate the important insights of the data to the user.

We use different circle attributions on the set of original points and another set of end points, appending red on original and black on the end. And we use thin lines to connect original ones and end ones to show the path when people checked in. 
Then according to our narrative, we use transition to build up a sequence of representation, setting duration for circles and lines to show the outcome from original points to end points and lines to lines. 
Due to the heavy data load, we also add “loading” area to tell the user whether data is loaded and graphics is shown completely. This may base on the user experiences to make sure that people know dataset is loading.