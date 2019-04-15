create user 'MonsterCardsDev'@'%' identified by 'TSitMonsterCards';
grant select, insert, update, delete, create, drop
	on MonsterCards.* to 'MonsterCardsDev'@'%';