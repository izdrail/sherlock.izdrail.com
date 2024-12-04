# Mobile security application - security.izdrail.com

## Open source OSINT application

### Motivation
This application was built at the Orange Hackathon in 2024. I’ve built this application to help people keep their social security safe and to fight cybercrime. Talking with friends during my career as Software Engineer, I realized that many people don’t know how to protect themselves from cybercrime, including my own family.

### Who is it for?
Parents, teachers, students, and anyone else who wants to learn more about a person, organization, phone number, or email address.
Governments use these types of tools to gather information on potential threats and adversaries.
Law enforcement agencies can use it or implement to investigate crimes and identify suspects.
Cybersecurity professionals use OSINT to identify vulnerabilities and potential cyberattacks.
Businesses can use OSINT to gather information on competitors, customers, and market trends.
Journalists use OSINT to research and report on news stories.
Researchers use OSINT to gather information for their research projects.

### What can it do?
It is a web application that allows users to search for information about a phone number,email address, or domain name. 

The application uses the available free SpiderFoot modules to perform the search. The results are displayed in a user-friendly format, making it easy for users to understand and interpret the information.


## Develoment
How to run the app locally
I have built a docker image that contains the backend and the frontend. 
To run the app locally, you need to have docker installed on your machine.

1. Clone the repository
```git clone https://github.com/izdrail/security.izdrail.com.git```
2. Build the docker image:
```docker build -t izdrail/security.izdrail.com:latest .```

3. Run the docker image
```docker run -p 10000:10000 izdrail/security.izdrail.com:latest```
4. Access the frontend at http://localhost:10000