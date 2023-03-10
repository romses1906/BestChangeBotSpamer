DROP TABLE IF EXISTS "groups" CASCADE;
DROP SEQUENCE IF EXISTS groups_id_seq;
CREATE SEQUENCE groups_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."groups" (
    "id" integer DEFAULT nextval('groups_id_seq') NOT NULL,
    "chat_id" bigint NOT NULL,
    "city" text NOT NULL,
    "message" text,
    CONSTRAINT "groups_id_uindex" UNIQUE ("id"),
    CONSTRAINT "groups_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "groups" ("id", "chat_id", "city", "message") VALUES
(1,	-1001793201153,	'Новосибирск',	'Хочешь больше зарабатывать - зайди на Best Change и проверь как мы стоим по твоему городу.\nНаши обменники: E-Change, FastWM, SpbWMCasher, YoChange, CoinShop24.\nТегай операторов, если нужно изменить ставки\n@CoyoteNSK\n\nhttps://www.bestchange.ru/tether-trc20-to-ruble-cash-in-nsk.html\n\nhttps://www.bestchange.ru/tether-trc20-to-dollar-cash-in-nsk.html'),
(2,	-1001793201153,	'Новосибирск',	'Коллеги, пришлите, пожалуйста, балансы региона, на которые могут рассчитывать ночные операторы!\n @CoyoteNSK'),
(3,	-860027213,	'Город',	'Хочешь больше зарабатывать - зайди на Best Change и проверь как мы стоим по твоему городу.\nНаши обменники: E-Change, FastWM, SpbWMCasher, YoChange, CoinShop24.\nТегай операторов, если нужно изменить ставки\n@CoyoteNSK\n\nhttps://www.bestchange.ru/tether-trc20-to-ruble-cash-in-nsk.html\n\nhttps://www.bestchange.ru/tether-trc20-to-dollar-cash-in-nsk.html');

DROP TABLE IF EXISTS "new_times";
CREATE TABLE "public"."new_times" (
    "time_id" integer NOT NULL,
    "time" time without time zone,
    "time_tz" timestamptz,
    "group_id" integer,
    "find_time" time with time zone,
    CONSTRAINT "new_times_pkey" PRIMARY KEY ("time_id")
) WITH (oids = false);


INSERT INTO "new_times" ("time_id", "time", "time_tz", "group_id", "find_time") VALUES
(6,	'03:30:00',	NULL,	1,	NULL),
(7,	'05:00:00',	NULL,	1,	NULL),
(8,	'08:00:00',	NULL,	1,	NULL),
(9,	'10:00:00',	NULL,	1,	NULL),
(14,	'11:37:00',	NULL,	2,	NULL),
(15,	'11:37:00',	NULL,	1,	NULL),
(16,	'13:30:00',	NULL,	2,	NULL),
(17,	'11:37:00',	NULL,	3,	NULL);


ALTER TABLE ONLY "public"."new_times" ADD CONSTRAINT "fk_group" FOREIGN KEY (group_id) REFERENCES groups(id) NOT DEFERRABLE;