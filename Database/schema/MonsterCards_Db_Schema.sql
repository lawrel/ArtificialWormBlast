/* 	Monster Cards Db Schema
 
	Authors: Sean Rice, (add your name here)
    
    Proposed Schema:
		Users(PK_ID, First, MidInit, Last, Email)
        UserLogins(PK_AuthToken, FK_AccountID, ExpirationDate)
        
        Card(ID*, Name, DoodleData)
*/

create database MonsterCards;
use MonsterCards;

create table Users(
	ID int auto_increment,
    First varchar(127),
    MidInit varchar(1),
    Last varchar(127),
    Email varchar(255) not null,
    Password char(64) not null,
    
    primary key (ID),
    unique (Email)
);
-- alter table Users
-- modify First varchar(127);

create table UserLogins(
	AuthToken varchar(255),
    AccountID int not null,
    ExpirationDate datetime not null,
    
    primary key (AuthToken),
    unique (AccountID),
    
    FOREIGN KEY (AccountID)
        REFERENCES Users(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);