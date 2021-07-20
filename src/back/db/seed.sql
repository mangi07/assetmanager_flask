delete from manufacturer;
delete from supplier;
delete from category;
delete from department;
delete from asset;
delete from picture;
delete from asset_picture;
delete from invoice;
delete from asset_invoice;
delete from far;
delete from account;
delete from asset_far;
delete from location;
delete from location_count;
update sqlite_sequence set seq = 0;

insert into manufacturer (name) values ('Carrier'),('Toshiba'),('Rheem');
insert into supplier (name) values ('Island Breeze'),('Japan AC, Inc.'),('Best Stuff');
insert into category (name) values ('AC'),('Furniture'),('AV/IT'),('Vehicles'),('Split AC Units'),('Chair'),('Camera');
insert into department (name) values ('SCHOOL'),('COFFEE SHOP'),('HOUSING'),('MAINTENANCE'),('CAFETERIA');

insert into asset (id, asset_id, description) values 
	(1, "000001", "test 1"),
	(2, "000002", "test 2 - far 1"),
	(3, "000003", "test 3 - far 2"),
	(4, "000004", "test 4"),
	(5, "000005", "test 5"),
	(6, "000006", "test 6"),
	(7, "000007", "test 7"),
	(8, "000008", "test 8");

update asset set
	asset_id = '000001',
	description = 'test 1',
	is_current = 1,
	requisition = 4,
	receiving = 1,
	category_1 = 1,
	category_2 = null,
	model_number = '38KCE009118',
	serial_number = '1302770188',
	bulk_count = 1,
	date_placed = '2019-01-01 15:00:01',
	manufacturer = 1,
	supplier = 1,
	date_warranty_expires = '2020-03-25 00:00:00',
	cost = 1000.25*10000000000,
	shipping = 20*10000000000,
	cost_brand_new = 1000.25*10000000000,
	life_expectancy_years = 8,
	notes = 'Replacement cost estimated.',
	department = 1,
	maint_dir = 0
where id = 1;

update asset set
    asset_id = '000002',
    description = 'test 2 - far 1',
    is_current = 1,
    requisition = 5,
    receiving = 2,
    category_1 = 1,
    category_2 = 4,
    model_number = '15KCE009119',
    serial_number = '1302770189',
    bulk_count = 1,
    date_placed = '2019-01-01 15:00:01',
    manufacturer = 1,
    supplier = 1,
    date_warranty_expires = null,
    cost = 500*10000000000,
    shipping = null,
    cost_brand_new = 5000000000000,
    life_expectancy_years = null,
    notes = 'Replacement cost estimated.',
    department = 1,
    maint_dir = 0
where id = 2;

update asset set
    asset_id = '000003',
    description = 'test 3 - far 2',
    is_current = 1,
    requisition = 2,
    receiving = 3,
    category_1 = 1,
    category_2 = null,
    model_number = '38KCE009118',
    serial_number = '1302770188',
    bulk_count = 3,
    date_placed = '2019-01-01 15:00:01',
    manufacturer = 1,
    supplier = 1,
    date_warranty_expires = null,
    cost = 1000*10000000000,
    shipping = null,
    cost_brand_new = 10000000000000,
    life_expectancy_years = 8,
    notes = 'Replacement cost estimated.',
    department = 1,
    maint_dir = 0
where id = 3;

update asset set
    asset_id = '000004',
    description = 'test 4',
    is_current = 1,
    requisition = 5,
    receiving = 4,
    category_1 = 1,
    category_2 = null,
    model_number = '15KCE009119',
    serial_number = '1302770189',
    bulk_count = 1,
    date_placed = '2019-01-01 15:00:01',
    manufacturer = 1,
    supplier = 1,
    date_warranty_expires = null,
    cost = 500*10000000000,
    shipping = null,
    cost_brand_new = 5000000000000,
    life_expectancy_years = 8,
    notes = 'Replacement cost estimated.',
    department = 1,
    maint_dir = 0
where id = 4;

update asset set
    asset_id = '000005',
    description = 'test 5',
    is_current = 1,
    requisition = 3,
    receiving = 3,
    category_1 = 1,
    category_2 = null,
    model_number = '38KCE009118',
    serial_number = '1302770188',
    bulk_count = 1,
    date_placed = '2019-01-01 15:00:01',
    manufacturer = 1,
    supplier = 1,
    date_warranty_expires = null,
    cost = 1000*10000000000,
    shipping = null,
    cost_brand_new = 10000000000000,
    life_expectancy_years = 8,
    notes = 'Replacement cost estimated.',
    department = 1,
    maint_dir = 0
where id = 5;

update asset set
    asset_id = '000006',
    description = 'test 6',
    is_current = 1,
    requisition = 5,
    receiving = 4,
    category_1 = 1,
    category_2 = null,
    model_number = '15KCE009119',
    serial_number = '1302770189',
    bulk_count = 1,
    date_placed = '2019-01-01 15:00:01',
    manufacturer = 1,
    supplier = 1,
    date_warranty_expires = null,
    cost = 500*10000000000,
    shipping = null,
    cost_brand_new = 5000000000000,
    life_expectancy_years = 8,
    notes = 'Replacement cost estimated.',
    department = 1,
    maint_dir = 0
where id = 6;

update asset set
    asset_id = '000007',
    description = 'test 7',
    is_current = 0,
    requisition = 5,
    receiving = 4,
    category_1 = 1,
    category_2 = null,
    model_number = '15KCE009119',
    serial_number = '1302770189',
    bulk_count = 1,
    date_placed = '2019-01-01 15:00:01',
    date_removed = '2029-01-01 15:00:01',
    manufacturer = 1,
    supplier = 1,
    date_warranty_expires = null,
    cost = 500*10000000000,
    shipping = null,
    cost_brand_new = 500*10000000000,
    life_expectancy_years = 8,
    notes = 'Replacement cost estimated.',
    department = 1,
    maint_dir = 0
where id = 7;

update asset set
    asset_id = '000008',
    description = 'test 8',
    is_current = 1,
    requisition = 5,
    receiving = 4,
    category_1 = 1,
    category_2 = null,
    model_number = '15KCE009119',
    serial_number = '1302770189',
    bulk_count = 1,
    date_placed = '2019-01-01 15:00:01',
    manufacturer = 1,
    supplier = 1,
    date_warranty_expires = null,
    cost = 500*10000000000,
    shipping = null,
    cost_brand_new = 5000000000000,
    life_expectancy_years = 8,
    notes = 'Replacement cost estimated.',
    department = 1,
    maint_dir = 0
where id = 8;


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
-- FIXED ASSET REGISTER ASSOCIATIONS 
insert into account (id, number, description) values
(1, '60261', 'test account 1'),
(2, '60262', 'test account 2');

insert into far (id, account, description, pdf, life,  start_date, amount) values
(1, 1, 'test far 1', 100, 5, '2020-02-02 00:00:00', 2000*10000000000),
(2, 2, 'test far 2', 101, 8, '2000-02-02 00:00:00', 4000.61*10000000000);

insert into asset_far (id, asset, far) values
(1, 2, 1), (2, 3, 2); 

