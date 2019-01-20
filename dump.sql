--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: items_in_cart; Type: TABLE; Schema: public; Owner: gracegan
--

CREATE TABLE public.items_in_cart (
    item_count integer DEFAULT 0,
    cart_id integer NOT NULL,
    product_id integer NOT NULL
);

--
-- Name: products; Type: TABLE; Schema: public; Owner: gracegan
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    title character varying(50) NOT NULL,
    price double precision NOT NULL,
    inventory_count integer NOT NULL
);


--
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: gracegan
--

CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

--
-- Name: products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gracegan
--

ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;


--
-- Name: shopping_cart; Type: TABLE; Schema: public; Owner: gracegan
--

CREATE TABLE public.shopping_cart (
    cart_id integer NOT NULL,
    purchase_status boolean DEFAULT false NOT NULL
);


--
-- Name: shopping_cart_cart_id_seq; Type: SEQUENCE; Schema: public; Owner: gracegan
--

CREATE SEQUENCE public.shopping_cart_cart_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: shopping_cart_cart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gracegan
--


--
-- Name: products product_id; Type: DEFAULT; Schema: public; Owner: gracegan
--

ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);


--
-- Name: shopping_cart cart_id; Type: DEFAULT; Schema: public; Owner: gracegan
--

ALTER TABLE ONLY public.shopping_cart ALTER COLUMN cart_id SET DEFAULT nextval('public.shopping_cart_cart_id_seq'::regclass);


--
-- Name: items_in_cart items_in_cart_pkey; Type: CONSTRAINT; Schema: public; Owner: gracegan
--

ALTER TABLE ONLY public.items_in_cart
    ADD CONSTRAINT items_in_cart_pkey PRIMARY KEY (cart_id, product_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: gracegan
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: products products_title_key; Type: CONSTRAINT; Schema: public; Owner: gracegan
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_title_key UNIQUE (title);


--
-- Name: shopping_cart table_name_pk; Type: CONSTRAINT; Schema: public; Owner: gracegan
--

ALTER TABLE ONLY public.shopping_cart
    ADD CONSTRAINT table_name_pk PRIMARY KEY (cart_id);


--
-- Name: items_in_cart items_in_cart_cart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gracegan
--

ALTER TABLE ONLY public.items_in_cart
    ADD CONSTRAINT items_in_cart_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES public.shopping_cart(cart_id);


--
-- Name: items_in_cart items_in_cart_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gracegan
--

ALTER TABLE ONLY public.items_in_cart
    ADD CONSTRAINT items_in_cart_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- PostgreSQL database dump complete
--

-- Insert some products
INSERT INTO public.products (title, price, inventory_count) VALUES ('Peach', 4, 40);
INSERT INTO public.products (title, price, inventory_count) VALUES ('Orange', 3, 30);
INSERT INTO public.products (title, price, inventory_count) VALUES ('Pear', 2, 50);
INSERT INTO public.products (title, price, inventory_count) VALUES ('Strawberry', 5, 100);