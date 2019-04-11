/* 	Monster Cards Db Schema

	Authors: Sean Rice, (add your name here)

    Proposed Schema:
		Users(PK_ID, First, MidInit, Last, Email)
        UserLogins(PK_AuthToken, FK_AccountID, ExpirationDate)

        Card(ID*, Name, DoodleData)
*/
drop table Users;


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
	CardName varchar(256),
	ImgData BLOB not null,

	primary key (CardID)
);

create table PlayerCards(
	PlayerID int,
	CardID int

	foreign key (PlayerID),
	foreign key (CardID)

	REFERENCES Cards(ID)
	ON DELETE CASCADE
    ON UPDATE CASCADE

	REFERENCES Users(ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

begin;
SELECT ID, Email, Password FROM MonsterCards.Users
WHERE Email = "" AND Password = sha2("",256);
commit;
