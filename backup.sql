-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: omkaroptics
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone_no` varchar(15) NOT NULL,
  `bill_no` varchar(50) NOT NULL,
  `order_date` date NOT NULL,
  `dob` date NOT NULL,
  `stock_unique_no` varchar(20) DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `after_discount` decimal(10,2) NOT NULL,
  `advance_amount` decimal(10,2) NOT NULL,
  `balance_amount` decimal(10,2) NOT NULL,
  `Lens` varchar(100) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT 'Pending',
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `bill_no` (`bill_no`),
  KEY `customers_ibfk_1` (`stock_unique_no`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`stock_unique_no`) REFERENCES `stock_items` (`unique_no`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Siddhesh Ganesh Chavan','9702667597','B12345','2025-06-06','2025-06-03','25WP0001',1000.00,500.00,200.00,0.00,NULL,'none','Paid'),(2,'Rohan Ganesh Chavan','9702667597','B4567','2025-06-06','2025-06-06','25WP0006',1000.00,500.00,200.00,0.00,NULL,NULL,'Paid'),(3,'Sarita Ganesh Chavan','9702667597','B4568','2025-06-08','2025-05-07','25WP0004',1000.00,200.00,100.00,0.00,NULL,NULL,'Paid'),(10,'Sidaef','9702667597','B456723','2025-06-08','2025-06-08',NULL,1000.00,800.00,100.00,0.00,'Progressive','Disposal','Paid'),(11,'Manesh Chavan','9702667597','B5699','2025-06-08','2025-03-19',NULL,1000.00,800.00,500.00,0.00,'Progressive','disposal','Paid'),(12,'Omkar','9702667597','B46486','2025-06-08','2025-06-08',NULL,1000.00,800.00,100.00,0.00,'Progressive','Dsiposal','Paid'),(13,'Hidawd','9702667597','B46468','2025-06-08','2025-06-03',NULL,1000.00,900.00,900.00,0.00,'awdwa','ADW','Paid'),(14,'Smruti','9702736449','B987','2025-08-22','2025-08-13','25WS0001',1000.00,980.00,100.00,0.00,NULL,NULL,'Paid'),(15,'Omkar','9702667598','B879','2025-08-22','2025-08-11',NULL,1000.00,980.00,100.00,880.00,'Disposal','Monthy disposal','Pending'),(16,'Smruti','9702667597','B5678','2025-08-22','2025-08-06',NULL,950.00,950.00,500.00,0.00,'Blue Block',NULL,'Paid'),(17,'adwdwa','9702667597','B1234897','2025-08-22','2025-08-22','25WP0002',1000.00,1000.00,0.00,1000.00,NULL,NULL,'Pending'),(18,'sMRUTI','9702667597','B564','2025-11-01','2025-11-01',NULL,1000.00,800.00,400.00,400.00,'nONE',NULL,'Pending'),(19,'Siddhesh','9702736448','b3753','2025-11-01','2025-11-01','25WP0003',1000.00,800.00,400.00,400.00,NULL,NULL,'Pending'),(20,'kashinath kasrung','9819854363','401','2025-11-02','1972-11-21','25SW0001',1000.00,800.00,400.00,0.00,NULL,NULL,'Paid');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eye_prescriptions`
--

DROP TABLE IF EXISTS `eye_prescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eye_prescriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `eye_type` enum('Distance','Reading') NOT NULL,
  `re_sph` decimal(5,2) DEFAULT NULL,
  `re_cyl` decimal(5,2) DEFAULT NULL,
  `re_axis` int DEFAULT NULL,
  `le_sph` decimal(5,2) DEFAULT NULL,
  `le_cyl` decimal(5,2) DEFAULT NULL,
  `le_axis` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `eye_prescriptions_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eye_prescriptions`
--

LOCK TABLES `eye_prescriptions` WRITE;
/*!40000 ALTER TABLE `eye_prescriptions` DISABLE KEYS */;
INSERT INTO `eye_prescriptions` VALUES (1,2,'Distance',8.00,5.00,120,0.00,0.00,0),(2,2,'Reading',0.00,0.00,0,1.50,8.00,120),(3,3,'Distance',1.00,5.00,180,0.00,0.00,0),(4,3,'Reading',0.00,0.00,0,0.00,0.00,0),(5,10,'Distance',1.00,2.00,120,0.00,0.00,0),(6,10,'Reading',0.00,0.00,0,0.00,0.00,0),(7,11,'Distance',1.00,2.00,120,0.00,0.00,0),(8,11,'Reading',0.00,0.00,0,0.00,0.00,0),(9,12,'Distance',0.00,0.00,0,0.00,0.00,0),(10,12,'Reading',5.00,4.00,120,0.00,0.00,0),(11,13,'Distance',2.00,2.00,120,0.00,0.00,0),(12,13,'Reading',0.00,0.00,0,0.00,0.00,0),(13,14,'Distance',1.00,2.00,180,0.00,0.00,0),(14,14,'Reading',0.00,0.00,0,120.00,20.00,120),(15,15,'Distance',45.00,20.00,120,0.00,0.00,0),(16,15,'Reading',0.00,0.00,0,120.00,15.00,120),(17,16,'Distance',-1.00,0.00,0,-0.25,0.00,0),(18,16,'Reading',0.00,0.00,0,0.00,0.00,0),(19,17,'Distance',0.00,0.00,0,0.00,0.00,0),(20,17,'Reading',0.00,0.00,0,0.00,0.00,0),(21,18,'Distance',1.00,2.00,180,0.00,0.00,0),(22,18,'Reading',0.00,0.00,0,0.00,0.00,0),(23,19,'Distance',6.00,2.00,160,0.00,0.00,0),(24,19,'Reading',0.00,0.00,0,0.00,0.00,0),(25,20,'Distance',8.00,1.00,120,0.00,0.00,0),(26,20,'Reading',0.00,0.00,0,0.00,0.00,0);
/*!40000 ALTER TABLE `eye_prescriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_items`
--

DROP TABLE IF EXISTS `stock_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_items` (
  `unique_no` varchar(20) NOT NULL,
  `frame` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  `customer_id` int DEFAULT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`unique_no`),
  KEY `fk_stock_customer` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_items`
--

LOCK TABLES `stock_items` WRITE;
/*!40000 ALTER TABLE `stock_items` DISABLE KEYS */;
INSERT INTO `stock_items` VALUES ('25SW0001','Sheet','WaterColor',20,'2025-11-02'),('25SW0002','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0003','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0004','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0005','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0006','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0007','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0008','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0009','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0010','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0011','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0012','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0013','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0014','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0015','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0016','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0017','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0018','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0019','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0020','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0021','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0022','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0023','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0024','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0025','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0026','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0027','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0028','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0029','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0030','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0031','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0032','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0033','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0034','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0035','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0036','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0037','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0038','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0039','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0040','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0041','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0042','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0043','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0044','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0045','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0046','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0047','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0048','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0049','Sheet','WaterColor',NULL,'2025-11-02'),('25SW0050','Sheet','WaterColor',NULL,'2025-11-02'),('25WP0001','WaterColor','Plastic',1,'2025-06-06'),('25WP0002','WaterColor','Plastic',17,'2025-06-06'),('25WP0003','WaterColor','Plastic',19,'2025-06-06'),('25WP0004','WaterColor','Plastic',3,'2025-06-06'),('25WP0005','WaterColor','Plastic',NULL,'2025-06-06'),('25WP0006','WaterColor','Plastic',2,'2025-06-06'),('25WP0007','WaterColor','Plastic',NULL,'2025-06-06'),('25WP0008','WaterColor','Plastic',NULL,'2025-06-06'),('25WP0009','WaterColor','Plastic',NULL,'2025-06-06'),('25WP0010','WaterColor','Plastic',NULL,'2025-06-06'),('25WP0011','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0012','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0013','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0014','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0015','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0016','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0017','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0018','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0019','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0020','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0021','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0022','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0023','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0024','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0025','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0026','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0027','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0028','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0029','WaterColor','Plastic',NULL,'2025-08-10'),('25WP0030','WaterColor','Plastic',NULL,'2025-08-10'),('25WS0001','WaterColor','Sheet',14,'2025-08-22'),('25WS0002','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0003','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0004','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0005','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0006','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0007','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0008','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0009','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0010','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0011','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0012','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0013','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0014','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0015','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0016','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0017','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0018','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0019','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0020','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0021','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0022','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0023','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0024','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0025','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0026','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0027','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0028','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0029','WaterColor','Sheet',NULL,'2025-08-22'),('25WS0030','WaterColor','Sheet',NULL,'2025-08-22');
/*!40000 ALTER TABLE `stock_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varbinary(60) NOT NULL,
  `type` enum('admin','user') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'user',
  `failed_attempts` int NOT NULL DEFAULT '0',
  `last_failed_login` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Omkar@admin',_binary '$2b$12$IjurNeZv6L6HWnzH6a/Gd.TbNHlsmmr27kukiAdG5X5Ib5RgmZ5ey','admin',1,'2025-11-01 20:14:32','2025-06-04 11:09:25','2025-11-01 14:44:32'),(2,'Omkar',_binary '$2b$12$GWvwVqbmQTbP9Hsm6lGWgO.nl//ipZuIWE1nNgLqnLXrWjXiT5OOi','user',0,NULL,'2025-06-05 14:17:17','2025-08-23 07:47:47'),(3,'Omkar@a',_binary '$2b$12$.6EEGk4kHtPdaOx9Ho19VuVp3SyvBxxDb1m7QervxpCrDTqulsCL2','admin',0,NULL,'2025-11-01 14:45:16','2025-11-05 14:52:57'),(4,'Omkar@acc',_binary '$2b$12$InHUm4Uhuu08KhrehSKN6OxksJp1MUqZgpQeaeq9eoBvbW25YfZ/S','user',0,NULL,'2025-11-01 14:46:30','2025-11-01 14:46:30');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'omkaroptics'
--

--
-- Dumping routines for database 'omkaroptics'
--
/*!50003 DROP PROCEDURE IF EXISTS `add_stock_items` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_stock_items`(
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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-05 20:29:27
