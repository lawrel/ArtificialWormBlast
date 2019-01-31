/* 	Monster Cards Db Schema
 
	Authors: Sean Rice, (add your name here)
    
	TODO: Determine the initial database schema, probably after the initial project description.
    
    Proposed Schema:
		User(ID*, First, MidInit, Last, Email)
        Card(ID*, Name, DoodleData)
    */

use MonsterCards;
create table Users(
	ID int auto_increment,
    First varchar(127),
    MidInit varchar(1),
    Last varchar(127),
    Email varchar(255),
    primary key (ID),
    unique (Email)
);