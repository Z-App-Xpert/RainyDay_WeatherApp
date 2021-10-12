-- Adminer 4.6.3-dev PostgreSQL dump

\connect "d97papfr8pull";

DROP TABLE IF EXISTS "Tblcheckings";
DROP SEQUENCE IF EXISTS "Tblcheckings_id_seq";
CREATE SEQUENCE "Tblcheckings_id_seq" INCREMENT  MINVALUE  MAXVALUE  START 1 CACHE ;

CREATE TABLE "public"."Tblcheckings" (
    "id" integer DEFAULT nextval('"Tblcheckings_id_seq"') NOT NULL,
    "email" character varying(50),
    "comment" text,
    "zipcode" character varying(5),
    CONSTRAINT "Tblcheckings_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "Tbllocations";
DROP SEQUENCE IF EXISTS "Tbllocations_id_seq";
CREATE SEQUENCE "Tbllocations_id_seq" INCREMENT  MINVALUE  MAXVALUE  START 1 CACHE ;

CREATE TABLE "public"."Tbllocations" (
    "id" integer DEFAULT nextval('"Tbllocations_id_seq"') NOT NULL,
    "zipcode" character varying(5),
    "city" character varying(50),
    "state" character varying(3),
    "latitude" character varying(10),
    "longitude" character varying(10),
    "population" integer,
    "checkin_count" integer,
    CONSTRAINT "Tbllocations_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "Tblusers";
DROP SEQUENCE IF EXISTS "Tblusers_id_seq";
CREATE SEQUENCE "Tblusers_id_seq" INCREMENT  MINVALUE  MAXVALUE  START 1 CACHE ;

CREATE TABLE "public"."Tblusers" (
    "id" integer DEFAULT nextval('"Tblusers_id_seq"') NOT NULL,
    "name" character varying(50),
    "email" character varying(50),
    "password" character varying(100),
    CONSTRAINT "Tblusers_email_key" UNIQUE ("email"),
    CONSTRAINT "Tblusers_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2018-07-12 18:33:22.146258+00
