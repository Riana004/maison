CREATE OR REPLACE FUNCTION inserer_maison_commodites(
    p_ville TEXT,
    p_nb_chambres INTEGER,
    p_prix INTEGER,
    p_accessibilite INTEGER,
    p_type INTEGER,
    p_commodites INTEGER[]
) RETURNS VOID AS $$
DECLARE
    v_maison_id INTEGER;
    v_commodite_id INTEGER;
BEGIN
    -- Insérer la maison
    INSERT INTO maisons (ville, nb_chambres, prix, accessibilite, "type")
    VALUES (p_ville, p_nb_chambres, p_prix, p_accessibilite, p_type)
    RETURNING id INTO v_maison_id;
    
    -- Insérer chaque commodité
    FOREACH v_commodite_id IN ARRAY p_commodites LOOP
        INSERT INTO maison_commodites (maison_id, commodite_id)
        VALUES (v_maison_id, v_commodite_id);
    END LOOP;
END;
$$ LANGUAGE plpgsql;