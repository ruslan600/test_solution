CREATE TABLE project (
	id SERIAL PRIMARY KEY,
	name varchar(50) NOT NULL,
	description varchar(255) NOT NULL
);


CREATE TABLE server (
	id SERIAL PRIMARY KEY,
	name varchar(50) NOT NULL,
	ip_address varchar(50) NOT NULL,
	description varchar(255) NOT NULL
);


CREATE TABLE recognition_results (
	id SERIAL PRIMARY KEY,
	project_id int REFERENCES project(id) ON DELETE CASCADE,
	server_id int REFERENCES server(id) ON DELETE CASCADE,
	date date,
	time time,
	unique_id UUID NOT NULL,
	rec_result varchar(50) NOT NULL,
	phone_number varchar(50) NOT NULL,
	duration numeric NOT NULL,
	transcript text
);
