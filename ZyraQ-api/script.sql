CREATE TABLE Question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    difficulty TEXT NOT NULL DEFAULT 'easy',
    image BLOB,
    position INTEGER
);

CREATE TABLE Answer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    isCorrect INTEGER NOT NULL CHECK (isCorrect IN (0, 1)),
    text TEXT NOT NULL,
    FOREIGN KEY(question_id) REFERENCES Question(id) ON DELETE CASCADE
);

CREATE TABLE Player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playerName TEXT NOT NULL,
    answers TEXT,
    score INTEGER DEFAULT
);
