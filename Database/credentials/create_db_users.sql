create user 'MonsterCardsDev'@'localhost' identified by 'TSitMonsterCards';
grant select, insert, update, delete, create, drop
	on MonsterCards.* to 'MonsterCardsDev'@'localhost';