create database project_management;
use project_management;
create table project (
	id int not null auto_increment,
	name varchar(100),
	roll_no int,
	team_member1 varchar(100),
	team_member2 varchar(100),
	supervisor varchar(100),
	batch varchar(100),
	session int,
	date_created datetime default current_timestamp,
primary key (id)
);
