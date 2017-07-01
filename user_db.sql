ALTER TABLE IF EXISTS ONLY public.starwars_users DROP CONSTRAINT IF EXISTS pk_starwars_users_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.starwars_planets DROP CONSTRAINT IF EXISTS pk_starwars_planets_id CASCADE;

DROP TABLE IF EXISTS public.starwars_users;
DROP SEQUENCE IF EXISTS public.starwars_users_id_seq;
CREATE TABLE starwars_users (
    id serial NOT NULL,
    username VARCHAR(255),
    password VARCHAR(255)
);

DROP TABLE IF EXISTS public.starwars_planets;
DROP SEQUENCE IF EXISTS public.starwars_planets_id_seq;
CREATE TABLE starwars_planets (
    id serial NOT NULL,
    planetname VARCHAR(255),
    username VARCHAR(255)
);

ALTER TABLE ONLY starwars_users
    ADD CONSTRAINT pk_starwars_users_id PRIMARY KEY (id);

ALTER TABLE ONLY starwars_planets
    ADD CONSTRAINT pk_starwars_planets_id PRIMARY KEY (id);

INSERT INTO starwars_users VALUES (1, 'admin', '12345');
INSERT INTO starwars_planets VALUES (1, 'Alderaan', 'admin');
SELECT pg_catalog.setval('starwars_users_id_seq', 1, true);
SELECT pg_catalog.setval('starwars_planets_id_seq', 1, true);