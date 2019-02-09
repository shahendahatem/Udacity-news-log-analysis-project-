# Logs Analysis Project
First project in the Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).
### By Shahenda Hatem

## Project Requirements
The main task of this project is a reporting tool that uses information from a database called news that contain three tables :

1.The `authors table` includes information about the authors of articles.
2.The `articles table` includes the articles themselves.
3.The `log table includes` one entry for each time a user has accessed the site.

The reporting tool should answer the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Project contents

* `logs_analysis.py` - The Python program that connects to the PostgreSQL database, executes the SQL queries and displays the results.
* `README.md` - This read me file.
* `logs_output.txt` - The text output of the `news_logs_analysis.py`

## How to Run the Program

### Rquired Libraries and Dependencies

The project code requires the following software:

* Python
* psycopg2
* PostgreSQL
* Vagrant
* virtualbox

### Setup Project:

1.Install Vagrant and VirtualBox, Please check [instructions to install the virtual machine](https://classroom.udacity.com/courses/ud197/lessons/3423258756/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
2.Download or Clone this repository in the /vagrant directory You must finish step 1 first

### Prepare the Software and Data

1.The virtual machine from step 1
If you need to bring the virtual machine back online with $ vagrant up. Then log into it with $ vagrant ssh

2.Download the data from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

	Unzip this file after downloading it. The file inside is called newsdata.sql.
	To run the reporting tool, you'll need to load the site's data into your local database. To load the data, use the command
	```psql -d news -f newsdata.sql```

3.Creating views
####collect		
This view is used to show the information about author_title,author_name,author_ID and he total view for each author

````sql
CREATE VIEW collect AS
    SELECT articles.title AS article_title,
         articles.author AS author_id,
         authors.name AS author_name,
         count(log.path) AS views
    FROM  log, articles, authors
    WHERE log.path LIKE ('%' || articles.slug)
         AND authors.id = articles.author
    GROUP BY article_title, author_id, author_name
    ORDER BY views DESC;
````  

#### All_requests 
This view show the total number of requests on the website

````sql
CREATE VIEW All_requests AS
    SELECT date(time), COUNT(*) AS reviewers
		   FROM log 
		   GROUP BY date(time)
		   ORDER BY date(time);
````

####error_requests
This view show the total nymber of bad requests on the website

````sql
CREATE VIEW error_requests AS
	SELECT date(time), COUNT(*) AS errors
		   FROM log WHERE status = '404 NOT FOUND' 
		   GROUP BY date(time) 
		   ORDER BY date(time);
````
####error_rate
This view show the percentage of the bad requests 

````sql
CREATE VIEW error_rate AS
	SELECT All_requests, (100.0*error_requests.errors/All_requests.reviewers) AS percentage
		   FROM All_requests, error_requests
		   WHERE All_requests.date = error_requests.date
		   ORDER BY All_requests.date;
````

4- Run the Tool

1.From the vagrant directory inside the virtual machine, run logs_analysis.py using:
`$ python logs_analysis.py`
2-Check the output file for the results output.txt


## Helpful Resources

* [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
* [PostgreSQL 9.5 Documentation](https://www.postgresql.org/docs/9.5/static/index.html)
* [Vagrant](https://www.vagrantup.com/downloads)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
