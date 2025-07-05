# Python Generators
## Tasks 1 Objective: create a generator that streams rows from an SQL database one by one.

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


## Task 2 Objective: create a generator that streams rows from an SQL database one by one.

# File: 0-stream_users.py
    <p> Task Breakdown</p>
    <ul>
    <li> Establish db connection <code>connection = seed.connect_to_prodev()</code> with existing db</li>
    <li> Fetch rows using generator <code>def stream_users(limit)</>
    <li> 
    </ul>

# Task 3 Objective: Create a generator to fetch and process data in batches from the users database

<p>Task Breakdown </p>
<ul>
<li> Establish db connection <code>connection = seed.connect_to_prodev()</code> with existing db</li>
<li>Fetch user data in batches, apply limit to query execution. <code>batch_processing(batch_size)</code> </li>
<li>Fetch users above the age of 25, using sql WHERE statement <code>batch_processing(batch_size)</code> </li>
<li>Fetch users apply limit <code>stream_users_in_batches(batch_size)</code> 
</ul>
