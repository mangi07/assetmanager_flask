delete from manufacturer;
delete from supplier;
delete from category;
delete from department;
delete from asset;
update sqlite_sequence set seq = 0;

insert into manufacturer (name) values ('Carrier'),('Toshiba'),('Rheem');
insert into supplier (name) values ('Island Breeze'),('Japan AC, Inc.'),('Best Stuff');
insert into category (name) values ('AC'),('Furniture'),('AV/IT'),('Vehicles'),('Split AC Units'),('Chair'),('Camera');
insert into department (name) values ('SCHOOL'),('COFFEE SHOP'),('HOUSING'),('MAINTENANCE'),('CAFETERIA');


insert into asset (
    asset_id, description, is_current, requisition, receiving, category_1, category_2, 
    model_number, serial_number, bulk_count, date_placed, manufacturer, supplier,
    cost, shipping, cost_brand_new, life_expectancy_years, notes, department, maint_dir)
values
(
    '000001', 'test 1', 1, 3, 3, 1, null,
    '38KCE009118', '1302770188', 1, '2019-01-01 15:00:01', 1, 1,
    10000000000000, null, 10000000000000, 8, 'Replacement cost estimated.', 1, 0
),
(
    '000002', 'test 2', 1, 3, 3, 1, null,
    '15KCE009119', '1302770189', 1, '2019-01-01 15:00:01', 1, 1,
    5000000000000, null, 5000000000000, 8, 'Replacement cost estimated.', 1, 0
);