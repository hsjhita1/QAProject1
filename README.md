# QAProject1
# Table of Contents
* [Project Brief](#projectbrief)
  * [Scope & Additional Requirements](#scopeadditional)
  * [Risk Assessment](#riskassessment)
  * [Constraints](#constraints)
* [Architecture](#architecture)
  * [Entity Relationship Diagrams](#entitydiagram)
  * [Project Tracking](#projecttracking)
* [Testing](#testing)
* [Deployment](#deployment)
* [Self Reflection](#selfreflection)

## Project Brief <a name="projectbrief"></a>
The purpose of this project was 'to create a CRUD application with utilisation of supporting tools, methodologies and technologies that encapsulate all core modules covered during training'.

Effectively, this meant that I had to create an application based on the training I have recieved which was able to create, read, update and delete data.

### Scope & Additional Requirements <a name="scopeadditional"></a>
In addition to the project brief, there are a set of requirements which the project will also have to meet. These requirements are as followed:
* A Trello board
* A relational database
  * With a minimum of 2 tables
* Clear documentation
  * Describing the architecture
  * Risk assessment
* A functional CRUD application base in Python
  * Following best practices & design principles
* Fully designed test suites
  * Automated tests for validation
  * High test coverage
  * Consistent reports & evidence towards a TDD approach
* A  functioning front-end website using Flask
* Code integrated into a version control system
  * Using the feature-branch model
  * Built through a CI server
  * Deployed to a cloud based virtual machine
  
### Risk Assessment <a name="riskassessment"></a>
For this project, there were several risks which had to be indentified before the main body of the project was undertaken. This risk assessment included security of the database and application, and potential costs which the project may incur.

[Link to risk assessment](https://github.com/hsjhita1/QAProject1/blob/master/Documentation/RiskAssessmentQAProject1.xlsx)

### Constraints <a name="constraints"></a>
Due to the limited time and training, there were constraints in the project which mainly impacted to choice of technology and services used in the project. The application had to use technology and services discussed during training.

## Architecture <a name="architecture"></a>
As previously mentioned, there were constraints on which technology and services could be used. As a result of this, below is a list of what was used in the project, with each item being discussed into further detail later on:

* Project Tracking: Trello
* Database: GCP SQL Server
* Programming Language: Python
* Unit Testing: Pytest
* Integration Testing: Selenium
* Front-end: Flask
* Version Control: Git
* CI Server: Jenkins
* Cloud server: GCP Compute Engine

### Entity Relationship Diagrams <a name="entitydiagram"></a>
#### Initial ERD
![alt text](https://github.com/hsjhita1/QAProject1/blob/master/Documentation/Initial%20ERD.png "Initial ERD")

In the initial ERD, it was planned to have more tables and columns in the database but due to time constraints, some of the tables were not created. Despite this, multiple tables were created with relationships to create my relational database for this project.

#### Final ERD
![alt text](https://github.com/hsjhita1/QAProject1/blob/master/Documentation/ERD%20Project.png "Final ERD")

This final ERD shows how the database was set up in MySQL.

### Project Tracking <a name="projecttracking"></a>
Trello was used to track progress for the project. Trello provided a card based tracking system which allowed easy tracking of what tasks had to be started, which tasks were in progress and which tasks had been completed. Labels were used to manage cards and what each card had represented e.g. Orange labels were used to show items which were part of the minimum viable product. The Trello board can be accessed through the link below:

https://trello.com/b/lLE9XSb2/project

## Testing <a name="testing"></a>
Due to time constraints, only unit testing was implemented rather than both unit and integration testing. Unit testing was conducted using PyTest

[Link to coverage report](https://github.com/hsjhita1/QAProject1/blob/testing/test_results/test-at-May-05-on-20-20:37.pdf)

As shown in the coverage report, 95% coverage was achieved using PyTest. While this coverage shows that in the tests, 95% of code was called, this does not reflect on real world application.

## Deployment <a name="deployment"></a>
![alt text](https://github.com/hsjhita1/QAProject1/blob/master/Documentation/CI%20Pipeline.png "Pipeline")
The image above shows the process of how the application was deployed. Initially, code was created in Visual Studio Code using the Python and Flask language. This code was then pushed to a VCS, in this case GitHub, where it would be stored inside a repository. To keep track of what code was completed, a Trello board was used. Once a task had been completed on Trello, the task was attached to the commit in which the code was in. Once a new task was taken on, the repository was pulled to make sure the latest code was on hand and then the task would then be carried out. 

While this was being carried out, a WebHook would automatically pull the code from GitHub to the CI Server, Jenkins. Using a shell script, the build was made automatically. From this, multiple operations were taking place. The first would be testing. The code would be tested to make sure it works as intended. Alongside this, a testing environment would be active which also allowed for dynamic and live development which meant some changes could be seen in real time. And finally, the live version of the application would be running using GUnicorn and a GCP Virtual Machine.

## Self Reflection <a name="selfreflection"></a>
The final build of the application met the necessary criteria which the projet had to fufuill. The application was able to meet the CRUD criteria. It had also managed to meet the additional requirements set for the project in acheiving multiple tables with relationships and achieving a test coverage of 95%.

While I can say the overall project was a success, there are a few things on which I would improve on next time if I were to undertake a similar project.
1. Implementing the market feature to its fullest extent. 
 
   The idea for the market page was that users could list games in their collection for sale and other users could view and maybe purchase them. However, this was not fully implemented. Users could list games onto the market but even those that had existed outside of the collection. Upon reflection, I realise how I could have coded the feature in correctly given how my knowledge in Flask and Python had improved over the course of this project.
   
2. Implementing all the tables and columns missed

   After creating the inital tables and dataset, I had realised that the tables and columns I had not created would have created extra functionality of the application, and features which were not feasible with the current tables, could have been made.
   
3. Improving the appearance of the site

   While not a key element of the project, the website was very basic in terms of its appearance and perhaps could have used CSS styling to improve the appearance and also the usability of the site.
