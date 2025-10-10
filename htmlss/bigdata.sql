-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: bigdatahackaton
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `datamap`
--

DROP TABLE IF EXISTS `datamap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datamap` (
  `item` text,
  `time` int DEFAULT NULL,
  `amount` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datamap`
--

LOCK TABLES `datamap` WRITE;
/*!40000 ALTER TABLE `datamap` DISABLE KEYS */;
INSERT INTO `datamap` VALUES ('Cassava',2019,1530000),('Maize',2020,2870000),('Beans',2021,1945000),('Rice',2019,2100000),('Cassava',2020,1650000),('Maize',2021,3200000),('Beans',2019,1780000),('Rice',2021,2250000),('Cassava',2021,1725000),('Maize',2019,2950000);
/*!40000 ALTER TABLE `datamap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datasetx`
--

DROP TABLE IF EXISTS `datasetx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datasetx` (
  `item` text,
  `time` int DEFAULT NULL,
  `amount` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datasetx`
--

LOCK TABLES `datasetx` WRITE;
/*!40000 ALTER TABLE `datasetx` DISABLE KEYS */;
INSERT INTO `datasetx` VALUES ('Cassava',2020,1000000),('Maize',2020,3000000),('Beans',2020,2200000),('Cassava',2021,1800000),('Maize',2021,2800000),('Beans',2021,2000000);
/*!40000 ALTER TABLE `datasetx` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `export_commodities`
--

DROP TABLE IF EXISTS `export_commodities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `export_commodities` (
  `period` text,
  `2020Q1` double DEFAULT NULL,
  `2020Q2` double DEFAULT NULL,
  `2020Q3` double DEFAULT NULL,
  `2020Q4` double DEFAULT NULL,
  `2021Q1` double DEFAULT NULL,
  `2021Q2` double DEFAULT NULL,
  `2021Q3` double DEFAULT NULL,
  `2021Q4` double DEFAULT NULL,
  `2022Q1` double DEFAULT NULL,
  `2022Q2` double DEFAULT NULL,
  `2022Q3` double DEFAULT NULL,
  `2022Q4` double DEFAULT NULL,
  `2023Q1` double DEFAULT NULL,
  `2023Q2` double DEFAULT NULL,
  `2023Q3` double DEFAULT NULL,
  `2023Q4` double DEFAULT NULL,
  `2024Q1` double DEFAULT NULL,
  `2024Q2` double DEFAULT NULL,
  `2024Q3` double DEFAULT NULL,
  `2024Q4` double DEFAULT NULL,
  `2025Q1` double DEFAULT NULL,
  `2025Q2` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `export_commodities`
--

LOCK TABLES `export_commodities` WRITE;
/*!40000 ALTER TABLE `export_commodities` DISABLE KEYS */;
INSERT INTO `export_commodities` VALUES ('Food and live animals',59.54,49.82,64.96,67.44,62.84,81.71,83.61,109.02,72.79,69.36,95.68,117.08,106.37,74.62,89.38,103.81,76.21,73.54,99.17,103.12,82.55,96.99),('Beverages and tobacco',0.07,0.02,0.02,0.18,0.06,0.12,0.2,0.14,0.1,0.05,0.54,0.29,0.21,0.34,0.26,0.33,1.99,0.08,0.08,0.1,1.19,2.84),('Crude materials, inedible, except fuels ',24.59,18.05,23.78,22.57,26.45,38.95,43.64,50.72,50.85,58.07,49.84,54.99,59.68,58.59,62.23,51.19,56.5,56.38,67.91,58.76,60.17,83.04),('Mineral fuels, lubricants and related materials',0.09,0.11,0.14,0.16,0.1,0.17,0.09,0.18,0.27,0.17,0.3,0.36,0.74,0.6,1.14,1.71,0.27,0.78,0.98,0.94,0.85,0.64),('Animals and vegetable oils, fats & waxes',0.08,0.1,0.13,0.13,0.06,0.33,0.46,1.25,0.9,0.56,2.46,2.46,0.72,2.41,2.87,1.11,2.87,4.56,12.04,23.4,12.85,23.9),('Chemicals & related products, n.e.s.',1.32,1.22,1.62,1.61,2.05,3.83,2.72,2.09,3.14,4.59,2.85,4.21,4.4,3.58,3.7,4.51,4.17,4.87,4.88,4.88,6.39,4.98),('Manufactured goods classified chiefly by material',7.57,6.76,11.84,17.6,14.83,13.62,19.65,18.16,25.39,28.07,34.15,26.81,29.52,28.76,28.61,24.63,27.19,35.35,30.73,34.87,32.25,38.75),('Machinery and transport equipment',4.74,1.81,2.27,2.45,1.87,4.95,4.46,3.85,15.27,2.73,3.83,4.47,5.36,4.65,3.14,2.84,4.06,1.49,7.07,4.9,2.54,3.78),('Miscellaneous manufactured articles',2.76,2.26,7.02,3.77,3.11,4.33,6.1,8.41,8.37,7.76,8.31,9.73,4.86,8.5,8.77,6.35,4.98,9.74,9.46,8.32,5.7,8.04),('Other commodities & transactions, n.e.s',106,121.63,294.22,124.34,50.46,93.47,102.51,116.74,116.5,160.19,144.61,134.45,190.28,302.69,188.01,202.62,253.37,350.85,434.69,438.15,276.31,83.09);
/*!40000 ALTER TABLE `export_commodities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exports_share`
--

DROP TABLE IF EXISTS `exports_share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exports_share` (
  `country` text,
  `share` double DEFAULT NULL,
  `value` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exports_share`
--

LOCK TABLES `exports_share` WRITE;
/*!40000 ALTER TABLE `exports_share` DISABLE KEYS */;
INSERT INTO `exports_share` VALUES ('United Arab Emirates',28.3,97.94),('Congo, The Democratic Republic Of',20.19,69.86),('China',11.81,40.88),('Belgium',4.16,14.4),('Luxembourg',3.94,13.64),('United Kingdom',2.76,9.55),('United States',2.76,9.55),('Others',26.07,90.22);
/*!40000 ALTER TABLE `exports_share` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exportss`
--

DROP TABLE IF EXISTS `exportss`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exportss` (
  `period` text,
  `exports` double DEFAULT NULL,
  `imports` double DEFAULT NULL,
  `re-imports` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exportss`
--

LOCK TABLES `exportss` WRITE;
/*!40000 ALTER TABLE `exportss` DISABLE KEYS */;
INSERT INTO `exportss` VALUES ('2020Q1',206.76,911.37,82.25),('2020Q2',201.78,692.71,62.65),('2020Q3',405.99,982.23,79.36),('2020Q4',240.25,894.49,89.91),('2021Q1',161.83,769.74,108.56),('2021Q2',241.49,961.44,114.99),('2021Q3',263.45,1008.68,116.57),('2021Q4',310.56,1079.66,129.39),('2022Q1',293.58,1034.54,150.66),('2022Q2',331.55,1348.03,161.74),('2022Q3',342.56,1481.22,201.15),('2022Q4',354.84,1281.21,190.42),('2023Q1',402.14,1476.51,156.25),('2023Q2',484.74,1571.09,154.52),('2023Q3',388.11,1581.81,173),('2023Q4',399.11,1486.93,159.55),('2024Q1',431.61,1410.52,173.17),('2024Q2',537.64,1568.97,164),('2024Q3',667,1751.57,184.56),('2024Q4',677.45,1629.39,177.29),('2025Q1',480.82,1379.05,135.39),('2025Q2',346.04,1247.39,142.41);
/*!40000 ALTER TABLE `exportss` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imports_commodities`
--

DROP TABLE IF EXISTS `imports_commodities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imports_commodities` (
  `period` text,
  `2020Q1` double DEFAULT NULL,
  `2020Q2` double DEFAULT NULL,
  `2020Q3` double DEFAULT NULL,
  `2020Q4` double DEFAULT NULL,
  `2021Q1` double DEFAULT NULL,
  `2021Q2` double DEFAULT NULL,
  `2021Q3` double DEFAULT NULL,
  `2021Q4` double DEFAULT NULL,
  `2022Q1` double DEFAULT NULL,
  `2022Q2` double DEFAULT NULL,
  `2022Q3` double DEFAULT NULL,
  `2022Q4` double DEFAULT NULL,
  `2023Q1` double DEFAULT NULL,
  `2023Q2` double DEFAULT NULL,
  `2023Q3` double DEFAULT NULL,
  `2023Q4` double DEFAULT NULL,
  `2024Q1` double DEFAULT NULL,
  `2024Q2` double DEFAULT NULL,
  `2024Q3` double DEFAULT NULL,
  `2024Q4` double DEFAULT NULL,
  `2025Q1` double DEFAULT NULL,
  `2025Q2` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imports_commodities`
--

LOCK TABLES `imports_commodities` WRITE;
/*!40000 ALTER TABLE `imports_commodities` DISABLE KEYS */;
INSERT INTO `imports_commodities` VALUES ('Food and live animals',107.3,88.6,104.65,122.23,108.21,134.28,133.45,139.44,134.54,186.66,196.1,311.28,264.48,228.98,254.36,290.33,202.46,238.2,237.17,234.57,203.57,228.34),('Beverages and tobacco',7.6,6.59,7.4,12.45,6.91,10.65,11.79,14.31,17.32,19.23,24.56,24.19,27.88,25.2,29.62,26.73,21.91,24.97,28.98,27.49,29.24,77.33),('Crude materials, inedible, except fuels ',20.57,21.54,18.03,20.2,17.9,20.45,31.07,28.8,30.09,39.83,29.12,31.57,39.37,32.81,41.14,39.2,33.55,31.87,44.33,42.68,28.19,36.58),('Mineral fuels, lubricants and related materials',147.9,75.21,61.35,70.61,58.43,104.32,117.64,130.37,147.49,167.27,265.67,204.88,190.83,161.79,157.62,174.68,184.27,195.46,202.08,190.53,178.01,162.79),('Animals and vegetable oils, fats & waxes',32.74,23.02,26.68,28.2,29.65,36.47,47.73,64.15,53.85,47.97,58.58,62.37,63.51,54,52.95,57.27,38.87,46.33,53.28,55.92,51.99,74.51),('Chemicals & related products, n.e.s.',110.76,80,105.99,107.36,102.72,113.03,128.95,121.89,115.79,146.51,160.08,153,139.71,136.9,149.46,130.47,120.46,137.98,146.93,135.39,129.69,137.71),('Manufactured goods classified chiefly by material',132.66,104.35,172.34,145.3,117.19,163.53,168.09,185.23,178.27,201.57,220.84,251.53,198.96,215.32,254.21,216.87,162.6,171.55,218.56,215.13,191.11,172.33),('Machinery and transport equipment',185.09,133.96,144.05,190.02,213.52,195.89,196.29,183.72,182.64,194.81,249.91,282.28,256.27,318.8,320.33,258.63,278.43,286.41,253.86,238.86,305.46,249.02),('Miscellaneous manufactured articles',63.55,41.45,56.35,77.5,55.01,87.49,75.18,97.11,76.93,91.89,141.49,96.72,87.09,87.75,107.35,87.39,92.03,88.35,87.25,92.66,73.48,85.1),('Other commodities & transactions, n.e.s',103.21,117.98,285.39,120.61,60.2,95.33,98.51,114.65,118.45,161.97,154.45,75.51,208.41,309.54,214.76,205.37,275.94,347.84,479.12,396.16,188.31,23.67);
/*!40000 ALTER TABLE `imports_commodities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imports_share`
--

DROP TABLE IF EXISTS `imports_share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imports_share` (
  `country` text,
  `share` double DEFAULT NULL,
  `value` double DEFAULT NULL,
  `change1` double DEFAULT NULL,
  `change2` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imports_share`
--

LOCK TABLES `imports_share` WRITE;
/*!40000 ALTER TABLE `imports_share` DISABLE KEYS */;
INSERT INTO `imports_share` VALUES ('China',22.1,275.63,-18.58,-1.88),('Tanzania, United Republic Of',14.35,178.94,18.27,13.13),('India',8.64,107.83,-6.76,-28.83),('Kenya',6.27,78.17,-42.24,-68.1),('United Arab Emirates',5.65,70.45,-13.12,-26.55),('Uganda',5.33,66.5,12.46,16.99);
/*!40000 ALTER TABLE `imports_share` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trade20_25q2`
--

DROP TABLE IF EXISTS `trade20_25q2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trade20_25q2` (
  `period` text,
  `2020Q1` double DEFAULT NULL,
  `2020Q2` double DEFAULT NULL,
  `2020Q3` double DEFAULT NULL,
  `2020Q4` double DEFAULT NULL,
  `2021Q1` double DEFAULT NULL,
  `2021Q2` double DEFAULT NULL,
  `2021Q3` double DEFAULT NULL,
  `2021Q4` double DEFAULT NULL,
  `2022Q1` double DEFAULT NULL,
  `2022Q2` double DEFAULT NULL,
  `2022Q3` double DEFAULT NULL,
  `2022Q4` double DEFAULT NULL,
  `2023Q1` double DEFAULT NULL,
  `2023Q2` double DEFAULT NULL,
  `2023Q3` double DEFAULT NULL,
  `2023Q4` double DEFAULT NULL,
  `2024Q1` double DEFAULT NULL,
  `2024Q2` double DEFAULT NULL,
  `2024Q3` double DEFAULT NULL,
  `2024Q4` double DEFAULT NULL,
  `2025Q1` double DEFAULT NULL,
  `2025Q2` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trade20_25q2`
--

LOCK TABLES `trade20_25q2` WRITE;
/*!40000 ALTER TABLE `trade20_25q2` DISABLE KEYS */;
INSERT INTO `trade20_25q2` VALUES ('exports',206.76,201.78,405.99,240.25,161.83,241.49,263.45,310.56,293.58,331.55,342.56,354.84,402.14,484.74,388.11,399.11,431.61,537.64,667,677.45,480.82,346.04),('imports',911.37,692.71,982.23,894.49,769.74,961.44,1008.68,1079.66,1034.54,1348.03,1481.22,1281.21,1476.51,1571.09,1581.81,1486.93,1410.52,1568.97,1751.57,1629.39,1379.05,1247.39),('re-imports',82.25,62.65,79.36,89.91,108.56,114.99,116.57,129.39,150.66,161.74,201.15,190.42,156.25,154.52,173,159.55,173.17,164,184.56,177.29,135.39,142.41);
/*!40000 ALTER TABLE `trade20_25q2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'kick','o'),(2,'slayer','scrypt:32768:8:1$SRamJ2euJYtLAq65$67bd3e3b94ec00a4afd0ae2bbc5c2db9f1fa559d82b6a0f078df2a5cda08cca8cb1837b99a41a624950c1540753beb3e43effce5bab97f797c63f75b7913c400'),(5,'hugor','scrypt:32768:8:1$s9KwCk0IE1hAnfil$6f847bf620e3352adb609a7f288ec2df776776447e93c4c07b26c5f1afe656d28117abc930671b4438babac9ba2889f5599174c6212364705c7e6b0b47d5c0b5');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-10  7:43:37
