DROP TABLE IF EXISTS tabs;
CREATE TABLE tabs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    path TEXT NOT NULL,
    selected_file TEXT NULL
);

DROP TABLE IF EXISTS tabs_history;
CREATE TABLE tabs_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tab_id INTEGER NULL,
    path TEXT NOT NULL,
    selected_file TEXT NULL
);

INSERT INTO tabs (title, path) VALUES ("test 1", "/home/hightemp");
INSERT INTO tabs (title, path) VALUES ("test 2", "/");
INSERT INTO tabs (title, path) VALUES ("test 3", "/home/hightemp/Pictures/");
INSERT INTO tabs (title, path) VALUES ("test 4", "/home/hightemp/.config/");
