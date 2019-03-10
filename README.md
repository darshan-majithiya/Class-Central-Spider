# Class Central Spider
This spider is used to crawl the https://www.class-central.com and generate dataset containing the information of various courses. The spider gets the information of 15 data points. For more information check dataset.csv in Spider root directory.
## Dependencies
- Python 3.x
- Scrapy 
###### This code is tested with Scrapy 1.5.1. You can install it via 'pip'.
```
pip install scrapy
```
###### or if you want to install it using 'conda', then you can do it as
```
conda install -c anaconda scrapy 
```
## Downloading the code
You can download it directly or by running the below command in your terminal
```
git clone https://github.com/darshan-majithiya/Class-Central-Spider.git
```
## Running the Spider
Go to Spider's root folder. And then run the command 
```
scrapy crawl ClassCentral
```
You can also pass the specific domain as argument of which you want to get the course information. You can check the available domains on 
https://www.class-central.com/subjects. 
```
scrapy crawl ClassCentral -a domain="Data Science"
```
And finally you can output the information to your desired data fromat (csv, json, and xml).
```
scrapy crawl ClassCentral -o dataset.csv
```
