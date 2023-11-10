# ACM AWS Workshop 2023

This workshop demonstrates how to set up a web server using AWS EC2, a database using AWS RDS (using MySQL), and fetch data from an S3 Bucket.

This workshop assumes you already have an AWS account and have access to EC2, RDS, and S3.

## 1) Make an EC2
- Open the [EC2 page on the AWS console](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1)
- Navigate to the instances tab
- Click Launch Instance, and give it a name
- Use Amazon Linux as the image and t2.micro as the instance type
- For key-pair login, create a new key pair, and enter a name. This will download a file to your computer.
- Under Network Settings, make sure `Allow SSH traffic from Anywhere` and `Allow HTTP traffic from the internet` are selected.
- Press `Launch Instance`

### 1a) Connecting
- Once you have your instance, click the `Connect` button
- Select `EC2 Instance Connect` and click Connect. This should open up an window in a new tab where you have command line access to your EC2 instance.

## 2) Hosting
To host a website on EC2, we need to set up a few things first. Run the following commands:

```
sudo dnf update -y

sudo dnf install -y httpd php php-mysqli mariadb105`

sudo systemctl start httpd
sudo systemctl enable httpd
```

You should now have a web server running on your ec2 instance! 

### 2a) Basic HTML
Let's create a webpage:
```
cd /var/www/html
sudo nano index.html
```

This opens a text editor. Add some HTML content, for example: 

`<h1> Hello World from EC2! </h1>`

Save the file by pressing CTRL + X and then pressing Y and then Enter.

Navigate back to the EC2 console, and under your instance settings, look for the link under `Public IPv4 DNS` (something like `ec2-1-23-45678.compute-1.amazonaws.com/`). Click the link next to it to open up your instance. If you get an error, try changing your URL to `http` (instead of `https`). You should now see your webpage!

### 2b) Cloning from git

Now let's try running a more complicated website, like the Hack for Humanity site!

First we need to remove our old index.html file:

```
sudo rm index.html
```

Next, we'll install git and then clone a repository into our existing directory.

```
sudo dnf install git
sudo git clone https://github.com/SCUACM/SCUACM.github.io .
```

Note: If you use a framework like React or Angular, you'll need to compile your code (using someting like `npm run build` or `ng build` and then copying the output files into /var/www/html)

### 2c) Additional Resources for Hosting
 [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html) 

# 3) Database
- Open [the RDS page of the AWS console](https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1)
- Select the Databases tab on the left
- Choose `Create Database`
- Use standard create, and select MySQL as the engine
- Select the free tier template
- In `Settings -> Credentials Settings`, leave the `Master username` as admin and add a password.
- Under `Connectivity` choose `Connect to an EC2 compute resource` and choose the EC2 instance you created earlier
- Open up the `Addiontal Configuration` settings and add an `Initial database name`, such as `sample`
- Click `Create Database`

Once your database is created, click on it and copy the endpoint URL (something like `mydb.abcdefg.us-east-1.rds.amazonaws.com`)

### 3a) Connect to the database using PHP
Now we want to connect to the database. Let's first do this with PHP. First we'll set up the credentials for database so that PHP can communicate with it:
```
cd /var/www
sudo mkdir inc
cd inc
sudo nano dbinfo.inc
```
Copy the `dbinfo.inc` provided in this repository. Change the `<db_instance_endpoint>` with your endpoint URL you copied earlier, and update the `<password>` to be the password you set for your database. Save your changes with CTRL + X -> Y -> Enter

Now let's create our PHP Page. Navigate to the html folder and create a page called SamplePage.php:
```
cd ../html
sudo nano SamplePage.php
```
Copy the `SamplePage.php` file provided in this repo, and save your changes with CTRL + X -> Y -> Enter

Now, open up your website again but add `/SamplePage.php` to the end of the URL. This should bring up a simple HTML page with fields to a name and address, followed by a table listing all elements already in the table.

### 3b) Using MySQL
If you want to have full access to your database, we can use the mySQL CLI tool to access it. Access it with:
```
mysql -h <endpoint> -P 3306 -u admin -p
```
Make sure you replace `<endpoint>` with your actual RDS endpoint!

This should bring you into a MySQL command line. Let's run some SQL commands to check that it is working:
```
USE sample;
SELECT * FROM EMPLOYEES;
```
This should list the employees you created earlier on the PHP page!

### 3c) Resources for RDS
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateDBInstance.html
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html

## 4. Flask!
Finally, let's create a Flask server that connects to SQL!

### 4a) Install Flask
First, navigate back to your home directory:

``` 
cd ~
```

Next, let's install pip, and then use pip to install Flask:

```
sudo dnf install python3-pip
pip install Flask
```

### 4b) Create a basic Flask endpoint
Let's create a simple Flask API in python:
```
sudo nano app.py
```
Copy the code from `app.py` and save it.

Now, let's run the flask app:
```
flask --app app run --host 0.0.0.0 
```

Our Flask app is now running on port 5000! We can try to open our flask app by visiting port 5000 in our browser (for example, `http://ec2-1-23-45678.compute-1.amazonaws.com:5000), but the page will not load. This is because we haven't told our EC2 instance to allow traffic on port 5000.

### 4c) Edit EC2 Inbound Rules

To allow access to our flask app, running on port 5000, we need to add an Inbound Security Rule:
- Open your instance in the EC2 console
- Click on the `Security` tab, and under `Security groups` select the group that says `launch-wizard-1`
- On the right, select `Edit inbound rules`
- Click `Add Rule`
- Leave the type as `Custom TCP`, set the `Port range` to `5000` and the Source to `0.0.0.0/0`
- Click `Save rules`

Now, try accessing port 5000 on the server again and you should be able to see `Hello World`

### 4d) Connect to SQL

Now, let's add API endpoints to our Flask server that allow us to talk to the database. First, we need to install the MySQL Connector
```
pip install mysql-connector-python
```

Next, let's create a new Flask app under sql.py
```
nano sql.py
```

Copy the code provided in `sql.py` and edit `<endpoint>` and `<password>` to be your RDS endpoint URL and password, respectively. Save the file:

Let's run our Flask app:
```
flask --app sql run --host 0.0.0.0 
```

If you try refreshing your Flask page in the browser, it should still look the same. However, if you add `/employees` to it you should see a list of employees we added to the table ealier.

To add new employees, we can use POST request. This can't be done in the browser, but we can see it in Postman!

Log in to [Postman](https://web.postman.co/) and import the collection in this repo: `AWS Tutorial.postman_collection.json`. Replace the URLs in the 3 sample requests with the correct EC2 URLs. This should allow you to make requests to view and add employees.

## 5) S3

S3 is a storage container for storing files. In this tutorial we will not be showing you how to create an S3 bucket or upload files, but we will show you how to list files and download them in Python given a Access Key ID and Secret Access Key.

### 5a) Listing files
First, we need to install the AWS library for Python, boto3:
```
pip install boto3
```

Next, we'll open up `s3access.py`. Update the `<your_access_key_id>`, `<your_secret_access_key>`, `<your_bucket_name>` to the correct access key, secret key, and bucket name. Now, run the python file and you should see a list of files that are in the bucket.

### 5b) Downloading a file

Open up `s3download.py` and update the same values as before, as well as the `object_key` to be the location of the file in s3, and the `local_file_path` to be the downloaded file. Run `s3download.py` and it should download the file you selected to your current directory!