use omkaroptics;
SHOW PROCEDURE STATUS WHERE Db = DATABASE();
DELIMITER //

CREATE PROCEDURE add_stock_items (
  IN in_frame VARCHAR(50),
  IN in_type VARCHAR(50),
  IN in_count INT
)
BEGIN
  DECLARE i INT DEFAULT 1;
  DECLARE last_num INT DEFAULT 0;
  DECLARE max_suffix VARCHAR(10);
  DECLARE year_prefix VARCHAR(2);
  DECLARE prefix VARCHAR(10);
  DECLARE full_id VARCHAR(20);

  -- Get last two digits of the year (e.g., '25' for 2025)
  SET year_prefix = DATE_FORMAT(NOW(), '%y');

  -- Build prefix: e.g., '25WP'
  SET prefix = CONCAT(year_prefix,
                      UPPER(LEFT(in_frame, 1)),
                      UPPER(LEFT(in_type, 1)));

  -- Get the maximum suffix number for this prefix
  SELECT MAX(SUBSTRING(unique_no, LENGTH(prefix) + 1))
  INTO max_suffix
  FROM stock_items
  WHERE unique_no LIKE CONCAT(prefix, '%');

  -- If no previous entry, set to 0
  IF max_suffix IS NOT NULL THEN
    SET last_num = CAST(max_suffix AS UNSIGNED);
  ELSE
    SET last_num = 0;
  END IF;

  -- Insert loop
  WHILE i <= in_count DO
    SET last_num = last_num + 1;
    SET full_id = CONCAT(prefix, LPAD(last_num, 4, '0'));

    INSERT INTO stock_items (unique_no, frame, type, date)
    VALUES (full_id, in_frame, in_type, CURDATE());

    SET i = i + 1;
  END WHILE;
END //

DELIMITER ;

select * from eye_prescriptions;
select * from customers;
select * from stock_items;
DESCRIBE eye_prescriptions;
describe stock_items;
show tables;
ALTER TABLE customers ADD payment_status VARCHAR(20) DEFAULT 'Pending';
UPDATE customers
SET balance_amount = 0, payment_status = 'Paid'
WHERE customer_id = 1;
SELECT balance_amount FROM customers WHERE bill_no = 'B46486';
UPDATE customers SET balance_amount = 0, payment_status='Paid' WHERE bill_no = 'B46486';
SELECT 
    c.customer_id,
    c.name,
    c.phone_no,
    c.bill_no,
    c.order_date,
    c.balance_amount,
    c.payment_status,
    c.stock_unique_no,
    ep.eye_type,
    ep.re_sph, ep.re_cyl, ep.re_axis,
    ep.le_sph, ep.le_cyl, ep.le_axis
FROM 
    customers c
JOIN 
    eye_prescriptions ep ON c.customer_id = ep.customer_id
WHERE 
    c.phone_no = '9702667597';
