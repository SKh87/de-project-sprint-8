-- DROP TABLE public.subscribers_restaurants;
create table public.subscribers_restaurants
(
    id            serial4 not null,
    client_id     uuid    not null,
    restaurant_id uuid    not null,
    constraint subscribers_restaurants_id_pkey primary key (id)
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

create table public.subscribers_feedback
(
    id                          serial4      not null,
    restaurant_id               uuid         not null,
    adv_campaign_id             uuid         not null,
    adv_campaign_content        text         not null,
    adv_campaign_owner          text         not null,
    adv_campaign_owner_contact  varchar(320) not null,
    adv_campaign_datetime_start timestamp    not null,
    adv_campaign_datetime_end   timestamp    not null,
    datetime_created            timestamp    not null,
    client_id                   uuid         not null,
    trigger_datetime_created    int4         not null,
    feedback                    varchar      null,
    constraint subscribers_feedback_id_pkey primary key (id)
);
