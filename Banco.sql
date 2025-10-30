--
-- PostgreSQL database dump
--

\restrict 85AJ9KV6iVk2lQ9Y4gJga6EnLKo9XkSXhDodS53kqKtAl8MQByNFqmVRVLj9Xrx

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-30 03:41:42

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

--
-- TOC entry 6 (class 2615 OID 16393)
-- Name: Resultados; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "Resultados";


ALTER SCHEMA "Resultados" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16404)
-- Name: metrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metrics (
    id integer NOT NULL,
    accuracy double precision,
    "precision" double precision,
    recall double precision,
    f1_score double precision,
    auc_roc double precision,
    ap_pr_curve double precision,
    tn integer,
    fp integer,
    fn integer,
    tp integer
);


ALTER TABLE public.metrics OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16403)
-- Name: metrics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.metrics_id_seq OWNER TO postgres;

--
-- TOC entry 5014 (class 0 OID 0)
-- Dependencies: 220
-- Name: metrics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metrics_id_seq OWNED BY public.metrics.id;


--
-- TOC entry 4857 (class 2604 OID 16407)
-- Name: metrics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics ALTER COLUMN id SET DEFAULT nextval('public.metrics_id_seq'::regclass);


--
-- TOC entry 5008 (class 0 OID 16404)
-- Dependencies: 221
-- Data for Name: metrics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.metrics (id, accuracy, "precision", recall, f1_score, auc_roc, ap_pr_curve, tn, fp, fn, tp) FROM stdin;
1	0.57	0.5797	0.57	0.5649	\N	\N	\N	\N	\N	\N
2	0.5	0.5282	0.5	0.5042	\N	\N	\N	\N	\N	\N
3	0.56	0.5609	0.56	0.5584	\N	\N	\N	\N	\N	\N
4	0.57	0.5681	0.57	0.5676	\N	\N	\N	\N	\N	\N
5	0.53	0.529	0.53	0.529	\N	\N	\N	\N	\N	\N
6	0.48	0.4918	0.48	0.481	\N	\N	\N	\N	\N	\N
7	0.47	0.471	0.47	0.4666	\N	\N	\N	\N	\N	\N
8	0.45	0.4484	0.45	0.4481	\N	\N	\N	\N	\N	\N
9	0.41	0.4101	0.41	0.403	\N	\N	\N	\N	\N	\N
10	0.49	0.4964	0.49	0.4872	\N	\N	\N	\N	\N	\N
11	0.57	0.5797	0.57	0.5649	\N	\N	\N	\N	\N	\N
12	0.5	0.5282	0.5	0.5042	\N	\N	\N	\N	\N	\N
13	0.56	0.5609	0.56	0.5584	\N	\N	\N	\N	\N	\N
14	0.57	0.5681	0.57	0.5676	\N	\N	\N	\N	\N	\N
15	0.53	0.529	0.53	0.529	\N	\N	\N	\N	\N	\N
16	0.48	0.4918	0.48	0.481	\N	\N	\N	\N	\N	\N
17	0.47	0.471	0.47	0.4666	\N	\N	\N	\N	\N	\N
18	0.45	0.4484	0.45	0.4481	\N	\N	\N	\N	\N	\N
19	0.41	0.4101	0.41	0.403	\N	\N	\N	\N	\N	\N
20	0.49	0.4964	0.49	0.4872	\N	\N	\N	\N	\N	\N
\.


--
-- TOC entry 5015 (class 0 OID 0)
-- Dependencies: 220
-- Name: metrics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.metrics_id_seq', 20, true);


--
-- TOC entry 4859 (class 2606 OID 16410)
-- Name: metrics metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT metrics_pkey PRIMARY KEY (id);


-- Completed on 2025-10-30 03:41:42

--
-- PostgreSQL database dump complete
--

\unrestrict 85AJ9KV6iVk2lQ9Y4gJga6EnLKo9XkSXhDodS53kqKtAl8MQByNFqmVRVLj9Xrx

