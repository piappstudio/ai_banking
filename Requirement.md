I wanted to refactor this project in proper way.
Currently it is a python tool directed connect with mysql server directly to provide the banking functionalites.

The issue is, it is exposing all the data outside. NO login functionality or session based stuffs.

Now. I wanted to create a plan to execute the following stuffs.
1. Create laravel platform to expose the banking functionalities. Use `laravel-add-api` SKILL to add new functionalities. 
2. This apis should use sanctum api authorization
3. Customer 
2. Update the Database with approriate column, if it is missing. 