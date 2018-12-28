drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

-- This will set up a single table with three fields - "id", "title", and "text".
-- SQLite will be used for our RDMS since it's built in to the standard Python library
-- and requires no configuration.
