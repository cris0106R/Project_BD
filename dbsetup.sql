/* type 'source ./dbsetup.sql' in mysql to run this script */

CREATE TABLE User (IdUser INT, name VARCHAR(20), email VARCHAR(40), balance INT, PRIMARY KEY (IdUser));
CREATE TABLE Room (IdRoom INT, room_name VARCHAR(20), room_capacity INT, PRIMARY KEY (IdRoom));
CREATE TABLE Game (IdGame INT, game_title VARCHAR(20), user_rating FLOAT, copyright INT, PRIMARY KEY (IdGame));
CREATE TABLE Session (IdSession INT, IdRoom INT, IdGame INT, date DATE, PRIMARY KEY (IdSession), FOREIGN KEY (IdRoom) REFERENCES Room(IdRoom), FOREIGN KEY (IdGame) REFERENCES Game(IdGame));
CREATE TABLE Reservation (IdReservation INT, IdSession INT, IdUser INT, time_alloc INT, PRIMARY KEY (IdReservation), FOREIGN KEY (IdSession) REFERENCES Session(IdSession), FOREIGN KEY (IdUser) REFERENCES User(IdUser));

/* Table values */
/* Room */
INSERT INTO Room (Room.IdRoom, Room.room_name, Room.room_capacity) VALUES (0, "Jabee", 4);
INSERT INTO Room (Room.IdRoom, Room.room_name, Room.room_capacity) VALUES (1, "Basler", 10);
INSERT INTO Room (Room.IdRoom, Room.room_name, Room.room_capacity) VALUES (2, "Prime", 14);
INSERT INTO Room (Room.IdRoom, Room.room_name, Room.room_capacity) VALUES (3, "Roche1", 18);
INSERT INTO Room (Room.IdRoom, Room.room_name, Room.room_capacity) VALUES (4, "Roche2", 22);

/* Game */
INSERT INTO Game (Game.IdGame, Game.game_title, Game.user_rating, Game.copyright) values (0, "Valorant", 3.8, 15);
INSERT INTO Game (IdGame, game_title, user_rating, copyright) VALUES (1, "Overwatch2", 3.8, 10);


INSERT INTO Reservation (Reservation.IdReservation, Reservation.IdSession, Reservation.IdUser, Reservation.time_alloc)
