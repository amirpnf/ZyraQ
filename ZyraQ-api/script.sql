CREATE TABLE Question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    image BLOB,
    position INTEGER
);


CREATE TABLE Answer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question INTEGER NOT NULL,
    isCorrect INTEGER NOT NULL CHECK (isCorrect IN (0, 1)),
    text TEXT NOT NULL,
    FOREIGN KEY(question) REFERENCES Question(id) ON DELETE CASCADE
);