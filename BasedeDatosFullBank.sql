--
-- PostgreSQL database dump
--

\restrict RyftbrgZzJU93OFUgAKUCNoWaIlNNUg2k30UN1AHeFoSFAaiKjJjfmCg88J4rDH

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-27 18:32:42

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 219 (class 1259 OID 16389)
-- Name: bank_full; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bank_full (
    age integer,
    job character varying(50),
    marital character varying(20),
    education character varying(20),
    "default" character varying(10),
    balance integer,
    housing character varying(5),
    loan character varying(5),
    contact character varying(20),
    day integer,
    month character varying(10),
    duration integer,
    campaign integer,
    pdays integer,
    previous integer,
    poutcome character varying(20),
    y character varying(5)
);


ALTER TABLE public.bank_full OWNER TO postgres;

--
-- TOC entry 5002 (class 0 OID 16389)
-- Dependencies: 219
-- Data for Name: bank_full; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bank_full (age, job, marital, education, "default", balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome, y) FROM stdin;
58	management	married	tertiary	no	2143	yes	no	unknown	5	may	261	1	-1	0	unknown	no
\.


-- Completed on 2025-10-27 18:32:42

--
-- PostgreSQL database dump complete
--

\unrestrict RyftbrgZzJU93OFUgAKUCNoWaIlNNUg2k30UN1AHeFoSFAaiKjJjfmCg88J4rDH

