delete from manufacturer;
delete from supplier;
delete from category;
delete from department;
delete from asset;
delete from picture;
delete from asset_picture;
delete from invoice;
delete from asset_invoice;
delete from location;
delete from location_count;
update sqlite_sequence set seq = 0;

insert into manufacturer (name) values ('Carrier'),('Toshiba'),('Rheem');
insert into supplier (name) values ('Island Breeze'),('Japan AC, Inc.'),('Best Stuff');
insert into category (name) values ('AC'),('Furniture'),('AV/IT'),('Vehicles'),('Split AC Units'),('Chair'),('Camera');
insert into department (name) values ('SCHOOL'),('COFFEE SHOP'),('HOUSING'),('MAINTENANCE'),('CAFETERIA');

insert into asset (
    id, asset_id, description, is_current, requisition, receiving, category_1, category_2, 
    model_number, serial_number, bulk_count, date_placed, manufacturer, supplier, date_warranty_expires,
    cost, shipping, cost_brand_new, life_expectancy_years, notes, department, maint_dir)
values
(
    1, '000001', 'test 1', 1, 4, 1, 1, null,
    '38KCE009118', '1302770188', 1, '2019-01-01 15:00:01', 1, 1, '2020-03-25 00:00:00',
    1000.25*10000000000, 20*10000000000, 1000.25*10000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    2, '000002', 'test 2 - far 1', 1, 5, 2, 1, 4,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1, null,
    500*10000000000, null, 5000000000000, null, 'Replacement cost estimated.', 1, 0
),
(
    3, '000003', 'test 3 - far 2', 1, 2, 3, 1, null,
    '38KCE009118', '1302770188', 3, '2019-01-01 15:00:01', 1, 1, null,
    1000*10000000000, null, 10000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    4, '000004', 'test 4', 1, 3, null, 1, null,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1, null,
    500*10000000000, null, 5000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    5, '000005', 'test 5', 1, 3, 3, 1, null,
    '38KCE009118', '1302770188', 1, '2019-01-01 15:00:01', 1, 1, null,
    1000*10000000000, null, 10000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    6, '000006', 'test 6', 1, null, null, 1, null,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1, null,
    500*10000000000, null, 5000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    7, '000007', 'test 7', 1, null, null, 1, null,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1, null,
    500*10000000000, null, 5000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    8, '000008', 'test 8', 1, null, null, 1, null,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1, null,
    500*10000000000, null, 5000000000000, 8, 'Replacement cost estimated.', 1, 0
);

insert into picture (id, file_path) values
(1, 'assets\1.JPG'),
(2, 'assets\2.JPG'),
(3, 'assets\3.JPG');

insert into asset_picture (asset, picture) values
(1, 1), (1, 2), (1, 3), 
(2, 2), 
(3, 3);


-- ########################################################################
-- LOCATIONS, COUNTS, AUDITS
insert into location (id, description, parent) values
(1, 'root', null), (2, 'subA', 1), (3, 'subB', 1),
(4, 'subA-1', 2), (5, 'subB-1', 3), (6, 'subB-2', 3);

insert into location_count (id, asset, location, count, audit_date) values
(1, 2, 1, 1, null),
(2, 3, 3, 1, null),
(3, 3, 6, 2, '2020-03-24 13:00:00');

-- Location Tree:
--		root ('test 3')
--	      /     \
--         subA    subB ('test 4')
--         /       /   \
--      subA-1  subB-1  subB-2 ('test 4' x 2, audited 2020-03-24 13:00:00)
--
-- ########################################################################


-- ########################################################################
-- INVOICES
insert into invoice (id, number, total, file_path, notes) values
(1, '100', 100*10000000000, 'invoices\1a.pdf',  'Testing invoice 1'),
(2, '200', 200*10000000000, 'invoices\1a2b.pdf',  'Testing invoice 2'),
(3, '300', 250*10000000000, 'invoices\1a2b3c.pdf',  'Testing invoice 3'),
(4, '400', 250*10000000000, 'invoices\1a2b3c4d.pdf', 'Testing invoice 4'),
(5, '500', 500*10000000000, 'invoices\1a2b3c4d5e.png', 'Testing invoice 5'),
(6, '600', 500*10000000000, 'invoices\1a2b3c4d5e6f.png', 'Testing invoice 6'),
(7, '700', 5000*10000000000, 'invoices\1a2b3c4d5e6f7g.png', 'Testing invoice 7'),
(8, '800', 1000*10000000000, 'invoices\1a2b3c4d5e6f7g8h.png', 'Testing invoice 8');

insert into asset_invoice (asset, invoice, cost) values
-- TODO: translate these cases into tests for (1) validating asset invoice associations,
-- TODO: (2) searching all assets that belong to a given invoice,
-- TODO: (4) searching all assets that have no invoice association,
-- TODO: (5) searching all invoices that have no asset association
-- CASE 1: asset has 2 invoices, total from both invoices less than total asset cost
(1, 1, 100*10000000000), -- asset 1 total cost is $1000.25
(1, 2, 50*10000000000),  -- asset 1 remaining cost not on invoices: $850.25
-- CASE 2: asset has 2 invoices, total from both invoices equal to total asset cost (of $500)
(2, 3, 250*10000000000),
(2, 4, 250*10000000000),
-- CASE 3: asset has 1 invoice, invoice amount less than total asset cost (of $1000)
(3, 5, 500*10000000000),
-- CASE 4: asset has 1 invoice, invoice amount equals total asset cost (of $500)
(4, 6, 500*1000000000),
-- CASE 5: invoice has 2 assets, combined total cost of both assets ($1000 and $500) less than total invoice amount ($5000)
(5, 7, 1000*10000000000),
(6, 7, 500*10000000000),
-- CASE 6: invoice has 2 assets, combined total cost of both ($500 + $500) equals total invoice amount ($1000)
(7, 8, 500*10000000000),
(8, 8, 500*10000000000);
-- CASE 7: asset has no invoices
-- CASE 8: invoice has no assets


-- ########################################################################
-- TODO: FIXED ASSET REGISTER ASSOCIATIONS 
-- insert into far (id, account, description, pdf, life,  start_date, amount) values
-- (1, 60261, 'test account 1', 100, 5, '2020-02-02 00:00:00', 2000*10000000000),
-- (2, 60262, 'test account 2', 101, 8, '2000-02-02 00:00:00', 4000.61*10000000000);
-- 
-- insert into asset_far (id, asset, far) values
-- (1, 2, 1), (2, 3, 2); 

