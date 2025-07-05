# ALX Python Tasks

> **Note**: This README is automatically generated from `python-generators-0x00/README.md`

---
# Python Generators
## Tasks 1 Objective: create a generator that streams rows from an SQL database one by one.

### Files: python-generators-0x00/fetch.py, python-generators-0x00/seed.py 
### Repository: [alx-backend-python](https://github.com/chinazagideon/alx-backend-python "alx-backend-python repo")

<p>Task Breakdown</p>
<ul>
    <li> Setup Database Connection:</li>
    <li> Create entity and define attributes 
        (<strong>entity:</strong> user_data, <strong>attributes:</strong> id pk, name varchar NOT NULL, email varchar NOT NULL, age, decimal NOT NULL)
    </li>
    <li> Seed table, data:  
    [user_data.csv](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv "user_data csv") 
    </li>
</ul>


## Task 2 Objective: create a generator that streams rows from an SQL database one by one.

### File: python-generators-0x00/0-stream_users.py
### Repository: [alx-backend-python](https://github.com/chinazagideon/alx-backend-python "alx-backend-python repo")

<p> Task Breakdown</p>
    <ul>
    <li> Establish db connection 
    <code>connection = seed.connect_to_prodev()</code> with existing db</li>
    <li> Fetch rows using generator <code>def stream_users(limit)</code><li> 
    </ul>

## Task 3 Objective: Create a generator to fetch and process data in batches from the users database

### Files: python-generators-0x00/1-batch_processing.py, main.py
### Repository: [alx-backend-python](https://github.com/chinazagideon/alx-backend-python "alx-backend-python repo")

<p>Task Breakdown </p>
<ul>
<li> Establish db connection <code>connection = seed.connect_to_prodev()</code> with existing db</li>
<li>Fetch user data in batches, apply limit to query execution. <code>batch_processing(batch_size)</code> </li>
<li>Fetch users above the age of 25, using sql WHERE statement <code>batch_processing(batch_size)</code> </li>
<li>Fetch users apply limit <code>stream_users_in_batches(batch_size)</code> 
</ul>

## Task 4 Objective: Simulte fetching paginated data from the users database using a generator to lazily load each page

### File: python-generators-0x00/2-lazy_paginate.py 
### Repository: [alx-backend-python](https://github.com/chinazagideon/alx-backend-python "alx-backend-python repo")


<p>Task Breakdown</p>
<ul>
    <li> Establish db connection <code>connection = seed.connect_to_prodev()</code> with existing db</li>
    <li> Fetch data from user table apply limit filter and offset for pagination <code>lazy_paginate(limit, offset)</code></li>
    <li> Paginate data apply pagesize and offest, return response.</li>
 <li> 
</ul>

## Task 5: to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

### File: python-generators-0x00/4-stream_ages.py
### Repository: [alx-backend-python](https://github.com/chinazagideon/alx-backend-python "alx-backend-python repo")

<ul>
<li>Stream age data in the user table <code>stream_user_ages()</code></li>
<li>Loop through the age data to calculate the average without using sql AVERAGE statement</li>
<li>Print the average age using a generator function</li>
<li>



