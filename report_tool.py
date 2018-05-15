#!/usr/bin/env python2.7
# The previous line has been copied from:
# https://stackoverflow.com/a/21189383 by: Nigel Tufnel.

import psycopg2


connection = psycopg2.connect("dbname=news")
cursor = connection.cursor()
cursor.execute("select articles.title, count(log.id) \
as visited from log, articles where path = \
('/article/' ||  articles.slug) group by articles.title \
order by visited desc limit 3;")
result = cursor.fetchall()
print "What are the most popular three articles of all time?\n"
for i in result:
    print '"{}" __ {} views'.format(i[0], i[1])

###################################################
cursor.execute("select authors.name, count(log.id) \
as visited from log, articles, authors where path = \
('/article/' ||  articles.slug) and articles.author = \
authors.id group by authors.name order by visited desc;")
result = cursor.fetchall()
print "\nWho are the most popular article \
authors of all time?\n"
for i in result:
    print '"{}" __ {} views'.format(i[0], i[1])

###################################################

cursor.execute("select total_table.tday, \
concat(round(cast((failed:: float * 100 / total) as \
numeric), 2), '%') as percent from (select TO_CHAR\
(time, 'Mon DD, YYYY') as tday, count(id) as total from log \
group by tday) total_table, (select TO_CHAR(time, 'Mon DD, YYYY') \
as fday, count(id) as failed from log where status != '200 OK' \
group by fday) failed_table where total_table.tday = \
failed_table.fday order by percent desc limit 1;")
result = cursor.fetchall()
print "\nOn which days did more than 1% of \
requests lead to errors?\n"
print '"{}" __ {} errors'.format(result[0][0], result[0][1])

connection.close()
