/* 	Monster Cards Db Schema
	Authors: Sean Rice, Jake Kloman
    Proposed Schema:
		Users(PK_ID, First, MidInit, Last, Email)
        UserLogins(PK_AuthToken, FK_AccountID, ExpirationDate)
        Card(PK_ID, Name, ImgData, Attributes)
        UserCards(FK_UserID, FK_CardID)
*/


create database MonsterCards;
use MonsterCards;

create table Users(
	ID int auto_increment,
    Email varchar(255) not null,
    Password char(64) not null,
    UserName varchar(31),

    primary key (ID),
    unique (Email, UserName)
);

create table UserInfo(
    UserID int not null,
    First varchar(127),
    MidInit varchar(1),
    Last varchar(127),

    primary key(UserID),

    FOREIGN KEY (UserID)
        REFERENCES Users(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);
-- alter table Users
-- modify First varchar(127);

create table UserLogins(
	AccountID int not null,
	AuthToken varchar(255),
    ExpirationDate datetime not null,

    primary key (AccountID),
    unique (AuthToken),

    FOREIGN KEY (AccountID)
        REFERENCES Users(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

create table Cards(
	ID int auto_increment,
	Name varchar(255),
	ImgData BLOB,
    Attributes varchar(511),

	primary key (ID)
);

create table UsersCards(
	UserID int,
	CardID int,

	foreign key (UserID)
        REFERENCES Cards(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

	foreign key (CardID)
        REFERENCES Users(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    unique(UserID, CardID)
);
