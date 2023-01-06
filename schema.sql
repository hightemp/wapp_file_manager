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

DROP TABLE IF EXISTS fav_groups;
CREATE TABLE fav_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS fav_categories;
CREATE TABLE fav_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_id INTEGER NULL,
    parent_id INTEGER NULL
);

DROP TABLE IF EXISTS fav_files;
CREATE TABLE fav_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT nULL,
    category_id INTEGER NULL
);