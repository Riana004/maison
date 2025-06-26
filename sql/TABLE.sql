CREATE DATABASE IF NOT EXISTS immobilier;
\c immobilier;

CREATE TABLE accessibilites(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(20) NOT NULL
);

CREATE TABLE types(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(20) NOT NULL,
    logement VARCHAR(20) NOT NULL
);

CREATE TABLE types_papiers(
    id SERIAL PRIMARY KEY,
    nom VARCHAR(20) NOT NULL
);

CREATE TABLE maisons(
    id SERIAL PRIMARY KEY,
    ville VARCHAR(20) NOT NULL,
    accessibilite INT references accessibilites(id),
    type INT references types(id),
    commodite VARCHAR(20) NOT NULL,
    nb_chambres INT NOT NULL,
    prix INT NOT NULL
);

CREATE TABLE terrains(
    id SERIAL PRIMARY KEY,
    ville VARCHAR(20) NOT NULL,
    superficie INT NOT NULL,
    type_papier INT references types_papiers(id),
    accessibilite INT references accessibilites(id),
    est_cloture BOOLEAN NOT NULL,
    est_pret_a_construire BOOLEAN NOT NULL,
    prix INT NOT NULL
);