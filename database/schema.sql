--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: diplomacy; Type: SCHEMA; Schema: -; Owner: skallaher
--

CREATE SCHEMA diplomacy;


ALTER SCHEMA diplomacy OWNER TO skallaher;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: add_em(integer, integer); Type: FUNCTION; Schema: public; Owner: skallaher
--

CREATE FUNCTION add_em(integer, integer) RETURNS integer
    LANGUAGE sql
    AS $_$SELECT $1 + $2;$_$;


ALTER FUNCTION public.add_em(integer, integer) OWNER TO skallaher;

SET search_path = diplomacy, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: color; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE color (
    name character varying NOT NULL,
    r integer NOT NULL,
    g integer NOT NULL,
    b integer NOT NULL
);


ALTER TABLE diplomacy.color OWNER TO skallaher;

--
-- Name: location; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE location (
    xpos integer NOT NULL,
    ypos integer NOT NULL,
    ispoi boolean NOT NULL,
    id integer NOT NULL,
    type integer
);


ALTER TABLE diplomacy.location OWNER TO skallaher;

--
-- Name: unit; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE unit (
    id integer NOT NULL,
    isnaval boolean,
    location integer,
    curorder integer
);


ALTER TABLE diplomacy.unit OWNER TO skallaher;

--
-- Name: player; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE player (
    firstname character varying,
    lastname character varying,
    units unit[],
    owned location[],
    id integer NOT NULL
);


ALTER TABLE diplomacy.player OWNER TO skallaher;

--
-- Name: faction; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE faction (
    id integer NOT NULL,
    name character varying,
    color color,
    player player
);


ALTER TABLE diplomacy.faction OWNER TO skallaher;

SET search_path = public, pg_catalog;

--
-- Name: faction_equal_procedure(diplomacy.faction, diplomacy.faction); Type: FUNCTION; Schema: public; Owner: skallaher
--

CREATE FUNCTION faction_equal_procedure(diplomacy.faction, diplomacy.faction) RETURNS boolean
    LANGUAGE sql
    AS $_$SELECT $1.id = $2.id;$_$;


ALTER FUNCTION public.faction_equal_procedure(diplomacy.faction, diplomacy.faction) OWNER TO skallaher;

--
-- Name: get_player(integer); Type: FUNCTION; Schema: public; Owner: skallaher
--

CREATE FUNCTION get_player(integer) RETURNS diplomacy.player
    LANGUAGE sql
    AS $_$SELECT * FROM diplomacy.player WHERE id = $1;$_$;


ALTER FUNCTION public.get_player(integer) OWNER TO skallaher;

--
-- Name: get_units(integer); Type: FUNCTION; Schema: public; Owner: skallaher
--

CREATE FUNCTION get_units(integer) RETURNS TABLE(faction_id integer, units diplomacy.unit[])
    LANGUAGE sql
    AS $_$SELECT faction.id, player.units FROM diplomacy.faction, diplomacy.player WHERE faction = ANY(SELECT unnest(game.factions) FROM diplomacy.game WHERE game.gameid = $1);$_$;


ALTER FUNCTION public.get_units(integer) OWNER TO skallaher;

--
-- Name: test(); Type: FUNCTION; Schema: public; Owner: skallaher
--

CREATE FUNCTION test() RETURNS integer
    LANGUAGE sql
    AS $$SELECT 1 as RESULT$$;


ALTER FUNCTION public.test() OWNER TO skallaher;

SET search_path = diplomacy, pg_catalog;

--
-- Name: faction_id_seq; Type: SEQUENCE; Schema: diplomacy; Owner: skallaher
--

CREATE SEQUENCE faction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diplomacy.faction_id_seq OWNER TO skallaher;

--
-- Name: faction_id_seq; Type: SEQUENCE OWNED BY; Schema: diplomacy; Owner: skallaher
--

ALTER SEQUENCE faction_id_seq OWNED BY faction.id;


--
-- Name: game; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE game (
    factions faction[],
    gameid integer NOT NULL
);


ALTER TABLE diplomacy.game OWNER TO skallaher;

--
-- Name: game_gameid_seq; Type: SEQUENCE; Schema: diplomacy; Owner: skallaher
--

CREATE SEQUENCE game_gameid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diplomacy.game_gameid_seq OWNER TO skallaher;

--
-- Name: game_gameid_seq; Type: SEQUENCE OWNED BY; Schema: diplomacy; Owner: skallaher
--

ALTER SEQUENCE game_gameid_seq OWNED BY game.gameid;


--
-- Name: location_id_seq; Type: SEQUENCE; Schema: diplomacy; Owner: skallaher
--

CREATE SEQUENCE location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diplomacy.location_id_seq OWNER TO skallaher;

--
-- Name: location_id_seq; Type: SEQUENCE OWNED BY; Schema: diplomacy; Owner: skallaher
--

ALTER SEQUENCE location_id_seq OWNED BY location.id;


--
-- Name: loctype; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE loctype (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE diplomacy.loctype OWNER TO skallaher;

--
-- Name: ordertype; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE ordertype (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE diplomacy.ordertype OWNER TO skallaher;

--
-- Name: player_id_seq; Type: SEQUENCE; Schema: diplomacy; Owner: skallaher
--

CREATE SEQUENCE player_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diplomacy.player_id_seq OWNER TO skallaher;

--
-- Name: player_id_seq; Type: SEQUENCE OWNED BY; Schema: diplomacy; Owner: skallaher
--

ALTER SEQUENCE player_id_seq OWNED BY player.id;


--
-- Name: testunit; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE testunit (
    id integer NOT NULL,
    faction_id integer
);


ALTER TABLE diplomacy.testunit OWNER TO skallaher;

--
-- Name: testunit_id_seq; Type: SEQUENCE; Schema: diplomacy; Owner: skallaher
--

CREATE SEQUENCE testunit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diplomacy.testunit_id_seq OWNER TO skallaher;

--
-- Name: testunit_id_seq; Type: SEQUENCE OWNED BY; Schema: diplomacy; Owner: skallaher
--

ALTER SEQUENCE testunit_id_seq OWNED BY testunit.id;


--
-- Name: unit_id_seq; Type: SEQUENCE; Schema: diplomacy; Owner: skallaher
--

CREATE SEQUENCE unit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diplomacy.unit_id_seq OWNER TO skallaher;

--
-- Name: unit_id_seq; Type: SEQUENCE OWNED BY; Schema: diplomacy; Owner: skallaher
--

ALTER SEQUENCE unit_id_seq OWNED BY unit.id;


--
-- Name: unitorder; Type: TABLE; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

CREATE TABLE unitorder (
    id integer NOT NULL,
    type integer,
    target integer
);


ALTER TABLE diplomacy.unitorder OWNER TO skallaher;

--
-- Name: unitorder_id_seq; Type: SEQUENCE; Schema: diplomacy; Owner: skallaher
--

CREATE SEQUENCE unitorder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diplomacy.unitorder_id_seq OWNER TO skallaher;

--
-- Name: unitorder_id_seq; Type: SEQUENCE OWNED BY; Schema: diplomacy; Owner: skallaher
--

ALTER SEQUENCE unitorder_id_seq OWNED BY unitorder.id;


--
-- Name: id; Type: DEFAULT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY faction ALTER COLUMN id SET DEFAULT nextval('faction_id_seq'::regclass);


--
-- Name: gameid; Type: DEFAULT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY game ALTER COLUMN gameid SET DEFAULT nextval('game_gameid_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY location ALTER COLUMN id SET DEFAULT nextval('location_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY player ALTER COLUMN id SET DEFAULT nextval('player_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY testunit ALTER COLUMN id SET DEFAULT nextval('testunit_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY unit ALTER COLUMN id SET DEFAULT nextval('unit_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY unitorder ALTER COLUMN id SET DEFAULT nextval('unitorder_id_seq'::regclass);


--
-- Name: color_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY color
    ADD CONSTRAINT color_pkey PRIMARY KEY (name);


--
-- Name: faction_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY faction
    ADD CONSTRAINT faction_pkey PRIMARY KEY (id);


--
-- Name: game_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY game
    ADD CONSTRAINT game_pkey PRIMARY KEY (gameid);


--
-- Name: location_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY location
    ADD CONSTRAINT location_pkey PRIMARY KEY (id);


--
-- Name: loctype_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY loctype
    ADD CONSTRAINT loctype_pkey PRIMARY KEY (id);


--
-- Name: ordertype_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY ordertype
    ADD CONSTRAINT ordertype_pkey PRIMARY KEY (id);


--
-- Name: player_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY player
    ADD CONSTRAINT player_pkey PRIMARY KEY (id);


--
-- Name: testunit_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY testunit
    ADD CONSTRAINT testunit_pkey PRIMARY KEY (id);


--
-- Name: unit_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY unit
    ADD CONSTRAINT unit_pkey PRIMARY KEY (id);


--
-- Name: unitorder_pkey; Type: CONSTRAINT; Schema: diplomacy; Owner: skallaher; Tablespace: 
--

ALTER TABLE ONLY unitorder
    ADD CONSTRAINT unitorder_pkey PRIMARY KEY (id);


--
-- Name: curorder; Type: FK CONSTRAINT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY unit
    ADD CONSTRAINT curorder FOREIGN KEY (curorder) REFERENCES unitorder(id);


--
-- Name: location; Type: FK CONSTRAINT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY unit
    ADD CONSTRAINT location FOREIGN KEY (location) REFERENCES location(id);


--
-- Name: target; Type: FK CONSTRAINT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY unitorder
    ADD CONSTRAINT target FOREIGN KEY (target) REFERENCES location(id);


--
-- Name: testunit_faction_id_fkey; Type: FK CONSTRAINT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY testunit
    ADD CONSTRAINT testunit_faction_id_fkey FOREIGN KEY (faction_id) REFERENCES faction(id);


--
-- Name: type; Type: FK CONSTRAINT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY location
    ADD CONSTRAINT type FOREIGN KEY (type) REFERENCES loctype(id) MATCH FULL;


--
-- Name: type; Type: FK CONSTRAINT; Schema: diplomacy; Owner: skallaher
--

ALTER TABLE ONLY unitorder
    ADD CONSTRAINT type FOREIGN KEY (type) REFERENCES ordertype(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

