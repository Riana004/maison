INSERT INTO accessibilites (nom) VALUES 
('Aucun'),
('Moto'),
('Voiture'),
('Voiture avec parking');
INSERT INTO types (nom, logement) VALUES 
('F2', 'appartement'),
('F3', 'appartement'),
('F4', 'appartement'),
('F5', 'appartement'),
('F6', 'appartement'),
('F7', 'appartement'),
('T3', 'maison'),
('T4', 'maison'),
('Villa', 'maison');
INSERT INTO types_papiers (nom) VALUES 
('Titre et borne'),
('Cadastre'),
('autres');
INSERT INTO maisons (ville, accessibilite, type, commodite, nb_chambres, prix) VALUES 
('Antananarivo', 3, 1, 'interieur', 2, 250000000),
('Antananarivo', 4, 2, 'exterieur', 3, 380000000),
('Toamasina', 2, 3, 'interieur', 4, 180000000),
('Antsirabe', 3, 4, 'exterieur', 3, 150000000),
('Mahajanga', 1, 5, 'exterieur', 4, 320000000),
('Fianarantsoa', 3, 4, 'interieur', 5, 450000000),
('Antananarivo', 4, 4, 'interieur', 13, 7000000),
('Ambatobe', 4, 5, 'interieur', 16, 9260000),
('Antananarivo', 4, 2, 'interieur', 4, 2000000),
('Antananarivo', 4, 5, 'interieur', 11, 4500000),
('Antananarivo', 4, 3, 'interieur', 6, 15000000),
('Antananarivo', 4, 3, 'interieur', 8, 3000000),
('Antananarivo', 4, 4, 'interieur', 13, 11250000),
('Antananarivo', 4, 4, 'interieur', 16, 8000000),
('Antananarivo', 4, 6, 'interieur', 4, 24000000),
('Antananarivo', 4, 1, 'interieur', 12, 2000000),
('Antananarivo', 4, 4, 'interieur', 10, 7500000),
('Antananarivo', 4, 3, 'interieur', 13, 8500000);
INSERT INTO terrains (ville, type_papier, superficie, accessibilite, est_cloture, est_pret_a_construire, prix) VALUES 
('Ambatobe', '1', 839, '3', TRUE, TRUE, 60000*839),
('Ambatobe', '1', 1235, '3', TRUE, TRUE, 60000*1235),
('Ivato', '1', 2200, '3', TRUE, TRUE, 750000 * 2200),
('Antananarivo', '1', 500, 3, TRUE, TRUE, 750000000), 
('Antananarivo', '1', 250, 4, FALSE, TRUE, 400000000),  
('Toamasina', '2', 1000, 2, TRUE, FALSE, 600000000),   
('Antsirabe', '2', 750, 3, FALSE, FALSE, 300000000),    
('Mahajanga', '1', 1500, 1, TRUE, TRUE, 900000000),   
('Fianarantsoa', '2', 2000, 3, TRUE, FALSE, 800000000), 
('Ambatolampy', '2', 2277, 3, TRUE, TRUE, 398475000),  
('Ambohidratrimo', '2', 1867, 3, TRUE, TRUE, 1213550000); 