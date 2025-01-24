DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS sharing;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  public_key TEXT NOT NULL,
  key_length TEXT NOT NULL, 
  api_token TEXT,
  verify_token TEXT
);

CREATE TABLE files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  location TEXT NOT NULL,
  real_name TEXT NOT NULL,
  checksum TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE sharing (
  file_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  passphrase TEXT NOT NULL,
  FOREIGN KEY (file_id) REFERENCES files (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);
