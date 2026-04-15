
#  Pet Shop Ordering Management System (PSOMS) -- Team 1

𝐎𝐯𝐞𝐫𝐯𝐢𝐞𝐰

The Pet Shop Ordering Management System (PSOMS) is a system specifically designed to aid in creating a new ordering system for pet shops. 




## Authors

- [@demaincpe](https://github.com/demaincpe)
- [@qpjcuadera-cpe](https://github.com/qpjcuadera-cpe)
- [@Libo-oncpe](https://github.com/Libo-oncpe)
- [@qwsponce-cloud](https://github.com/qwsponce-cloud)
- [@RealubitCPE](https://github.com/RealubitCPE)
# Features
* User Sign-up
Create a new account by registering with a username, password, and role. The system checks for duplicates before saving it into a JSON file in the form of a dictionary.

* Login System and Account Security
Log in using a username and password. Passwords are hashed using SHA-256. Successful login grants access based on the user's assigned role upon sign-up.

* Admin Product Management
Admin account are able to add, update, and store information about new and current products.

* Normal User Access
Normal user accounts have restricted access. They can browse animals and make reservations but is not able to modify the catalog.

* Display Animal Products and Information
View important information about the animal, along with their image references and stock to give the normal users information before making the decision in reserving one for themself.

* Stock Tracking
Tracks the number of available stock for each animal product. Admins are able to update the stock and the changes are immediately reflected for the other users.

* Reservation System
Customers are able to reserve animals from the catalog along with view their own reservation history. 