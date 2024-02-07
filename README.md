CREATE
OR REPLACE VIEW "compressed_ledger_cache"."vw_orders" AS
SELECT
    co.sf_order_id,
    co.source,
    CASE
    WHEN co.source:: text = 'DIRECT':: character varying:: text
    OR co.source:: text = 'INTERNAL':: character varying:: text THEN 'spoonflower':: character varying
    WHEN co.source:: text = 'ROOSTERY':: character varying:: text THEN 'roostery':: character varying
    WHEN co.source:: text = 'DISTRO':: character varying:: text THEN cdo.shop_code
    ELSE NULL:: character varying END AS shop_code,
    co.paid_at,
    co.currency_code,
    po.exchange_rate,
    co.items_subtotal,
    co.items_subtotal / po.exchange_rate AS items_subtotal_usd,
    co.tax_total,
    co.tax_total / po.exchange_rate AS tax_total_usd,
    co.shipping_subtotal,
    co.shipping_subtotal / po.exchange_rate AS shipping_subtotal_usd,
    co.order_total,
    co.order_total / po.exchange_rate AS order_total_usd,
    co.total_discount,
    co.total_discount / po.exchange_rate AS total_discount_usd,
    co.tax_type,
    co.tax_exemption_id,
    co.is_rush_shipping,
    co.freight_class,
    co.address1,
    co.address2,
    co.city,
    co.state,
    co.zipcode,
    co.country,
    co.last_ledger_transaction_type,
    co.last_ledger_transaction_at,
    co.is_legacy,
    co.checkout_bookmark,
    co.row_created_at,
    co.row_updated_at,
    co.shipped_at,
    co.tax_rate,
    CASE
    WHEN po.is_comped = true THEN true
    ELSE false END AS is_comped,
    CASE
    WHEN co.source:: text = 'DIRECT':: character varying:: text THEN doi.sf_user_id
    WHEN co.source:: text = 'INTERNAL':: character varying:: text THEN ioi.sf_user_id
    WHEN co.source:: text = 'ROOSTERY':: character varying:: text THEN roi.sf_target_user_id
    WHEN co.source:: text = 'DISTRO':: character varying:: text THEN cdo.sf_target_user_id
    ELSE NULL:: integer END AS user_id
FROM
    orders co
    LEFT JOIN public.fct_orders po ON co.sf_order_id = po.id
    LEFT JOIN distro_order_info cdo ON co.sf_order_id = cdo.sf_order_id
    LEFT JOIN direct_order_info doi ON doi.sf_order_id = co.sf_order_id
    LEFT JOIN internal_order_info ioi ON ioi.sf_order_id = co.sf_order_id
    LEFT JOIN roostery_order_info roi ON roi.sf_order_id = co.sf_order_id;
