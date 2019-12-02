/*
File: clear_tables.sql
*/

delete from "category";
delete from "manufacturer";
delete from "supplier";
delete from "purchase_order";
delete from "department";
delete from "user";
delete from "asset";
delete from "category";
delete from "checkout";
delete from "account";
delete from "far";
delete from "asset_far";
delete from "location";
delete from "location_count";
delete from "invoice";
delete from "asset_invoice";
delete from "picture";
delete from "asset_picture";
delete from "sqlite_sequence";
delete from "requisition";
delete from "receiving";

-- set up requisition and receiving lookup tables
insert into requisition (status) values ('awaiting invoice'),('partial payment'),('paid in full'),('donated');

insert into receiving (status) values ('shipped'), ('received'), ('placed');