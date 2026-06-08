# 3-PL (3D Printer Log)
3-PL is a python customTkinter application designed for organisations such as universities/schools to track and monitor usage of 3D printers. This application functions as a digital logbook where users enter information about their print job every time they use a 3D printer. The application can also store information about the printers and filament materials available for use that can be selected from when making a log entry. This thus gives organisations greater traceability and accountability over the use of their 3D printers

3-PL features secure login access with all passwords stored as a hashed string, preventing attackers from viewing passwords even if they are stolen. 3-PL also contains an authorisation system, allowing administrators to choose the level of access that users are given. Access levels and authorised actions are detailed below:

|Access Level|Authorised Actions|
| --- | --- |
| 5 | Admin access: can create accounts and authorise users |
| 4 | can view all accounts, add new printers and materials |
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
**access_level**: 4  

**Name**: Olivia Doe  
**id**: 135135  
**password**: qwerty  
**access_level**: 4  

**Name**: Bob Builder  
**id**: 654321  
**password**: password  
**access_level**: 1  

