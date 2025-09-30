-- ---------------- Questions ----------------
INSERT INTO Question (title, text, difficulty, image, position) VALUES
('Énigme 1', 'Quel est le résultat de 2 + 2 ?', 'Facile', NULL, 1),
('Énigme 2', 'Quelle couleur obtient-on en mélangeant le rouge et le bleu ?', 'Facile', NULL, 2),
('Énigme 3', 'Combien de continents y a-t-il sur Terre ?', 'Facile', NULL, 3),
('Énigme 4', 'Quelle planète est la plus proche du Soleil ?', 'Facile', NULL, 4),
('Énigme 5', 'Quelle est la capitale de la France ?', 'Facile', NULL, 5),
('Énigme 6', 'Quel animal est le roi de la jungle ?', 'Facile', NULL, 6),
('Énigme 7', 'Combien de côtés a un hexagone ?', 'Facile', NULL, 7),
('Énigme 8', 'Quelle langue est parlée au Brésil ?', 'Facile', NULL, 8),
('Énigme 9', 'Combien d''heures y a-t-il dans une journée ?', 'Facile', NULL, 9),
('Énigme 10', 'Quelle est la plus grande planète du système solaire ?', 'Facile', NULL, 10),
('Énigme 11', 'Qui a peint la Joconde ?', 'Moyen', NULL, 11),
('Énigme 12', 'Quelle est la formule chimique de l''eau ?', 'Facile', NULL, 12),
('Énigme 13', 'Quel est le plus grand océan du monde ?', 'Facile', NULL, 13),
('Énigme 14', 'Combien de planètes dans le système solaire ?', 'Facile', NULL, 14),
('Énigme 15', 'Quel est l''animal le plus rapide ?', 'Moyen', NULL, 15),
('Énigme 16', 'Quel métal a pour symbole Fe ?', 'Facile', NULL, 16),
('Énigme 17', 'Qui a écrit "Le Petit Prince" ?', 'Facile', NULL, 17),
('Énigme 18', 'Quelle est la capitale du Japon ?', 'Facile', NULL, 18),
('Énigme 19', 'Quel est le plus grand désert du monde ?', 'Moyen', NULL, 19),
('Énigme 20', 'Quel est le carré de 12 ?', 'Facile', NULL, 20);

-- ---------------- Answers ----------------
-- Question 1
INSERT INTO Answer (question, text, isCorrect) VALUES (1, '3', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (1, '4', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (1, '5', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (1, '22', 0);

-- Question 2
INSERT INTO Answer (question, text, isCorrect) VALUES (2, 'Vert', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (2, 'Violet', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (2, 'Orange', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (2, 'Rose', 0);

-- Question 3
INSERT INTO Answer (question, text, isCorrect) VALUES (3, '5', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (3, '6', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (3, '7', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (3, '7', 1);

-- Question 4
INSERT INTO Answer (question, text, isCorrect) VALUES (4, 'Mercure', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (4, 'Vénus', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (4, 'Terre', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (4, 'Mars', 0);

-- Question 5
INSERT INTO Answer (question, text, isCorrect) VALUES (5, 'Paris', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (5, 'Lyon', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (5, 'Marseille', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (5, 'Nice', 0);

-- Question 6
INSERT INTO Answer (question, text, isCorrect) VALUES (6, 'Lion', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (6, 'Tigre', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (6, 'Éléphant', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (6, 'Ours', 0);

-- Question 7
INSERT INTO Answer (question, text, isCorrect) VALUES (7, '5', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (7, '6', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (7, '7', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (7, '8', 0);

-- Question 8
INSERT INTO Answer (question, text, isCorrect) VALUES (8, 'Portugais', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (8, 'Espagnol', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (8, 'Français', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (8, 'Anglais', 0);

-- Question 9
INSERT INTO Answer (question, text, isCorrect) VALUES (9, '12', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (9, '24', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (9, '48', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (9, '30', 0);

-- Question 10
INSERT INTO Answer (question, text, isCorrect) VALUES (10, 'Jupiter', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (10, 'Saturne', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (10, 'Terre', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (10, 'Mars', 0);

-- Question 11
INSERT INTO Answer (question, text, isCorrect) VALUES (11, 'Leonard de Vinci', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (11, 'Michel-Ange', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (11, 'Raphael', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (11, 'Pablo Picasso', 0);

-- Question 12
INSERT INTO Answer (question, text, isCorrect) VALUES (12, 'H2O', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (12, 'CO2', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (12, 'O2', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (12, 'NaCl', 0);

-- Question 13
INSERT INTO Answer (question, text, isCorrect) VALUES (13, 'Océan Atlantique', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (13, 'Océan Pacifique', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (13, 'Océan Indien', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (13, 'Océan Arctique', 0);

-- Question 14
INSERT INTO Answer (question, text, isCorrect) VALUES (14, '7', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (14, '8', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (14, '9', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (14, '6', 0);

-- Question 15
INSERT INTO Answer (question, text, isCorrect) VALUES (15, 'Guépard', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (15, 'Lion', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (15, 'Tigre', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (15, 'Éléphant', 0);

-- Question 16
INSERT INTO Answer (question, text, isCorrect) VALUES (16, 'Fer', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (16, 'Or', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (16, 'Cuivre', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (16, 'Plomb', 0);

-- Question 17
INSERT INTO Answer (question, text, isCorrect) VALUES (17, 'Antoine de Saint-Exupéry', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (17, 'Victor Hugo', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (17, 'Jules Verne', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (17, 'Émile Zola', 0);

-- Question 18
INSERT INTO Answer (question, text, isCorrect) VALUES (18, 'Tokyo', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (18, 'Kyoto', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (18, 'Osaka', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (18, 'Nagasaki', 0);

-- Question 19
INSERT INTO Answer (question, text, isCorrect) VALUES (19, 'Sahara', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (19, 'Désert de Gobi', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (19, 'Désert de l''Antarctique', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (19, 'Kalahari', 0);

-- Question 20
INSERT INTO Answer (question, text, isCorrect) VALUES (20, '144', 1);
INSERT INTO Answer (question, text, isCorrect) VALUES (20, '124', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (20, '142', 0);
INSERT INTO Answer (question, text, isCorrect) VALUES (20, '154', 0);
