--- find relationships for each asset that makes up part of an invoice
--- (where the invoice might be associated with multiple assets)
select * from asset_invoice
inner join invoice on asset_invoice.invoice = invoice.id
where invoice.total > asset_invoice.cost;

--- find all invoices for which asset entries do not fully account for the invoice
--- (indicating invoices for which assets may still need to be entered)
select invoice.number, invoice.file_path, sum(cost), invoice.total from asset_invoice
inner join invoice on asset_invoice.invoice = invoice.id
group by invoice.id
having invoice.total > sum(cost);