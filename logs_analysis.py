
#Author: Shahenda Hatem

#Udacity Full Stack Nanodegree Project 1 :Log Analysis Project

#objective: creating reporting tool that contains three main reports

#1st Report:List of the most three articles that have been accessed 
#2nd Report:List of authors that have the most page views
#3rd Report:List the days that have more than 1% of requests lead to errors


#Steps for developing the reports queries
#-------------------------------------------------------------------------------------------------------
#improt database PostgreSQl lib
import psycopg2

#1st report 
popular_articles = """ SELECT article_title, views
				FROM   collect
				LIMIT 3;"""		

#2nd report
popular_articles_authors = """ SELECT author_name, sum(collect.views) AS views
				FROM   collect
				GROUP BY author_name
				ORDER BY views DESC;"""
#3rd report
failure_requests= """  SELECT *
                FROM error_rate
				WHERE error_rate.percentage > 1
				ORDER BY error_rate.percentage DESC;"""
#-------------------------------------------------------------------------------------------------------

def query_database(sql_queries):
    
    try:
        connection = psycopg2.connect(database="news") #news is the database we need to connect
        cursor = connection.cursor()
    except psycopg2.Error:
        print("Failed to connect to the PostgreSQL database.")
        return None
    else:
        cursor.execute(sql_queries)
        results = cursor.fetchall()
        connection.close()
        return results
#-------------------------------------------------------------------------------------------------------
#printing reports
#-------------------------------------------------------------------------------------------------------
def first_report():
    result1 = query_database(popular_articles)
    print("\n\t\t List of the most three articles that have been accessed \n")
    for title, count in result1:
        print(" \"{}\" -- {} views".format(title, count))
#------------------------------------------------------------------------------------------------------
def second_report():
    result2 = query_database(popular_articles_authors)
    print("\n\t\t List of the authors that have the most page views \n")
    for name, count in result2:
        print(" {} -- {} views".format(name, count))
# ------------------------------------------------------------------------------------------------------
def third_report():
    result3 = query_database(failure_requests)
    print("\n\t\t List the days that have more than 1% of requests lead to errors \n")
    for date, percentage in result3:
        print("        {} - {}% errors ".format(date, percentage))
	print("-" * 70)
# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
   first_report()
   second_report()
   third_report()

