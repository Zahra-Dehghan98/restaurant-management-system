-- menu items 
create table menu_items (
id serial primary key,
name varchar(50) not null,
price decimal(10,2) not null check (price >= 0)
);

-- Tables
create table "tables" (
id serial primary key,
table_number integer UNIQUE not null,
status varchar(150) not null DEFAULT 'available'
);

-- orders
create table orders (
id serial primary key,
table_id integer REFERENCES tables(id) on delete cascade,
order_time timestamp DEFAULT current_timestamp,
status varchar(150) not null DEFAULT 'pending'
);

-- order details
create table order_details (
id serial primary key,
order_id integer REFERENCES orders(id) ON DELETE CASCADE,
item_id integer REFERENCES menu_items(id),
quantity integer not null check (quantity > 0)
);