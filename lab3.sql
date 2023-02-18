CREATE TABLE chair
(
	chair_id integer PRIMARY KEY,
	chair_name text NOT NULL,
	chair_deanery text NOT NULL
);

CREATE TABLE student_group
(
	group_id integer PRIMARY KEY,
	group_name text NOT NULL,
	chair_id integer NOT NULL,
	FOREIGN KEY (chair_id) REFERENCES chair(chair_id)
);

CREATE TABLE students
(
	student_id integer PRIMARY KEY,
	student_name text NOT NULL,
	student_passport integer NOT NULL,
	group_id integer NOT NULL,
	FOREIGN KEY (group_id) REFERENCES student_group(group_id)
);

INSERT INTO chair (chair_id, chair_name, chair_deanery)
VALUES
(1, 'Информационные технологии', 'Информатика'),
(2, 'Сети и системы связи', 'Сети связи и системы коммуникации');

INSERT INTO student_group (group_id, group_name, chair_id)
VALUES
(1, 'БВТ2201', 1),
(2, 'БВТ2202', 1),
(3, 'БРТ2201', 2),
(4, 'БРТ2202', 2);

INSERT INTO students (student_id, student_name, student_passport, group_id)
VALUES
(1, 'Сергей', 14086734, 1),
(2, 'Илья', 14085489, 1),
(3, 'Маргарита', 14089721, 1),
(4, 'Артем', 14073481, 1),
(5, 'Екатерина', 14083917, 1),
(6, 'Егор', 14059430, 2),
(7, 'Павел', 14085495, 2),
(8, 'Ольга', 14068120, 2),
(9, 'Мария', 14074280, 2),
(10, 'Владимир', 14071257, 2),
(11, 'Сергей', 14095219, 3),
(12, 'Анна', 14031273, 3),
(13, 'Анастасия', 14061046, 3),
(14, 'Иван', 14079347, 3),
(15, 'Андрей', 14090567, 3),
(16, 'Александра', 14071528, 4),
(17, 'Артем', 14071374, 4),
(18, 'Роман', 14050416, 4),
(19, 'Даниил', 14081530, 4),
(20, 'Анна', 14059145, 4);
