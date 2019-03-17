drop table if exists ospf;
CREATE TABLE ospf {
    name text primary key not null,
    username text not null,
    password text not null,
    pid not null,
    area_id text,
    loopbackIP text 
};
