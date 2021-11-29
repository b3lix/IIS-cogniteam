--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)

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

--
-- Name: stationupdatetype; Type: TYPE; Schema: public; Owner: travelwise
--

CREATE TYPE public.stationupdatetype AS ENUM (
    'insert',
    'update',
    'delete'
);


ALTER TYPE public.stationupdatetype OWNER TO travelwise;

--
-- Name: usertype; Type: TYPE; Schema: public; Owner: travelwise
--

CREATE TYPE public.usertype AS ENUM (
    'passenger',
    'staff',
    'carrier',
    'admin'
);


ALTER TYPE public.usertype OWNER TO travelwise;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: route_stops; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.route_stops (
    id integer NOT NULL,
    arrival integer,
    departure integer,
    route_id integer NOT NULL,
    station_id integer NOT NULL
);


ALTER TABLE public.route_stops OWNER TO travelwise;

--
-- Name: route_stops_id_seq; Type: SEQUENCE; Schema: public; Owner: travelwise
--

CREATE SEQUENCE public.route_stops_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.route_stops_id_seq OWNER TO travelwise;

--
-- Name: route_stops_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: travelwise
--

ALTER SEQUENCE public.route_stops_id_seq OWNED BY public.route_stops.id;


--
-- Name: route_times; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.route_times (
    id integer NOT NULL,
    "time" time without time zone,
    repeat boolean[],
    route_id integer NOT NULL,
    vehicle_id integer NOT NULL
);


ALTER TABLE public.route_times OWNER TO travelwise;

--
-- Name: route_times_id_seq; Type: SEQUENCE; Schema: public; Owner: travelwise
--

CREATE SEQUENCE public.route_times_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.route_times_id_seq OWNER TO travelwise;

--
-- Name: route_times_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: travelwise
--

ALTER SEQUENCE public.route_times_id_seq OWNED BY public.route_times.id;


--
-- Name: routes; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.routes (
    id integer NOT NULL,
    name character varying NOT NULL,
    price double precision,
    carrier_id integer NOT NULL
);


ALTER TABLE public.routes OWNER TO travelwise;

--
-- Name: routes_id_seq; Type: SEQUENCE; Schema: public; Owner: travelwise
--

CREATE SEQUENCE public.routes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.routes_id_seq OWNER TO travelwise;

--
-- Name: routes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: travelwise
--

ALTER SEQUENCE public.routes_id_seq OWNED BY public.routes.id;


--
-- Name: seats; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.seats (
    id integer NOT NULL,
    date date,
    amount integer,
    price double precision,
    paid boolean,
    name character varying,
    created_at timestamp without time zone,
    email character varying,
    user_id integer,
    from_stop_id integer,
    to_stop_id integer,
    time_id integer,
    route_id integer
);


ALTER TABLE public.seats OWNER TO travelwise;

--
-- Name: seats_id_seq; Type: SEQUENCE; Schema: public; Owner: travelwise
--

CREATE SEQUENCE public.seats_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seats_id_seq OWNER TO travelwise;

--
-- Name: seats_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: travelwise
--

ALTER SEQUENCE public.seats_id_seq OWNED BY public.seats.id;


--
-- Name: staff; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.staff (
    user_id integer NOT NULL,
    carrier_id integer NOT NULL
);


ALTER TABLE public.staff OWNER TO travelwise;

--
-- Name: station_updates; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.station_updates (
    id integer NOT NULL,
    name character varying(64),
    location character varying(64),
    type public.stationupdatetype,
    original_station_id integer,
    author_id integer NOT NULL
);


ALTER TABLE public.station_updates OWNER TO travelwise;

--
-- Name: station_updates_id_seq; Type: SEQUENCE; Schema: public; Owner: travelwise
--

CREATE SEQUENCE public.station_updates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.station_updates_id_seq OWNER TO travelwise;

--
-- Name: station_updates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: travelwise
--

ALTER SEQUENCE public.station_updates_id_seq OWNED BY public.station_updates.id;


--
-- Name: stations; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.stations (
    id integer NOT NULL,
    name character varying(64),
    location character varying(64)
);


ALTER TABLE public.stations OWNER TO travelwise;

--
-- Name: stations_id_seq; Type: SEQUENCE; Schema: public; Owner: travelwise
--

CREATE SEQUENCE public.stations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stations_id_seq OWNER TO travelwise;

--
-- Name: stations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: travelwise
--

ALTER SEQUENCE public.stations_id_seq OWNED BY public.stations.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(64),
    password character varying(128),
    email character varying(128),
    name character varying(128),
    type public.usertype
);


ALTER TABLE public.users OWNER TO travelwise;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: travelwise
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO travelwise;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: travelwise
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: vehicles; Type: TABLE; Schema: public; Owner: travelwise
--

CREATE TABLE public.vehicles (
    id integer NOT NULL,
    name character varying(64),
    carrier_id integer NOT NULL,
    capacity integer,
    station_id integer
);


ALTER TABLE public.vehicles OWNER TO travelwise;

--
-- Name: vehicles_id_seq; Type: SEQUENCE; Schema: public; Owner: travelwise
--

CREATE SEQUENCE public.vehicles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vehicles_id_seq OWNER TO travelwise;

--
-- Name: vehicles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: travelwise
--

ALTER SEQUENCE public.vehicles_id_seq OWNED BY public.vehicles.id;


--
-- Name: route_stops id; Type: DEFAULT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.route_stops ALTER COLUMN id SET DEFAULT nextval('public.route_stops_id_seq'::regclass);


--
-- Name: route_times id; Type: DEFAULT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.route_times ALTER COLUMN id SET DEFAULT nextval('public.route_times_id_seq'::regclass);


--
-- Name: routes id; Type: DEFAULT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.routes ALTER COLUMN id SET DEFAULT nextval('public.routes_id_seq'::regclass);


--
-- Name: seats id; Type: DEFAULT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.seats ALTER COLUMN id SET DEFAULT nextval('public.seats_id_seq'::regclass);


--
-- Name: station_updates id; Type: DEFAULT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.station_updates ALTER COLUMN id SET DEFAULT nextval('public.station_updates_id_seq'::regclass);


--
-- Name: stations id; Type: DEFAULT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.stations ALTER COLUMN id SET DEFAULT nextval('public.stations_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: vehicles id; Type: DEFAULT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.vehicles ALTER COLUMN id SET DEFAULT nextval('public.vehicles_id_seq'::regclass);


--
-- Data for Name: route_stops; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.route_stops (id, arrival, departure, route_id, station_id) FROM stdin;
1	0	5	1	1
2	120	125	1	2
3	220	225	1	3
4	320	325	1	4
5	420	425	1	5
6	520	525	1	13
7	620	625	1	12
8	720	725	1	11
11	0	5	2	11
12	120	125	2	12
13	220	225	2	13
14	320	325	2	5
15	420	425	2	4
16	520	525	2	3
17	620	625	2	2
18	720	725	2	1
19	0	5	3	2
20	50	55	3	8
21	130	135	3	9
22	200	205	3	7
23	240	245	3	10
24	320	325	3	6
31	0	5	4	6
32	45	50	4	10
33	70	75	4	7
34	130	135	4	9
35	200	205	4	8
36	320	325	4	2
67	0	1	6	21
68	4	5	6	22
69	6	7	6	19
70	13	14	6	23
71	16	17	6	24
72	20	21	6	25
73	23	24	6	26
74	27	28	6	27
75	30	31	6	2
76	0	1	5	14
77	5	6	5	20
78	8	9	5	16
79	11	12	5	19
80	16	17	5	18
81	19	20	5	17
82	0	1	7	17
83	5	6	7	18
84	8	9	7	19
85	11	12	7	16
86	16	17	7	20
87	19	20	7	14
90	0	1	9	2
91	4	5	9	27
92	6	7	9	26
93	13	14	9	25
94	16	17	9	24
95	20	21	9	23
96	23	24	9	19
97	27	28	9	22
98	30	31	9	21
\.


--
-- Data for Name: route_times; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.route_times (id, "time", repeat, route_id, vehicle_id) FROM stdin;
1	04:00:00	{t,t,t,t,t,t,t}	1	2
2	20:00:00	{t,t,t,t,t,t,t}	1	2
205	04:00:00	{t,t,t,t,t,t,t}	5	5
4	00:00:00	{t,t,t,t,t,t,t}	2	3
5	16:00:00	{t,t,t,t,t,t,t}	2	3
6	00:00:00	{t,t,t,t,t,t,t}	3	1
7	08:00:00	{t,t,t,t,t,t,t}	3	1
8	16:00:00	{t,t,t,t,t,t,t}	3	1
9	22:00:00	{t,t,t,t,t,t,t}	3	1
206	05:00:00	{t,t,t,t,t,t,t}	5	5
11	06:00:00	{t,t,t,t,t,t,t}	4	4
12	14:00:00	{t,t,t,t,t,t,t}	4	4
13	20:00:00	{t,t,t,t,t,t,t}	4	4
207	06:00:00	{t,t,t,t,t,t,t}	5	5
208	07:00:00	{t,t,t,t,t,t,t}	5	5
209	08:00:00	{t,t,t,t,t,t,t}	5	5
210	09:00:00	{t,t,t,t,t,t,t}	5	5
211	10:00:00	{t,t,t,t,t,t,t}	5	5
212	11:00:00	{t,t,t,t,t,t,t}	5	5
213	12:00:00	{t,t,t,t,t,t,t}	5	5
214	13:00:00	{t,t,t,t,t,t,t}	5	5
215	14:00:00	{t,t,t,t,t,t,t}	5	5
216	15:00:00	{t,t,t,t,t,t,t}	5	5
217	16:00:00	{t,t,t,t,t,t,t}	5	5
218	17:00:00	{t,t,t,t,t,t,t}	5	5
219	18:00:00	{t,t,t,t,t,t,t}	5	5
220	19:00:00	{t,t,t,t,t,t,t}	5	5
221	20:00:00	{t,t,t,t,t,t,t}	5	5
222	21:00:00	{t,t,t,t,t,t,t}	5	5
223	22:00:00	{t,t,t,t,t,t,t}	5	5
224	23:00:00	{t,t,t,t,t,t,t}	5	5
225	04:30:00	{t,t,t,t,t,t,t}	5	5
226	05:30:00	{t,t,t,t,t,t,t}	5	5
227	06:30:00	{t,t,t,t,t,t,t}	5	5
228	07:30:00	{t,t,t,t,t,t,t}	5	5
229	08:30:00	{t,t,t,t,t,t,t}	5	5
230	09:30:00	{t,t,t,t,t,t,t}	5	5
231	10:30:00	{t,t,t,t,t,t,t}	5	5
232	11:30:00	{t,t,t,t,t,t,t}	5	5
233	12:30:00	{t,t,t,t,t,t,t}	5	5
234	13:30:00	{t,t,t,t,t,t,t}	5	5
235	14:30:00	{t,t,t,t,t,t,t}	5	5
236	15:30:00	{t,t,t,t,t,t,t}	5	5
237	16:30:00	{t,t,t,t,t,t,t}	5	5
238	17:30:00	{t,t,t,t,t,t,t}	5	5
239	18:30:00	{t,t,t,t,t,t,t}	5	5
240	19:30:00	{t,t,t,t,t,t,t}	5	5
241	20:30:00	{t,t,t,t,t,t,t}	5	5
242	21:30:00	{t,t,t,t,t,t,t}	5	5
243	22:30:00	{t,t,t,t,t,t,t}	5	5
244	04:00:00	{t,t,t,t,t,t,t}	7	5
245	05:00:00	{t,t,t,t,t,t,t}	7	5
246	06:00:00	{t,t,t,t,t,t,t}	7	5
247	07:00:00	{t,t,t,t,t,t,t}	7	5
248	08:00:00	{t,t,t,t,t,t,t}	7	5
249	09:00:00	{t,t,t,t,t,t,t}	7	5
250	10:00:00	{t,t,t,t,t,t,t}	7	5
251	11:00:00	{t,t,t,t,t,t,t}	7	5
252	12:00:00	{t,t,t,t,t,t,t}	7	5
253	13:00:00	{t,t,t,t,t,t,t}	7	5
254	14:00:00	{t,t,t,t,t,t,t}	7	5
255	15:00:00	{t,t,t,t,t,t,t}	7	5
256	16:00:00	{t,t,t,t,t,t,t}	7	5
257	17:00:00	{t,t,t,t,t,t,t}	7	5
258	18:00:00	{t,t,t,t,t,t,t}	7	5
259	19:00:00	{t,t,t,t,t,t,t}	7	5
260	20:00:00	{t,t,t,t,t,t,t}	7	5
261	21:00:00	{t,t,t,t,t,t,t}	7	5
262	22:00:00	{t,t,t,t,t,t,t}	7	5
263	23:00:00	{t,t,t,t,t,t,t}	7	5
264	04:30:00	{t,t,t,t,t,t,t}	7	5
265	05:30:00	{t,t,t,t,t,t,t}	7	5
266	06:30:00	{t,t,t,t,t,t,t}	7	5
267	07:30:00	{t,t,t,t,t,t,t}	7	5
268	08:30:00	{t,t,t,t,t,t,t}	7	5
269	09:30:00	{t,t,t,t,t,t,t}	7	5
270	10:30:00	{t,t,t,t,t,t,t}	7	5
271	11:30:00	{t,t,t,t,t,t,t}	7	5
272	12:30:00	{t,t,t,t,t,t,t}	7	5
273	13:30:00	{t,t,t,t,t,t,t}	7	5
274	14:30:00	{t,t,t,t,t,t,t}	7	5
275	15:30:00	{t,t,t,t,t,t,t}	7	5
276	16:30:00	{t,t,t,t,t,t,t}	7	5
277	17:30:00	{t,t,t,t,t,t,t}	7	5
278	18:30:00	{t,t,t,t,t,t,t}	7	5
279	19:30:00	{t,t,t,t,t,t,t}	7	5
280	20:30:00	{t,t,t,t,t,t,t}	7	5
281	21:30:00	{t,t,t,t,t,t,t}	7	5
282	22:30:00	{t,t,t,t,t,t,t}	7	5
167	04:15:00	{t,t,t,t,t,t,t}	6	6
168	05:15:00	{t,t,t,t,t,t,t}	6	6
169	06:15:00	{t,t,t,t,t,t,t}	6	6
170	07:15:00	{t,t,t,t,t,t,t}	6	6
171	08:15:00	{t,t,t,t,t,t,t}	6	6
172	09:15:00	{t,t,t,t,t,t,t}	6	6
173	10:15:00	{t,t,t,t,t,t,t}	6	6
174	11:15:00	{t,t,t,t,t,t,t}	6	6
175	12:15:00	{t,t,t,t,t,t,t}	6	6
176	13:15:00	{t,t,t,t,t,t,t}	6	6
177	14:15:00	{t,t,t,t,t,t,t}	6	6
178	15:15:00	{t,t,t,t,t,t,t}	6	6
179	16:15:00	{t,t,t,t,t,t,t}	6	6
180	17:15:00	{t,t,t,t,t,t,t}	6	6
181	18:15:00	{t,t,t,t,t,t,t}	6	6
182	19:15:00	{t,t,t,t,t,t,t}	6	6
183	20:15:00	{t,t,t,t,t,t,t}	6	6
184	21:15:00	{t,t,t,t,t,t,t}	6	6
185	22:15:00	{t,t,t,t,t,t,t}	6	6
186	04:45:00	{t,t,t,t,t,t,t}	6	6
187	05:45:00	{t,t,t,t,t,t,t}	6	6
188	06:45:00	{t,t,t,t,t,t,t}	6	6
189	07:45:00	{t,t,t,t,t,t,t}	6	6
190	08:45:00	{t,t,t,t,t,t,t}	6	6
191	09:45:00	{t,t,t,t,t,t,t}	6	6
192	10:45:00	{t,t,t,t,t,t,t}	6	6
193	11:45:00	{t,t,t,t,t,t,t}	6	6
194	12:45:00	{t,t,t,t,t,t,t}	6	6
195	13:45:00	{t,t,t,t,t,t,t}	6	6
196	14:45:00	{t,t,t,t,t,t,t}	6	6
197	15:45:00	{t,t,t,t,t,t,t}	6	6
198	16:45:00	{t,t,t,t,t,t,t}	6	6
199	17:45:00	{t,t,t,t,t,t,t}	6	6
200	18:45:00	{t,t,t,t,t,t,t}	6	6
201	19:45:00	{t,t,t,t,t,t,t}	6	6
202	20:45:00	{t,t,t,t,t,t,t}	6	6
203	21:45:00	{t,t,t,t,t,t,t}	6	6
204	22:45:00	{t,t,t,t,t,t,t}	6	6
284	04:15:00	{t,t,t,t,t,t,t}	9	6
285	05:15:00	{t,t,t,t,t,t,t}	9	6
286	06:15:00	{t,t,t,t,t,t,t}	9	6
287	07:15:00	{t,t,t,t,t,t,t}	9	6
288	08:15:00	{t,t,t,t,t,t,t}	9	6
289	09:15:00	{t,t,t,t,t,t,t}	9	6
290	10:15:00	{t,t,t,t,t,t,t}	9	6
291	11:15:00	{t,t,t,t,t,t,t}	9	6
292	12:15:00	{t,t,t,t,t,t,t}	9	6
293	13:15:00	{t,t,t,t,t,t,t}	9	6
294	14:15:00	{t,t,t,t,t,t,t}	9	6
295	15:15:00	{t,t,t,t,t,t,t}	9	6
296	16:15:00	{t,t,t,t,t,t,t}	9	6
297	17:15:00	{t,t,t,t,t,t,t}	9	6
298	18:15:00	{t,t,t,t,t,t,t}	9	6
299	19:15:00	{t,t,t,t,t,t,t}	9	6
300	20:15:00	{t,t,t,t,t,t,t}	9	6
301	21:15:00	{t,t,t,t,t,t,t}	9	6
302	22:15:00	{t,t,t,t,t,t,t}	9	6
303	04:45:00	{t,t,t,t,t,t,t}	9	6
304	05:45:00	{t,t,t,t,t,t,t}	9	6
305	06:45:00	{t,t,t,t,t,t,t}	9	6
306	07:45:00	{t,t,t,t,t,t,t}	9	6
307	08:45:00	{t,t,t,t,t,t,t}	9	6
308	09:45:00	{t,t,t,t,t,t,t}	9	6
309	10:45:00	{t,t,t,t,t,t,t}	9	6
310	11:45:00	{t,t,t,t,t,t,t}	9	6
311	12:45:00	{t,t,t,t,t,t,t}	9	6
312	13:45:00	{t,t,t,t,t,t,t}	9	6
313	14:45:00	{t,t,t,t,t,t,t}	9	6
314	15:45:00	{t,t,t,t,t,t,t}	9	6
315	16:45:00	{t,t,t,t,t,t,t}	9	6
316	17:45:00	{t,t,t,t,t,t,t}	9	6
317	18:45:00	{t,t,t,t,t,t,t}	9	6
318	19:45:00	{t,t,t,t,t,t,t}	9	6
319	20:45:00	{t,t,t,t,t,t,t}	9	6
320	21:45:00	{t,t,t,t,t,t,t}	9	6
321	22:45:00	{t,t,t,t,t,t,t}	9	6
\.


--
-- Data for Name: routes; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.routes (id, name, price, carrier_id) FROM stdin;
1	Inter Praha-Brno-Bratislava-Žilina-Košice	5	2
2	Inter Košice-Žilina-Bratislava-Brno-Praha	5	2
3	OsPRIM Brno-Myjava	2	2
4	OsPRIM Myjava-Brno	2	2
5	Brno-53	0.2	5
6	Brno-12	0.2	5
7	53-Brno	0.2	5
9	12-Brno	0.2	5
\.


--
-- Data for Name: seats; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.seats (id, date, amount, price, paid, name, created_at, email, user_id, from_stop_id, to_stop_id, time_id, route_id) FROM stdin;
1	2021-10-28	2	5	f	Jozef Nemko	2021-11-28 17:15:04.774031	jozef.nemko@gmail.com	10	2	3	1	1
3	2021-10-28	1	10	t	Jozef Nemko	2021-11-28 17:15:04.774031	jozef.nemko@gmail.com	10	19	24	8	3
2	2021-10-28	2	10	t	Jozef Nemko	2021-11-28 17:15:04.774031	jozef.nemko@gmail.com	10	16	18	5	2
6	2021-10-28	1	1.4000000000000001	f	Jozef Nemko	2021-11-28 17:15:04.774031	jozef.nemko@gmail.com	10	67	74	201	6
5	2021-10-28	2	1.6	t	Jozef Nemko	2021-11-28 17:15:04.774031	jozef.nemko@gmail.com	10	67	75	183	6
7	2021-10-28	1	0.4	f	Karol Jerguš	2021-11-28 17:15:04.774031	kjergus@azet.sk	10	79	81	240	5
8	2021-10-28	1	1	f	Karol Jerguš	2021-11-28 17:15:04.774031	kjergus@azet.sk	10	82	87	260	7
\.


--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.staff (user_id, carrier_id) FROM stdin;
3	2
6	2
7	2
8	5
9	5
\.


--
-- Data for Name: station_updates; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.station_updates (id, name, location, type, original_station_id, author_id) FROM stdin;
\.


--
-- Data for Name: stations; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.stations (id, name, location) FROM stdin;
1	Hl. Nádraží	Praha
2	Hl. Nádraží	Brno
3	Hl. Stanica	Bratislava
4	Hl. Stanica	Trnava
5	Hl. Stanica	Piešťany
6	Vlaková stanica	Myjava
7	Vlakové nádraží	Veselí nad Moravou
8	Slavkov u Brna	Slavkov u Brna
9	Vlakové nádraží	Kyjov
10	Vlakové nádraží	Velká nad Veličkou
11	Hl. Stanica	Košice
12	Hl. Stanica	Poprad
13	Hl. Stanica	Žilina
14	Kolejni	Brno
16	Záhřebská	Brno
17	Semilasso	Brno
18	Husitská	Brno
19	Skácelova	Brno
20	Technická	Brno
21	Technologický Park	Brno
22	Červinkova	Brno
23	Klusáčkova	Brno
24	Nerudova	Brno
25	Grohova	Brno
26	Česká	Brno
27	Nové Sady	Brno
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.users (id, username, password, email, name, type) FROM stdin;
1	admin	pbkdf2:sha256:260000$3mGG4JQMdBJNMd6a$bd100dfadb439a9bf485150e80be58fa6e232906cd821e61d4566384ee2e2a2b	admin@travelwise.online	Administrátor	admin
2	dopravca	pbkdf2:sha256:260000$Mw5E24CVbIiHDugp$f86b46118cd710d39416ec959ffeadd76b65eb8ac2a9ad8a4c42628e76557665	dopravca@travelwise.online	České dráhy	carrier
3	personal	pbkdf2:sha256:260000$4KgtfU7VZQiM0azY$765fe9299cf4a01b5601ce0a8543acab287283c3d218270611a078d6bd4548c7	personal@travelwise.online	Jozef Zeman	staff
5	dopravca2	pbkdf2:sha256:260000$26FNf9rfg0roTwYW$be6a9ad38e84c312dad62d58b8436b5c88f2fe603266056d4b7b30508d129cca	dopravca2@travelwise.online	DPMB	carrier
4	pasazier	pbkdf2:sha256:260000$HLZmE2H7A9WDfJbm$4d94d5c13f85aab1a8655a6a3d09f903b48e12c62512545530782a624bce6377	pasazier@travelwise.online	Dana Kramárová	passenger
6	personal2	pbkdf2:sha256:260000$rFB1JFwsffqMSi5Y$0ef798ab3d1017df75f34db144606b6baac3eff74ccea8e6f7ad45b56577ff85	personal2@travelwise.online	Martin Tenký	staff
7	personal3	pbkdf2:sha256:260000$TDAAtDJkEFOXeQVv$b19256748a2244cac506e9cf014700fc621925bd28eaf3a0a4f92840273f7c91	personal3@travelwise.online	Anton Drahý	staff
8	personal4	pbkdf2:sha256:260000$MuVWTCxMJfDhUpBH$ebdc25579ac04cce36f1d0df72c78c2d528e809a33a92d61cf6a37f6d8e2615b	personal4@travelwise.online	Gregor Losko	staff
9	personal5	pbkdf2:sha256:260000$xWelE4BrenLdvQ3n$710b3eab98ae9bfc7b0baf47a6dd4cadba873d4fa1bc1853ea11e6cef5a3f570	personal5@travelwise.online	Sára Nagyová	staff
10	jozef	pbkdf2:sha256:260000$XdxLTg6PZnDDoa8Y$d8944f744a57f82800123be081a367dc82b7fd3f28cf8c4d628abf9debdf9fd1	jozef.nemko@gmail.com	Jozef Nemko	passenger
\.


--
-- Data for Name: vehicles; Type: TABLE DATA; Schema: public; Owner: travelwise
--

COPY public.vehicles (id, name, carrier_id, capacity, station_id) FROM stdin;
1	Os4232	2	380	\N
2	R441	2	480	\N
3	R228	2	480	\N
5	Bus 53	5	40	\N
4	Os2442	2	380	\N
6	Šalina 12	5	60	\N
\.


--
-- Name: route_stops_id_seq; Type: SEQUENCE SET; Schema: public; Owner: travelwise
--

SELECT pg_catalog.setval('public.route_stops_id_seq', 98, true);


--
-- Name: route_times_id_seq; Type: SEQUENCE SET; Schema: public; Owner: travelwise
--

SELECT pg_catalog.setval('public.route_times_id_seq', 321, true);


--
-- Name: routes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: travelwise
--

SELECT pg_catalog.setval('public.routes_id_seq', 9, true);


--
-- Name: seats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: travelwise
--

SELECT pg_catalog.setval('public.seats_id_seq', 8, true);


--
-- Name: station_updates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: travelwise
--

SELECT pg_catalog.setval('public.station_updates_id_seq', 13, true);


--
-- Name: stations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: travelwise
--

SELECT pg_catalog.setval('public.stations_id_seq', 27, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: travelwise
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: vehicles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: travelwise
--

SELECT pg_catalog.setval('public.vehicles_id_seq', 6, true);


--
-- Name: route_stops route_stops_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.route_stops
    ADD CONSTRAINT route_stops_pkey PRIMARY KEY (id);


--
-- Name: route_times route_times_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.route_times
    ADD CONSTRAINT route_times_pkey PRIMARY KEY (id);


--
-- Name: routes routes_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_pkey PRIMARY KEY (id);


--
-- Name: seats seats_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.seats
    ADD CONSTRAINT seats_pkey PRIMARY KEY (id);


--
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (user_id, carrier_id);


--
-- Name: station_updates station_updates_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.station_updates
    ADD CONSTRAINT station_updates_pkey PRIMARY KEY (id);


--
-- Name: stations stations_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.stations
    ADD CONSTRAINT stations_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: vehicles vehicles_pkey; Type: CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_pkey PRIMARY KEY (id);


--
-- Name: ix_routes_carrier_id; Type: INDEX; Schema: public; Owner: travelwise
--

CREATE INDEX ix_routes_carrier_id ON public.routes USING btree (carrier_id);


--
-- Name: ix_staff_carrier_id; Type: INDEX; Schema: public; Owner: travelwise
--

CREATE INDEX ix_staff_carrier_id ON public.staff USING btree (carrier_id);


--
-- Name: ix_staff_user_id; Type: INDEX; Schema: public; Owner: travelwise
--

CREATE INDEX ix_staff_user_id ON public.staff USING btree (user_id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: travelwise
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: ix_vehicles_carrier_id; Type: INDEX; Schema: public; Owner: travelwise
--

CREATE INDEX ix_vehicles_carrier_id ON public.vehicles USING btree (carrier_id);


--
-- Name: route_stops route_stops_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.route_stops
    ADD CONSTRAINT route_stops_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(id) ON DELETE CASCADE;


--
-- Name: route_stops route_stops_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.route_stops
    ADD CONSTRAINT route_stops_station_id_fkey FOREIGN KEY (station_id) REFERENCES public.stations(id) ON DELETE CASCADE;


--
-- Name: route_times route_times_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.route_times
    ADD CONSTRAINT route_times_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(id) ON DELETE CASCADE;


--
-- Name: route_times route_times_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.route_times
    ADD CONSTRAINT route_times_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicles(id) ON DELETE CASCADE;


--
-- Name: routes routes_carrier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.routes
    ADD CONSTRAINT routes_carrier_id_fkey FOREIGN KEY (carrier_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: seats seats_from_stop_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.seats
    ADD CONSTRAINT seats_from_stop_id_fkey FOREIGN KEY (from_stop_id) REFERENCES public.route_stops(id) ON DELETE SET NULL;


--
-- Name: seats seats_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.seats
    ADD CONSTRAINT seats_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.routes(id) ON DELETE SET NULL;


--
-- Name: seats seats_time_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.seats
    ADD CONSTRAINT seats_time_id_fkey FOREIGN KEY (time_id) REFERENCES public.route_times(id) ON DELETE SET NULL;


--
-- Name: seats seats_to_stop_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.seats
    ADD CONSTRAINT seats_to_stop_id_fkey FOREIGN KEY (to_stop_id) REFERENCES public.route_stops(id) ON DELETE SET NULL;


--
-- Name: seats seats_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.seats
    ADD CONSTRAINT seats_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: staff staff_carrier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_carrier_id_fkey FOREIGN KEY (carrier_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: staff staff_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: station_updates station_updates_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.station_updates
    ADD CONSTRAINT station_updates_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: station_updates station_updates_original_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.station_updates
    ADD CONSTRAINT station_updates_original_station_id_fkey FOREIGN KEY (original_station_id) REFERENCES public.stations(id) ON DELETE CASCADE;


--
-- Name: vehicles vehicles_carrier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_carrier_id_fkey FOREIGN KEY (carrier_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: vehicles vehicles_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: travelwise
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_station_id_fkey FOREIGN KEY (station_id) REFERENCES public.stations(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

