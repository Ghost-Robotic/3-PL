# 3-PL (3D Printer Log)
3-PL is a python customTkinter application designed for organisations such as universities/schools to track and monitor usage of 3D printers. This application functions as a digital logbook where users enter information about their print job every time they use a 3D printer. The application can also store information about the printers and filament materials available for use that can be selected from when making a log entry. This thus gives organisations greater traceability and accountability over the use of their 3D printers

3-PL features secure login access with all passwords stored as a hashed string, preventing attackers from viewing passwords even if they are stolen. 3-PL also contains an authorisation system, allowing administrators to choose the level of access that users are given. Access levels and authorised actions are detailed below:

|Access Level|Authorised Actions|
| --- | --- |
| 5 | Admin access: can create/edit accounts and authorise users, add new printers |
| 4 | can view all accounts, add new materials |
| 3 | can view logs |
| 2 | can add logs |
| 1 | can only view materials and printers |

## Test Accounts
**Name**: John Doe  
**id**: 123456  
**password**: admin  
**access_level**: 5  

**Name**: Thomas Smith  
**id**: 987654  
**password**: 123456  
**access_level**: 4  

**Name**: Amelia Smith  
**id**: 246246  
**password**: password123  
**access_level**: 3  

**Name**: Olivia Doe  
**id**: 135135  
**password**: qwerty  
**access_level**: 2  

**Name**: Bob Builder  
**id**: 654321  
**password**: password  
**access_level**: 1  

|ID|Name|Password|Access Level|
| --- | --- | --- | :---: |
| 123456 | John Doe | admin | 5 |
| 987654 | Thomas Smith | 123456 | 4 |
| 246246 | Amelia Smith | password123 | 3 |
| 135135 | Olivia Doe | qwerty | 2 |
| 654321 | Bob Builder | password | 1 |
| 396886 | Carina Collins | password1 | 4 |
| 321321 | Christian Janis | password2 | 2 |
| 123123 | Beth Jang | password3 | 3 |
| 654123 | Jane Dough | password4 | 1 |
| 903123 | Ellen Joe | password5 | 3 |
| 687345 | Dan Tedum | password6 | 4 |
| 987456 | Jenny Maud | password7 | 3 |
| 763957 | Tray Aurus | password8 | 2 |
