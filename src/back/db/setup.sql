/*
File: setup.sql

Created: 8/12/2019

Description: idea of how to flesh out the sqlite db
  
  Set up with the following commands:
  > sqlite3 db.sqlite3
  sqlite> .read setup.sql
*/


PRAGMA foreign_keys=OFF;


CREATE TABLE IF NOT EXISTS "category"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [name] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "requisition"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [status] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "receiving"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [status] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "manufacturer"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [name] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "supplier"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [name] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "purchase_order"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [number] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "department"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [name] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "user"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [name] TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS "asset"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [asset_id] TEXT NOT NULL,
    [description] TEXT NOT NULL,
    [is_current] INTEGER NOT NULL DEFAULT 2, -- 0: disposed/retired/salvaged, 1: in Harvest's possession, 2: awaiting assignment indicating status of possession (possibly unknown status or not yet received)
    [requisition] INTEGER NOT NULL DEFAULT 5, -- foreign key to requisition, either awaiting invoice, partial payment, paid in full, donated, or unspecified
    [receiving] INTEGER NOT NULL DEFAULT 4, -- foreign key to receiving, shipped, received, or placed, or unspecified
    [category_1] INTEGER, -- foreign key to category
    [category_2] INTEGER, -- foreign key to category
    [model_number] TEXT,
    [serial_number] TEXT,
    [bulk_count] INTEGER NOT NULL DEFAULT 1, -- often 1 but several entries are bulk
    [bulk_count_removed] INTEGER NOT NULL DEFAULT 0, -- how many of this entry are disposed/removed
    [date_placed] TEXT,
    [date_removed] TEXT,
    [date_record_created] TEXT NOT NULL DEFAULT (datetime(current_timestamp)),
    [date_warranty_expires] TEXT,
    [manufacturer] INTEGER, -- foreign key to manufacturer
    [supplier] INTEGER, -- foreign key to supplier
    [cost] INTEGER, -- what Harvest paid, stored as actual cost * 10000000000 (eg: $13.29 stored as 132900000000)
    [shipping] INTEGER, -- cost of shipping, stored as actual shipping cost * 10000000000
    [purchase_order] INTEGER, -- foreign key to purchase_order
    [cost_brand_new] INTEGER, -- brand new cost, stored as actual * 10000000000
    [life_expectancy_years] INTEGER,
    [notes] TEXT, -- combine "status" column with this one
    [department] INTEGER, -- foreign key to department
    [maint_dir] INTEGER, -- bool whether entered in Maintenance Direct
    
    /*
    FOREIGN KEYS for requisition, receiving, category_1, category_2, manufacturer, supplier, purchase_order, department
    */
    FOREIGN KEY ([requisition]) REFERENCES "requisition" ([id])
      ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY ([receiving]) REFERENCES "receiving" ([id])
      ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY ([category_1]) REFERENCES "category" ([id])
      ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY ([category_2]) REFERENCES "category" ([id])
      ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY ([manufacturer]) REFERENCES "manufacturer" ([id])
      ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY ([supplier]) REFERENCES "supplier" ([id])
      ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY ([purchase_order]) REFERENCES "purchase_order" ([id])
      ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY ([department]) REFERENCES "department" ([id])
      ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS "checkout"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [asset] INTEGER NOT NULL,
    [user] INTEGER NOT NULL,
    [date_out] TEXT NOT NULL DEFAULT (datetime(current_timestamp)),
    [date_in] TEXT,
    
    FOREIGN KEY ([asset]) REFERENCES "asset" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY ([user]) REFERENCES "user" ([name])
      ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS "account"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [number] TEXT NOT NULL,
    [description] TEXT
);

CREATE TABLE IF NOT EXISTS "far" -- line entry in fixed asset register
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [account] INTEGER, -- foreign key to account
    [description] TEXT,
    [pdf] INTEGER, -- unique identifier for line in fixed asset register
    [life] INTEGER, -- asset life in years
    [start_date] TEXT DEFAULT NULL,
    [amount] INTEGER, -- stores total dollar amount of this FAR line * 10000000000
    
    FOREIGN KEY ([account]) REFERENCES "account" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS "asset_far"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [asset] INTEGER,
    [far] INTEGER,
    
    FOREIGN KEY ([asset]) REFERENCES "asset" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY ([far]) REFERENCES "far" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS "location"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [description] TEXT NOT NULL,
    [parent] INTEGER,
    
    FOREIGN KEY ([parent]) REFERENCES "location" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS "location_count"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [asset] INTEGER NOT NULL,
    [location] INTEGER NOT NULL,
    [count] INTEGER NOT NULL,
    [audit_date] TEXT, -- store with datetime()
    
    FOREIGN KEY ([asset]) REFERENCES "asset" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY ([location]) REFERENCES "location" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS "invoice"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [number] TEXT,
    [file_path] TEXT,
    [total] INTEGER, --- stored as total * 10000000000
    [notes] TEXT,
    CHECK (number IS NOT NULL OR file_path IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS "asset_invoice"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [asset] INTEGER NOT NULL,
    [invoice] INTEGER NOT NULL,
    [cost] INTEGER, --- stored as cost * 10000000000, representing how much of the invoice that asset makes up
    
    FOREIGN KEY ([asset]) REFERENCES "asset" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY ([invoice]) REFERENCES "invoice" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS "picture" -- two or more assets can share a picture
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [file_path] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "asset_picture"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [asset] INTEGER NOT NULL,
    [picture] INTEGER NOT NULL,
    
    FOREIGN KEY ([asset]) REFERENCES "asset" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY ([picture]) REFERENCES "picture" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS "attachment" -- assets can have more than one attachment (file) and an attachment can have one or more assets
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [file_path] TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "asset_attachment"
(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [asset] INTEGER NOT NULL,
    [attachment] INTEGER NOT NULL,
    
    FOREIGN KEY ([asset]) REFERENCES "asset" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY ([attachment]) REFERENCES "attachment" ([id])
      ON DELETE CASCADE ON UPDATE NO ACTION
);

-- set up requisition and receiving lookup tables
insert into requisition (status) values ('awaiting invoice'),('partial payment'),('paid in full'),('donated'),('unspecified');

insert into receiving (status) values ('shipped'), ('received'), ('placed'),('unspecified');
