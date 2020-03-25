delete from manufacturer;
delete from supplier;
delete from category;
delete from department;
delete from asset;
delete from picture;
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
    2, '000003', 'test 3', 1, 5, 2, 1, 4,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1, null,
    5000000000000, null, 5000000000000, null, 'Replacement cost estimated.', 1, 0
),
(
    3, '000004', 'test 4', 1, 2, 3, 1, null,
    '38KCE009118', '1302770188', 3, '2019-01-01 15:00:01', 1, 1, null,
    10000000000000, null, 10000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    4, '000005', 'test 5', 1, 3, null, 1, null,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1, null,
    5000000000000, null, 5000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    5, '000006', 'test 6', 1, 3, 3, 1, null,
    '38KCE009118', '1302770188', 1, '2019-01-01 15:00:01', 1, 1, null,
    10000000000000, null, 10000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    6, '000007', 'test 7', 1, null, null, 1, null,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1, null,
    5000000000000, null, 5000000000000, 8, 'Replacement cost estimated.', 1, 0
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
