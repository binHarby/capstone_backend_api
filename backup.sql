--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: res_prop; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.res_prop (
    res_id integer NOT NULL,
    comp_1 character varying,
    comp_2 character varying,
    comp_3 character varying,
    comp_4 character varying,
    comp_5 character varying,
    comp_6 character varying,
    comp_7 character varying,
    comp_8 character varying,
    comp_9 character varying,
    comp_10 character varying
);


--
-- Name: res_rules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.res_rules (
    id integer NOT NULL,
    name character varying NOT NULL,
    no_rules integer NOT NULL,
    traces boolean NOT NULL,
    minerals boolean NOT NULL,
    vitamins boolean NOT NULL,
    macros boolean NOT NULL,
    description character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: res_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.res_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: res_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.res_rules_id_seq OWNED BY public.res_rules.id;


--
-- Name: user_activities_general; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_activities_general (
    user_id integer NOT NULL,
    name character varying NOT NULL,
    duration character varying NOT NULL,
    cals_burned integer DEFAULT 0 NOT NULL,
    created_at timestamp without time zone NOT NULL,
    activity_id integer NOT NULL,
    state_id integer NOT NULL
);


--
-- Name: user_activities_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_activities_activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_activities_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_activities_activity_id_seq OWNED BY public.user_activities_general.activity_id;


--
-- Name: user_food_general; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_food_general (
    user_id integer NOT NULL,
    food_name character varying NOT NULL,
    cals_per_serv double precision NOT NULL,
    servings double precision DEFAULT 1 NOT NULL,
    total_cals integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    food_entry_id integer NOT NULL,
    state_id integer NOT NULL,
    ingredients character varying,
    brand_name character varying,
    serving_size_unit character varying,
    servings_taken double precision DEFAULT 1 NOT NULL
);


--
-- Name: user_food_food_entry_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_food_food_entry_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_food_food_entry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_food_food_entry_id_seq OWNED BY public.user_food_general.food_entry_id;


--
-- Name: user_food_macros; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_food_macros (
    food_entry_id integer NOT NULL,
    carb integer,
    sugar integer,
    fructose integer,
    lactose integer,
    protein integer,
    amino integer,
    fat integer,
    unsaturated integer,
    monounsaturated integer,
    polyunsaturated integer,
    saturated integer,
    fiber integer,
    trans integer
);


--
-- Name: user_food_minerals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_food_minerals (
    food_entry_id integer NOT NULL,
    calcium integer,
    phosphorus integer,
    magnesium integer,
    sodium integer,
    potassium integer,
    iron integer,
    zinc integer
);


--
-- Name: user_food_traces; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_food_traces (
    food_entry_id integer NOT NULL,
    boron integer,
    copper integer,
    selenium integer,
    maganese integer,
    fluorine integer,
    chromium integer,
    cobalt integer,
    iodine integer
);


--
-- Name: user_food_vitamins; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_food_vitamins (
    food_entry_id integer NOT NULL,
    b integer,
    b_1 integer,
    b_2 integer,
    b_3 integer,
    b_8 integer,
    b_5 integer,
    b_6 integer,
    b_7 integer,
    b_12 integer,
    choline integer,
    a integer,
    c integer,
    d integer,
    d_2 integer,
    d_3 integer,
    k_1 integer,
    k_2 integer,
    k_3 integer,
    k integer,
    e integer
);


--
-- Name: user_goal_general; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_goal_general (
    user_id integer NOT NULL,
    tdee integer NOT NULL,
    bmi integer NOT NULL,
    cal_goal integer,
    cal_diff integer,
    weight integer NOT NULL,
    activity_lvl integer NOT NULL,
    control_lvl character varying NOT NULL
);


--
-- Name: user_goal_macros; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_goal_macros (
    user_id integer NOT NULL,
    carb integer,
    sugar integer,
    fructose integer,
    lactose integer,
    protein integer,
    amino integer,
    fat integer,
    unsaturated integer,
    monounsaturated integer,
    polyunsaturated integer,
    saturated integer,
    fiber integer,
    trans integer
);


--
-- Name: user_goal_minerals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_goal_minerals (
    user_id integer NOT NULL,
    calcium integer,
    phosphorus integer,
    magnesium integer,
    sodium integer,
    potassium integer,
    iron integer,
    zinc integer
);


--
-- Name: user_goal_traces; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_goal_traces (
    user_id integer NOT NULL,
    boron integer,
    copper integer,
    selenium integer,
    maganese integer,
    fluorine integer,
    chromium integer,
    cobalt integer,
    iodine integer
);


--
-- Name: user_goal_vitamins; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_goal_vitamins (
    user_id integer NOT NULL,
    b integer,
    b_1 integer,
    b_2 integer,
    b_3 integer,
    b_8 integer,
    b_5 integer,
    b_6 integer,
    b_7 integer,
    b_12 integer,
    choline integer,
    a integer,
    c integer,
    d integer,
    d_2 integer,
    d_3 integer,
    k_1 integer,
    k_2 integer,
    k_3 integer,
    k integer,
    e integer
);


--
-- Name: user_meds_delta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_meds_delta (
    doses_taken integer NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    med_id integer NOT NULL,
    state_id integer NOT NULL
);


--
-- Name: user_meds_general; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_meds_general (
    user_id integer NOT NULL,
    med_name character varying NOT NULL,
    res_name character varying NOT NULL,
    res_id integer NOT NULL,
    daily_doses integer NOT NULL,
    dose_quant integer NOT NULL,
    dose_quant_type character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    med_id integer NOT NULL
);


--
-- Name: user_meds_med_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_meds_med_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_meds_med_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_meds_med_id_seq OWNED BY public.user_meds_general.med_id;


--
-- Name: user_res; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_res (
    user_id integer NOT NULL,
    res_id integer NOT NULL,
    rule integer NOT NULL,
    user_res_id integer NOT NULL
);


--
-- Name: user_res_user_res_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_res_user_res_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_res_user_res_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_res_user_res_id_seq OWNED BY public.user_res.user_res_id;


--
-- Name: user_state_general; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_state_general (
    state_id integer NOT NULL,
    user_id integer NOT NULL,
    day date NOT NULL,
    total_cals integer DEFAULT 0 NOT NULL
);


--
-- Name: user_state_macros; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_state_macros (
    carb integer,
    sugar integer,
    fructose integer,
    lactose integer,
    protein integer,
    amino integer,
    fat integer,
    unsaturated integer,
    monounsaturated integer,
    polyunsaturated integer,
    saturated integer,
    state_id integer NOT NULL,
    fiber integer,
    trans integer
);


--
-- Name: user_state_minerals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_state_minerals (
    state_id integer NOT NULL,
    calcium integer,
    phosphorus integer,
    magnesium integer,
    sodium integer,
    potassium integer,
    iron integer,
    zinc integer
);


--
-- Name: user_state_state_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_state_state_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_state_state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_state_state_id_seq OWNED BY public.user_state_general.state_id;


--
-- Name: user_state_traces; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_state_traces (
    boron integer,
    copper integer,
    selenium integer,
    maganese integer,
    fluorine integer,
    chromium integer,
    cobalt integer,
    iodine integer,
    state_id integer NOT NULL
);


--
-- Name: user_state_vitamins; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_state_vitamins (
    state_id integer NOT NULL,
    b integer,
    b_1 integer,
    b_2 integer,
    b_3 integer,
    b_8 integer,
    b_5 integer,
    b_6 integer,
    b_7 integer,
    b_12 integer,
    choline integer,
    a integer,
    c integer,
    d integer,
    d_2 integer,
    d_3 integer,
    k_1 integer,
    k_2 integer,
    k_3 integer,
    k integer,
    e integer
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    gender character varying NOT NULL,
    email character varying NOT NULL,
    birthday date NOT NULL,
    password character varying NOT NULL,
    bloodtype character varying NOT NULL,
    height double precision NOT NULL,
    age integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: res_rules id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.res_rules ALTER COLUMN id SET DEFAULT nextval('public.res_rules_id_seq'::regclass);


--
-- Name: user_activities_general activity_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activities_general ALTER COLUMN activity_id SET DEFAULT nextval('public.user_activities_activity_id_seq'::regclass);


--
-- Name: user_food_general food_entry_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_general ALTER COLUMN food_entry_id SET DEFAULT nextval('public.user_food_food_entry_id_seq'::regclass);


--
-- Name: user_meds_general med_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_meds_general ALTER COLUMN med_id SET DEFAULT nextval('public.user_meds_med_id_seq'::regclass);


--
-- Name: user_res user_res_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_res ALTER COLUMN user_res_id SET DEFAULT nextval('public.user_res_user_res_id_seq'::regclass);


--
-- Name: user_state_general state_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_general ALTER COLUMN state_id SET DEFAULT nextval('public.user_state_state_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: res_prop; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.res_prop (res_id, comp_1, comp_2, comp_3, comp_4, comp_5, comp_6, comp_7, comp_8, comp_9, comp_10) FROM stdin;
5	sugar	carbs	\N	\N	\N	\N	\N	\N	\N	\N
6	iron	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: res_rules; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.res_rules (id, name, no_rules, traces, minerals, vitamins, macros, description, created_at, updated_at) FROM stdin;
5	diabetes	3	f	f	f	t	diabetes tends to have to types, type 1 and type 2 	2022-05-06 11:05:45.157259	2022-05-06 22:13:47.728728
6	iron deficiency	3	f	t	f	f	iron deficiency 	2022-05-06 19:15:41.851726	2022-05-06 19:15:41.851729
\.


--
-- Data for Name: user_activities_general; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_activities_general (user_id, name, duration, cals_burned, created_at, activity_id, state_id) FROM stdin;
6	running		0	2022-05-16 16:32:34.462089	3	5
6	running		0	2022-07-06 23:07:13.101542	4	7
6	joggg	566	0	2022-07-06 23:07:13.101542	5	7
6	walking	56	0	2022-07-06 23:07:13.101542	6	7
6	walin	56	0	2022-07-27 08:19:47.957513	7	10
6	walking	56	0	2022-07-27 14:29:25.052142	40	10
6	walking	56	0	2022-07-27 14:29:25.052142	41	10
\.


--
-- Data for Name: user_food_general; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_food_general (user_id, food_name, cals_per_serv, servings, total_cals, created_at, food_entry_id, state_id, ingredients, brand_name, serving_size_unit, servings_taken) FROM stdin;
6	ham	0	1	0	2022-05-14 11:56:46.795744	10	4	\N	\N	\N	3
16	Combination Fried Rice	0	1	241	2022-08-25 08:20:54.65186	50	54	\N	\N	\N	1
16	Scrambled Egg	0	1	90	2022-08-25 08:20:54.65186	51	54	\N	\N	\N	1
16	Scrambled Egg	0	1	90	2022-08-25 08:20:54.65186	52	54	\N	\N	\N	1
6	milk	0	1	500	2022-05-14 01:27:03.643132	8	3	\N	\N	\N	5
6	Wrap	0	1	2280	2022-07-14 17:02:01.724741	11	8	\N	\N	\N	1
6	rice	0	1	205	2022-07-14 17:09:48.500078	12	8	\N	\N	cup	1
6	Energy Drink	0	1	10	2022-07-14 17:09:48.500078	13	8	carbonated water, sucrose, glucose, citric acid, taurine, sodium bicarbonate, magnesium carbonate, caffeine, niacinamide, calcium pantothenate, pyridoxine hcl, vitamin b12, natural and artificial flavors, colors.	Red Bull	can	1
6	Energy Drink	0	1	10	2022-07-14 20:04:13.594822	14	8	carbonated water, sucrose, glucose, citric acid, taurine, sodium bicarbonate, magnesium carbonate, caffeine, niacinamide, calcium pantothenate, pyridoxine hcl, vitamin b12, natural and artificial flavors, colors.	Red Bull	can	1
6	Energy Drink	0	1	10	2022-07-14 20:04:13.594822	15	8	carbonated water, sucrose, glucose, citric acid, taurine, sodium bicarbonate, magnesium carbonate, caffeine, niacinamide, calcium pantothenate, pyridoxine hcl, vitamin b12, natural and artificial flavors, colors.	Red Bull	can	1
6	Energy Drink	0	1	10	2022-07-14 20:09:30.732413	16	8	carbonated water, sucrose, glucose, citric acid, taurine, sodium bicarbonate, magnesium carbonate, caffeine, niacinamide, calcium pantothenate, pyridoxine hcl, vitamin b12, natural and artificial flavors, colors.	Red Bull	can	1
6	Energy Drink	0	1	10	2022-07-14 20:11:12.058871	17	8	carbonated water, sucrose, glucose, citric acid, taurine, sodium bicarbonate, magnesium carbonate, caffeine, niacinamide, calcium pantothenate, pyridoxine hcl, vitamin b12, natural and artificial flavors, colors.	Red Bull	can	1
6	Energy Drink	0	1	10	2022-07-14 20:15:43.043556	18	8	carbonated water, sucrose, glucose, citric acid, taurine, sodium bicarbonate, magnesium carbonate, caffeine, niacinamide, calcium pantothenate, pyridoxine hcl, vitamin b12, natural and artificial flavors, colors.	Red Bull	can	1
6	Energy Drink	0	1	10	2022-07-15 12:02:11.519669	19	9	carbonated water, sucrose, glucose, citric acid, taurine, sodium bicarbonate, magnesium carbonate, caffeine, niacinamide, calcium pantothenate, pyridoxine hcl, vitamin b12, natural and artificial flavors, colors.	Red Bull	can	1
11	Wheat Bread	0	1	77	2022-08-23 12:25:04.777512	20	43	\N	\N	\N	1
11	Regular 330 Ml	0	1	139	2022-08-23 12:25:04.777512	21	43	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 08:17:01.712814	22	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 08:17:01.712814	23	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 08:17:01.712814	24	45	\N	Coca-Cola	can	1
11	rice	0	1	205	2022-08-24 08:17:01.712814	25	45	\N	\N	cup	1
11	rice	0	1	205	2022-08-24 08:17:01.712814	26	45	\N	\N	cup	1
11	rice	0	1	205	2022-08-24 08:17:01.712814	27	45	\N	\N	cup	1
11	Regular 330 Ml	0	1	139	2022-08-24 09:57:02.409664	28	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 09:57:02.409664	29	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 09:57:02.409664	30	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 09:57:02.409664	31	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 10:33:20.175806	32	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 10:33:20.175806	33	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 10:33:20.175806	34	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 10:33:20.175806	35	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	139	2022-08-24 10:33:20.175806	36	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	278	2022-08-25 00:49:02.37897	37	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	834	2022-08-25 00:49:02.37897	38	45	\N	Coca-Cola	can	1
11	Regular 330 Ml	0	1	278	2022-08-25 00:49:02.37897	39	45	\N	Coca-Cola	can	1
11	rice	0	1	410	2022-08-25 00:49:02.37897	40	45	\N	\N	cup	1
11	Wheat Bread	0	1	154	2022-08-25 00:49:02.37897	41	45	\N	\N	\N	1
16	Scrambled Egg	0	1	90	2022-08-25 08:20:54.65186	53	54	\N	\N	\N	1
16	Scrambled Egg	0	1	90	2022-08-25 08:20:54.65186	54	54	\N	\N	\N	1
16	Scrambled Egg	0	1	90	2022-08-25 08:20:54.65186	55	54	\N	\N	\N	1
16	Scrambled Egg	0	1	90	2022-08-25 08:20:54.65186	56	54	\N	\N	\N	1
16	Scrambled Egg	0	1	90	2022-08-25 08:20:54.65186	57	54	\N	\N	\N	1
16	Scrambled Egg	0	1	900	2022-08-25 08:20:54.65186	58	54	\N	\N	\N	1
16	Scrambled Egg	0	1	9000	2022-08-25 08:20:54.65186	59	54	\N	\N	\N	1
16	Scrambled Egg	0	1	90000	2022-08-25 08:20:54.65186	60	54	\N	\N	\N	1
16	Scrambled Egg	0	1	900000	2022-08-25 08:20:54.65186	61	54	\N	\N	\N	1
16	Scrambled Egg	0	1	9000000	2022-08-25 08:20:54.65186	62	54	\N	\N	\N	1
16	Scrambled Egg	0	1	90000000	2022-08-25 08:20:54.65186	63	54	\N	\N	\N	1
16	Scrambled Egg	0	1	900000000	2022-08-25 08:20:54.65186	64	54	\N	\N	\N	1
\.


--
-- Data for Name: user_food_macros; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_food_macros (food_entry_id, carb, sugar, fructose, lactose, protein, amino, fat, unsaturated, monounsaturated, polyunsaturated, saturated, fiber, trans) FROM stdin;
10	15	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
8	50	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
11	233	14	\N	\N	124	\N	92	\N	34	12	38	\N	\N
12	44	\N	\N	\N	4	\N	\N	\N	\N	\N	\N	\N	\N
13	3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
14	3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
15	3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
16	3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
17	3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
18	3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
19	3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
20	14	2	\N	\N	3	\N	1	\N	\N	\N	\N	\N	\N
21	35	35	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
22	35	35	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
23	35	35	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
24	35	35	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
25	44	\N	\N	\N	4	\N	\N	\N	\N	\N	\N	\N	\N
26	44	\N	\N	\N	4	\N	\N	\N	\N	\N	\N	\N	\N
27	44	\N	\N	\N	4	\N	\N	\N	\N	\N	\N	\N	\N
28	35	35	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
29	35	35	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
30	105	105	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
31	315	315	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
32	945	945	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
33	2835	2835	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
34	8505	8505	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
35	25515	25515	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
36	25515	25515	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
37	70	70	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
38	210	210	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
39	70	70	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
40	88	\N	\N	\N	8	\N	\N	\N	\N	\N	\N	\N	\N
41	28	4	\N	\N	6	\N	2	\N	\N	\N	\N	\N	\N
50	32	1	\N	\N	8	\N	9	\N	3	5	2	\N	\N
51	1	1	\N	\N	6	\N	7	\N	3	1	2	\N	\N
52	1	1	\N	\N	6	\N	7	\N	3	1	2	\N	\N
53	1	1	\N	\N	6	\N	7	\N	3	1	2	\N	\N
54	1	1	\N	\N	6	\N	7	\N	3	1	2	\N	\N
55	1	1	\N	\N	6	\N	7	\N	3	1	2	\N	\N
56	1	1	\N	\N	6	\N	7	\N	3	1	2	\N	\N
57	1	1	\N	\N	6	\N	7	\N	3	1	2	\N	\N
58	10	10	\N	\N	60	\N	70	\N	30	10	20	\N	\N
59	100	100	\N	\N	600	\N	700	\N	300	100	200	\N	\N
60	1000	1000	\N	\N	6000	\N	7000	\N	3000	1000	2000	\N	\N
61	10000	10000	\N	\N	60000	\N	70000	\N	30000	10000	20000	\N	\N
62	100000	100000	\N	\N	600000	\N	700000	\N	300000	100000	200000	\N	\N
63	1000000	1000000	\N	\N	6000000	\N	7000000	\N	3000000	1000000	2000000	\N	\N
64	10000000	10000000	\N	\N	60000000	\N	70000000	\N	30000000	10000000	20000000	\N	\N
\.


--
-- Data for Name: user_food_minerals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_food_minerals (food_entry_id, calcium, phosphorus, magnesium, sodium, potassium, iron, zinc) FROM stdin;
\.


--
-- Data for Name: user_food_traces; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_food_traces (food_entry_id, boron, copper, selenium, maganese, fluorine, chromium, cobalt, iodine) FROM stdin;
\.


--
-- Data for Name: user_food_vitamins; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_food_vitamins (food_entry_id, b, b_1, b_2, b_3, b_8, b_5, b_6, b_7, b_12, choline, a, c, d, d_2, d_3, k_1, k_2, k_3, k, e) FROM stdin;
10	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	30	\N	\N	\N	\N	\N	\N	\N	\N
8	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	50	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: user_goal_general; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_goal_general (user_id, tdee, bmi, cal_goal, cal_diff, weight, activity_lvl, control_lvl) FROM stdin;
2	2643	24	2643	0	80	1	tight
1	2574	27	2574	0	80	1	tight
6	3020	30	3020	0	100	1	normal
9	2775	39	2775	0	120	1	normal
10	2394	30	2394	0	100	1	normal
11	2425	27	2425	0	100	1	normal
12	3252	30	3252	0	95	3	normal
13	2492	34	2492	0	100	1	normal
14	2762	30	2762	0	95	2	normal
15	2762	30	2762	0	95	2	normal
16	2759	30	2759	0	95	2	normal
\.


--
-- Data for Name: user_goal_macros; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_goal_macros (user_id, carb, sugar, fructose, lactose, protein, amino, fat, unsaturated, monounsaturated, polyunsaturated, saturated, fiber, trans) FROM stdin;
2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
1	200	50	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
6	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
11	200	25	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
12	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
13	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
14	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
15	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
16	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: user_goal_minerals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_goal_minerals (user_id, calcium, phosphorus, magnesium, sodium, potassium, iron, zinc) FROM stdin;
2	\N	\N	\N	\N	\N	\N	\N
1	\N	\N	\N	\N	\N	15	\N
6	\N	\N	\N	\N	\N	\N	\N
11	\N	\N	\N	\N	\N	\N	\N
12	\N	\N	\N	\N	\N	\N	\N
13	\N	\N	\N	\N	\N	\N	\N
14	\N	\N	\N	\N	\N	\N	\N
15	\N	\N	\N	\N	\N	\N	\N
16	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: user_goal_traces; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_goal_traces (user_id, boron, copper, selenium, maganese, fluorine, chromium, cobalt, iodine) FROM stdin;
2	\N	\N	\N	\N	\N	\N	\N	\N
1	\N	\N	\N	\N	\N	\N	\N	\N
6	\N	\N	\N	\N	\N	\N	\N	\N
11	\N	\N	\N	\N	\N	\N	\N	\N
12	\N	\N	\N	\N	\N	\N	\N	\N
13	\N	\N	\N	\N	\N	\N	\N	\N
14	\N	\N	\N	\N	\N	\N	\N	\N
15	\N	\N	\N	\N	\N	\N	\N	\N
16	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: user_goal_vitamins; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_goal_vitamins (user_id, b, b_1, b_2, b_3, b_8, b_5, b_6, b_7, b_12, choline, a, c, d, d_2, d_3, k_1, k_2, k_3, k, e) FROM stdin;
2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
1	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
6	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
11	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
12	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
13	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
14	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
15	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
16	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: user_meds_delta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_meds_delta (doses_taken, updated_at, med_id, state_id) FROM stdin;
1	2022-05-17 23:09:45.848977	4	6
\.


--
-- Data for Name: user_meds_general; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_meds_general (user_id, med_name, res_name, res_id, daily_doses, dose_quant, dose_quant_type, created_at, med_id) FROM stdin;
6	pee	diabetes	5	1	5	mg	2022-05-17 10:05:34.85025	4
6	gg	diabetes	5	1	5	mg	2022-07-06 22:03:19.721129	5
6	gee	diabetes	5	1	5	pill	2022-07-06 23:07:13.103231	6
6	med 1	diabetes	5	1	5	pill	2022-07-06 23:07:13.103231	7
6	sss	diabetes	5	1	3	pill	2022-07-27 08:19:47.959183	8
6	dfdf	diabetes	5	1	3	pill	2022-07-27 14:29:25.053842	9
6	Med1	diabetes	5	1	5	pill	2022-07-27 14:29:25.053842	10
11	enwlkj	diabetes	5	1	3	pill	2022-08-23 11:50:44.727454	11
11	enwl	diabetes	5	1	3	pill	2022-08-23 11:50:44.727454	12
11	ddd	diabetes	5	1	3	pill	2022-08-23 12:14:26.155837	13
11	halmo	diabetes	5	1	3	pill	2022-08-25 00:49:02.393062	14
11	Deferoxamine	diabetes	5	1	3	1	2022-08-25 08:20:54.657918	15
11	Deferasirox	diabetes	5	1	3	pill	2022-08-25 15:04:27.694359	16
\.


--
-- Data for Name: user_res; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_res (user_id, res_id, rule, user_res_id) FROM stdin;
1	6	1	7
1	5	1	8
11	5	1	9
\.


--
-- Data for Name: user_state_general; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_state_general (state_id, user_id, day, total_cals) FROM stdin;
1	1	2022-05-09	300
54	16	2022-08-25	1000000771
56	15	2022-08-25	0
2	2	2022-05-10	600
45	11	2022-08-24	4237
60	11	2022-08-25	0
3	6	2022-05-13	0
4	6	2022-05-14	0
44	6	2022-08-24	0
5	6	2022-05-16	0
6	6	2022-05-17	0
7	6	2022-07-06	0
8	6	2022-07-14	10
9	6	2022-07-15	10
10	6	2022-07-27	0
43	11	2022-08-23	216
\.


--
-- Data for Name: user_state_macros; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_state_macros (carb, sugar, fructose, lactose, protein, amino, fat, unsaturated, monounsaturated, polyunsaturated, saturated, state_id, fiber, trans) FROM stdin;
\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	56	\N	\N
\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	60	\N	\N
3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2	\N	\N
295	14	\N	\N	128	\N	92	\N	34	12	38	8	\N	\N
3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	9	\N	\N
49	37	\N	\N	3	\N	1	\N	\N	\N	\N	43	\N	\N
64508	64264	\N	\N	26	\N	2	\N	\N	\N	\N	45	\N	\N
\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	44	\N	\N
11111149	11111118	\N	\N	66666710	\N	77777828	\N	33333354	11111122	22222236	54	\N	\N
\.


--
-- Data for Name: user_state_minerals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_state_minerals (state_id, calcium, phosphorus, magnesium, sodium, potassium, iron, zinc) FROM stdin;
45	\N	\N	\N	\N	\N	\N	\N
44	\N	\N	\N	\N	\N	\N	\N
54	\N	\N	\N	\N	\N	\N	\N
56	\N	\N	\N	\N	\N	\N	\N
60	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: user_state_traces; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_state_traces (boron, copper, selenium, maganese, fluorine, chromium, cobalt, iodine, state_id) FROM stdin;
\N	\N	\N	\N	\N	\N	\N	\N	45
\N	\N	\N	\N	\N	\N	\N	\N	44
\N	\N	\N	\N	\N	\N	\N	\N	54
\N	\N	\N	\N	\N	\N	\N	\N	56
\N	\N	\N	\N	\N	\N	\N	\N	60
\.


--
-- Data for Name: user_state_vitamins; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.user_state_vitamins (state_id, b, b_1, b_2, b_3, b_8, b_5, b_6, b_7, b_12, choline, a, c, d, d_2, d_3, k_1, k_2, k_3, k, e) FROM stdin;
2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	99	\N	\N	\N	\N	\N	\N	\N	\N
45	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
44	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
54	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
56	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
60	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, gender, email, birthday, password, bloodtype, height, age, created_at, updated_at, first_name, last_name) FROM stdin;
1	male	hankerman@gmail.com	1999-11-28	$2b$12$wst8nDlE8wI6c0la7TnpfuWwk7Zhz82CuNEVm61JiEzIYSucplmG2	O+	1.72	22	2022-04-25 05:03:41.15989	2022-04-25 05:03:41.15989	Ahmed	Al otabi
3	male	newuser@gmail.com	1999-11-28	$2b$12$fCrwHxZvzJ4fPHKX2c4lueI0iDtaMIFpYEbpTDjDh9Kusli9WAI3.	O+	1.72	22	2022-05-04 22:24:34.383727	2022-05-04 22:24:34.383727	Ahmed	Al otabi
2	male	lunerman@gmail.com	1999-11-28	$2b$12$KUn6CoDqnlcDWP6Gf8R0UejrHyQQoc4SuFCfNcA.FYUamb/ARey2K	O-	1.82	22	2022-05-04 22:15:46.759856	2022-05-05 15:44:16.592383	Ahmed	Al otabi
6	male	newnewuser@gmail.com	1999-11-28	$2b$12$NUnqTGxvxpUMOYAy4sg75eglVnVKVj3nTWv2qPLTxy.V9avoDBvEm	O-	1.82	22	2022-05-08 10:01:10.666604	2022-05-08 06:01:10.668656	Ahmed	Al otabi
7	Male	naim@naim.nom	1999-08-11	$2b$12$.tZT9PLZzXjt55BIaFftr.6VCCC5rGaXIB4E2Tj4sH38kcmGwqPS6	A+	1.22	23	2022-08-21 11:44:33.675758	2022-08-21 11:44:33.675762	naim	naim
8	Male	moonmoon@moon.co	1999-11-11	$2b$12$GvNigqOrs1g4TyYP0.NKDOs3d..Qc1E.jy21Cp4OmHyYiHCcFQzka	O+	1.7	22	2022-08-21 11:44:33.675758	2022-08-21 11:44:33.675762	aaa	aaa
9	Male	abdulla@abdulla.ae	1999-09-09	$2b$12$lTFpdM75ipglN6VmDMwgzOITV5JInAHFii0B6Y0C7lRjbTLBjQWBu	A+	1.75	22	2022-08-21 11:44:33.675758	2022-08-21 11:44:33.675762	Abdulla	Alameri
10	Male	man@down.co	1980-06-06	$2b$12$faaHD8zItqkrm3IyYY3kJ.1rQ7xxAGRELdr3ZPSw7HiXEeGEvwmSC	A+	1.8	42	2022-08-21 11:44:33.675758	2022-08-21 11:44:33.675762	land	lord
11	Male	tall@man.co	1980-10-11	$2b$12$9jhC3MWwwITMF.b9unGulus6xJPg60vID71ptFwSVC05ILs8e2nRG	A+	1.9	41	2022-08-21 11:44:33.675758	2022-08-21 11:44:33.675762	hand	man
12	Male	mahmoud.alolabi@outlook.com	2022-08-06	$2b$12$HJqFlwGxfSiAq3Ung9Y7sOlCk5GX45vmb.Qw7l2Is9/jsLcTsDvoG	A+	1.77	0	2022-08-25 08:20:54.621631	2022-08-25 08:20:54.621637	mahmoud	alolabi
13	Male	gg@gg.cc	1999-07-28	$2b$12$Pjexq0CumybPaDSzGf17weP6G3dwxyZ53QaPlNa1f3wIZnmpSjvCy	O-	1.7	23	2022-08-25 08:20:54.621631	2022-08-25 08:20:54.621637	agg	gg
14	Male	king-mahmoud-2000@hotmail.com	2000-06-06	$2b$12$MO9cXgbSXr1l2y0r/gazz.1N.GPWa7piofJy.ZKl/jpcbkI80xsFe	A+	1.77	22	2022-08-25 08:20:54.621631	2022-08-25 08:20:54.621637	mahmoud	alolabi
15	Male	mahmoud@gmail.com	2000-06-06	$2b$12$PE/KhQKeqXv/Z5qzq7O8d.FsDF/zvpPSJDUNmITzZdGsPapXe98mq	A+	1.77	22	2022-08-25 08:20:54.621631	2022-08-25 08:20:54.621637	mahmoud	alolabi
16	Male	mahmoud@outlook.com	2000-06-06	$2b$12$OkqMxGs3glTxvG8AehJJSOItbbqr8IOQpZy3LzY/BiWODSc/0xkDe	A+	1.76	22	2022-08-25 08:20:54.621631	2022-08-25 08:20:54.621637	mahmoud	alolabi
\.


--
-- Name: res_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.res_rules_id_seq', 6, true);


--
-- Name: user_activities_activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_activities_activity_id_seq', 41, true);


--
-- Name: user_food_food_entry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_food_food_entry_id_seq', 67, true);


--
-- Name: user_meds_med_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_meds_med_id_seq', 16, true);


--
-- Name: user_res_user_res_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_res_user_res_id_seq', 9, true);


--
-- Name: user_state_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.user_state_state_id_seq', 60, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 16, true);


--
-- Name: res_prop res_prop_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.res_prop
    ADD CONSTRAINT res_prop_pkey PRIMARY KEY (res_id);


--
-- Name: res_rules res_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.res_rules
    ADD CONSTRAINT res_rules_pkey PRIMARY KEY (id);


--
-- Name: user_activities_general user_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activities_general
    ADD CONSTRAINT user_activities_pkey PRIMARY KEY (activity_id);


--
-- Name: user_food_macros user_food_macros_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_macros
    ADD CONSTRAINT user_food_macros_pkey PRIMARY KEY (food_entry_id);


--
-- Name: user_food_minerals user_food_minerals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_minerals
    ADD CONSTRAINT user_food_minerals_pkey PRIMARY KEY (food_entry_id);


--
-- Name: user_food_general user_food_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_general
    ADD CONSTRAINT user_food_pkey PRIMARY KEY (food_entry_id);


--
-- Name: user_food_traces user_food_traces_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_traces
    ADD CONSTRAINT user_food_traces_pkey PRIMARY KEY (food_entry_id);


--
-- Name: user_food_vitamins user_food_vitamins_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_vitamins
    ADD CONSTRAINT user_food_vitamins_pkey PRIMARY KEY (food_entry_id);


--
-- Name: user_goal_general user_goal_general_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_general
    ADD CONSTRAINT user_goal_general_pkey PRIMARY KEY (user_id);


--
-- Name: user_goal_macros user_goal_macros_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_macros
    ADD CONSTRAINT user_goal_macros_pkey PRIMARY KEY (user_id);


--
-- Name: user_goal_minerals user_goal_minerals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_minerals
    ADD CONSTRAINT user_goal_minerals_pkey PRIMARY KEY (user_id);


--
-- Name: user_goal_traces user_goal_traces_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_traces
    ADD CONSTRAINT user_goal_traces_pkey PRIMARY KEY (user_id);


--
-- Name: user_goal_vitamins user_goal_vitamins_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_vitamins
    ADD CONSTRAINT user_goal_vitamins_pkey PRIMARY KEY (user_id);


--
-- Name: user_meds_delta user_meds_delta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_meds_delta
    ADD CONSTRAINT user_meds_delta_pkey PRIMARY KEY (state_id);


--
-- Name: user_meds_general user_meds_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_meds_general
    ADD CONSTRAINT user_meds_pkey PRIMARY KEY (med_id);


--
-- Name: user_res user_res_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_res
    ADD CONSTRAINT user_res_pkey PRIMARY KEY (user_res_id);


--
-- Name: user_res user_res_user_id_res_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_res
    ADD CONSTRAINT user_res_user_id_res_id_key UNIQUE (user_id, res_id);


--
-- Name: user_state_general user_state_general_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_general
    ADD CONSTRAINT user_state_general_pkey PRIMARY KEY (state_id);


--
-- Name: user_state_macros user_state_macros_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_macros
    ADD CONSTRAINT user_state_macros_pkey PRIMARY KEY (state_id);


--
-- Name: user_state_minerals user_state_minerals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_minerals
    ADD CONSTRAINT user_state_minerals_pkey PRIMARY KEY (state_id);


--
-- Name: user_state_traces user_state_traces_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_traces
    ADD CONSTRAINT user_state_traces_pkey PRIMARY KEY (state_id);


--
-- Name: user_state_vitamins user_state_vitamins_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_vitamins
    ADD CONSTRAINT user_state_vitamins_pkey PRIMARY KEY (state_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: res_prop res_prop_res_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.res_prop
    ADD CONSTRAINT res_prop_res_id_fkey FOREIGN KEY (res_id) REFERENCES public.res_rules(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_activities_general user_activities_general_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activities_general
    ADD CONSTRAINT user_activities_general_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.user_state_general(state_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_activities_general user_activities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activities_general
    ADD CONSTRAINT user_activities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_food_general user_food_general_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_general
    ADD CONSTRAINT user_food_general_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.user_state_general(state_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_food_macros user_food_macros_food_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_macros
    ADD CONSTRAINT user_food_macros_food_entry_id_fkey FOREIGN KEY (food_entry_id) REFERENCES public.user_food_general(food_entry_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_food_minerals user_food_minerals_food_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_minerals
    ADD CONSTRAINT user_food_minerals_food_entry_id_fkey FOREIGN KEY (food_entry_id) REFERENCES public.user_food_general(food_entry_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_food_traces user_food_traces_food_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_traces
    ADD CONSTRAINT user_food_traces_food_entry_id_fkey FOREIGN KEY (food_entry_id) REFERENCES public.user_food_general(food_entry_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_food_general user_food_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_general
    ADD CONSTRAINT user_food_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_food_vitamins user_food_vitamins_food_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_food_vitamins
    ADD CONSTRAINT user_food_vitamins_food_entry_id_fkey FOREIGN KEY (food_entry_id) REFERENCES public.user_food_general(food_entry_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_goal_general user_goal_general_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_general
    ADD CONSTRAINT user_goal_general_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_goal_macros user_goal_macros_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_macros
    ADD CONSTRAINT user_goal_macros_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_goal_minerals user_goal_minerals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_minerals
    ADD CONSTRAINT user_goal_minerals_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_goal_traces user_goal_traces_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_traces
    ADD CONSTRAINT user_goal_traces_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_goal_vitamins user_goal_vitamins_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_goal_vitamins
    ADD CONSTRAINT user_goal_vitamins_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_meds_delta user_meds_delta_med_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_meds_delta
    ADD CONSTRAINT user_meds_delta_med_id_fkey FOREIGN KEY (med_id) REFERENCES public.user_meds_general(med_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_meds_delta user_meds_delta_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_meds_delta
    ADD CONSTRAINT user_meds_delta_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.user_state_general(state_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_meds_general user_meds_res_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_meds_general
    ADD CONSTRAINT user_meds_res_id_fkey FOREIGN KEY (res_id) REFERENCES public.res_rules(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_meds_general user_meds_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_meds_general
    ADD CONSTRAINT user_meds_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_res user_res_res_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_res
    ADD CONSTRAINT user_res_res_id_fkey FOREIGN KEY (res_id) REFERENCES public.res_rules(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_res user_res_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_res
    ADD CONSTRAINT user_res_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_state_macros user_state_macros_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_macros
    ADD CONSTRAINT user_state_macros_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.user_state_general(state_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_state_minerals user_state_minerals_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_minerals
    ADD CONSTRAINT user_state_minerals_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.user_state_general(state_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_state_traces user_state_traces_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_traces
    ADD CONSTRAINT user_state_traces_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.user_state_general(state_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_state_general user_state_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_general
    ADD CONSTRAINT user_state_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_state_vitamins user_state_vitamins_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_state_vitamins
    ADD CONSTRAINT user_state_vitamins_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.user_state_general(state_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

