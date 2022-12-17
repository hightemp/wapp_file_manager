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

DROP TABLE IF EXISTS rsync_sync;
CREATE TABLE rsync_sync (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NULL
);

DROP TABLE IF EXISTS rsync_options;
CREATE TABLE rsync_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rsync_sync_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL
);

DROP TABLE IF EXISTS rsync_sync_processes;
CREATE TABLE rsync_sync_processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rsync_sync_id INTEGER NOT NULL,
    exit_code INTEGER NULL,
    created_at INTEGER NOT NULL,
    stopped_at INTEGER NULL,
    progress INTEGER NOT NULL,
    stdout TEXT NULL,
    stderror TEXT NULL
);