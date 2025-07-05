# Python Generators
## Tasks One: Objective: create a generator that streams rows from an SQL database one by one.

## Files: fetch.py, seed.py 
## Repository: 
<p>Task Breakdown</p>
    <ul>
    <li> Setup Database Connection:</li>
    <li> Create entity and define attributes 
        (<strong>entity:</strong> user_data, <strong>attributes:</strong> id pk, name varchar NOT NULL, email varchar NOT NULL, age, decimal NOT NULL)</li>
    <li> Seed table, data source:  
    [user_data.csv](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv "user_data csv") </li>
    </ul>


## Task Two Objective: create a generator that streams rows from an SQL database one by one.

# File: 0-stream_users.py
    <p> Task Breakdown</p>
    <li> Establish db connection <code>connection = seed.connect_to_prodev()</code> with existing db</li>
    <li> Fetch rows using generator <code>def stream_users(limit)</>
    <li> 

