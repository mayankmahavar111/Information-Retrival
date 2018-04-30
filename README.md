# Information-Retrival
###Learning to Rank , Selection Bias , Personal Search

#####Pre-Requisties installation
pip install -r requirements.txt

download document.db[2.81 gb] from 
https://drive.google.com/open?id=1OroqztNS4ZwPog7JBv2jtwI9BYJTkWt5
and replace it with current document.db file
or generate database.db by following instruction given at last

now run preprocessing.py

open *interface/search/view.py* file, find connectdb method and change 'dir' path according to your system 


#####How to run program
go to interface folder and then run 

python manage.py runserver

now open browser and type 
http://127.0.0.1:8000/search/

type query in query field
select which engine you want to use. You have 4 choices :
 1. Normal (without any bias value)
 2. global (with global bias)
 3. segment (with segment bias)
 4. generalise (with generalise bias)

then press submit 

The results will be shown in the page with links.
click on link to see the full document.

#####Use of Every file
database.py : create database from reuters files

preprocessing.py  : preprocess the data from database and then store it again in the database

idf.py : store inverse document frequency for each term in the idf table in database

doc-vector.py : create document vector and store it in database

click.py : generate random clicks on different document on different poistion

interface/search/views.py : contains all the methoda required to run the website.
It also contain methods of global bias,generalise bias and normal bias.

interface/search/segment.py : contain method to find segment bias value

##### how to generate database.db and configure it without downloading
run  *python database.py* file  ,before running change dbname to 'database'

run *python preprocessing.py* file , it will preprocess files

run *python idf.py* file to find terms idf values

run *python doc-vector.py* file to term coincident matrix for documents

run *click.py* file to generate random clicks
 
run *database.py* file again by changing dbname as 'result'

open *interface/search/view.py* file, find connectdb method and change 'dir' path according to your system 
