use MonsterCards;

/*  Account(ID, Email, First, MidInit, Last, Password)
	
    ID is the primary key. It uses AUTO_INCREMENT to generate the userid.
    Emails are unique.
    Passwords should be encrypted strings.
*/

/*  You will need to enter minimal account info. The ID auto populates. */
insert into Users (Email, Password) values("sheryl@example.com", "Password");

/*  We will keep our password entries in the database with sha-256 encryption because we're good people. :)  */
insert into Users (Email, First, Password) values("bob@example.com", "Bob", sha2("password", 256));

/*  Show everyone in the table. Notice how the Password field is encrypted */
select * from Users;

/*	Delete users  */
-- delete from Users where Email = "email";

/*	UserLogins tests:
		All fields Unique
        All fields non null
        Foreign key add/delete tests
*/

