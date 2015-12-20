Data Processing 

The database we used is Weibo Dataset, and we tried to look into the check-in information to geo-locate the places where prostitution may happened.
On the first test, we wanted to create a subset of the Weibo data in order to shrink the range of data to provide a more stable query process. In this round, we targeted the Dongguan prince hotel and queried the check-in information either based on the geo-location of the spot or the checkin_text which contains the words about 'dongguan（东莞）' and 'prince（太子）'.
The filtering code as following:

def filter_database():
    query = 'SELECT FROM Checkins WHERE text containstext "东莞" and text containstext "太子"'
    records = client.command(query) # My guess: records is the set of all records
    cluster_id = 3 
    rec_list = []
    for rec in records:
        rec_list.append(rec)
    print rec_list
    client.db_close()
The result of the code were quite limited and only about 20 check-in results came out, thus in this stage we kept changing different types of query code in orientDB to find the better results we want. 
And we also typed some code based on the time range in order to filter out specific type of data. For instance, we want to query the data from 8:00 pm to 4:00am everyday which more related to the yellow industry. Following are the union syntax to check the specific time range.
SELECT * FROM Checkin WHERE lat BETWEEN 22.53 AND 22.56 AND lng BETWEEN 114.04 AND 114.08 AND time REGEXP "^2014-{1}[01]{1}[0-9]{1}-{1}[0-3]{1}[0-9]{1}\s2{1}[0-3]{1}:.*$"

UNION

SELECT * FROM Checkin WHERE lat BETWEEN 22.53 AND 22.56 AND lng BETWEEN 114.04 AND 114.08 AND time REGEXP "^2014-{1}[01]{1}[0-9]{1}-{1}[0-3]{1}[0-9]{1}\s0{1}[0-3]{1}:.*$"
]{1}[0-9]{1}-{1}[0-3]{1}[0-9]{1}\s0{1}[0-3]{1}:.*$"

The language of the code cannot be read by python and it may need further filtering in terms of the uncertainty of the type of check-in.

Then, we slightly changed our target from one spot 'prince hotel' to one district 'houjie', another street that are also famous for these kind of industry. And in these area, we started making the query on one specific day period after the yellow clearance action, this help us get the original places as our set A.

query = 'SELECT FROM Checkin WHERE lat BETWEEN 22.929935 AND 22.961751 AND lng BETWEEN 113.639837 AND 113.693017 AND time BETWEEN "2014-09-03 03:00:00" and "2014-09-04 04:00:00"'
numListings = len(records)
print 'received ' + str(numListings) + ' Checkins'

The next thing we do was using the 60 results we get from the last step to search for the user profile who issued the Weibo check-ins. And then used 'Traverse' command to build up a new query to look for the other places where the group of people goes. In this case, we tried to build up the connection between our original places(set A) and the extended places(set C). 

uniqueUsers = []
originPlaces = []
connectedPlaces = []

output = {"type":"FeatureCollection","originP":[],"connectedP":[]}

for record in records:
	user = str(record.out)

 	if user in uniqueUsers:
    	continue
 	uniqueUsers.append(user)
    	
    	places = client.command("SELECT * FROM (TRAVERSE out(Checkin) FROM (SELECT * FROM      	{})) WHERE @class = 'Place'".format(record.out))
    	print 'received ' + str(len(places)) + ' connected places from ' + str(record._in)
