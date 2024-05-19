-- DROP TABLE public.subscribers_restaurants;

CREATE TABLE public.subscribers_restaurants
(
    id            serial4 NOT NULL,
    client_id     varchar NOT NULL,
    restaurant_id varchar NOT NULL,
    CONSTRAINT pk_id PRIMARY KEY (id)
);

-- Пример заполненных данных
insert into public.subscribers_restaurants(client_id, restaurant_id)
values ('223e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000'),
       ('323e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000'),
       ('423e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000'),
       ('523e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000'),
       ('623e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000'),
       ('723e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000'),
       ('823e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000'),
       ('923e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174001'),
       ('023e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000'),
       ('123e4567-e89b-12d3-a456-426614174000', '123e4567-e89b-12d3-a456-426614174000');



-- Выходная таблица
-- DROP TABLE public.subscribers_feedback;

CREATE TABLE public.subscribers_feedback
(
    id                          serial4 NOT NULL,
    restaurant_id               text    NOT NULL,
    adv_campaign_id             text    NOT NULL,
    adv_campaign_content        text    NOT NULL,
    adv_campaign_owner          text    NOT NULL,
    adv_campaign_owner_contact  text    NOT NULL,
    adv_campaign_datetime_start int8    NOT NULL,
    adv_campaign_datetime_end   int8    NOT NULL,
    datetime_created            int8    NOT NULL,
    client_id                   text    NOT NULL,
    trigger_datetime_created    int4    NOT NULL,
    feedback                    varchar NULL,
    CONSTRAINT id_pk PRIMARY KEY (id)
);
