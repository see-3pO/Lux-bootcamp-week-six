#Using an official runtime as a parent image
FROM python:3.9-slim-buster

#set the working directory to the app
WORKDIR /app

#Copy the current directory contents into the container at /app
COPY . /app

#Install any needed packages specified in the requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#Make port 80 available to the world outside the container
EXPOSE 80

#Define environmental variable
ENV NAME todo

#Run the app.py when the container launches
CMD ["python", "app.py"]