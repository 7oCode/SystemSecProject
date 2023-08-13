-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: sys_sec
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `card_info`
--
LOCK TABLES card_info WRITE;
DROP TABLE IF EXISTS `card_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card_info` (
  `card_ID` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(50) NOT NULL,
  `card_num` varchar(255) NOT NULL,
  `exp_date` varchar(7) NOT NULL,
  `cvv` varchar(255) NOT NULL,
  `budget` varchar(4) DEFAULT '0',
  `user_id` varchar(2) NOT NULL,
  PRIMARY KEY (`card_ID`),
  KEY `user_id_idx` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card_info`
--

LOCK TABLES `card_info` WRITE;
/*!40000 ALTER TABLE `card_info` DISABLE KEYS */;
INSERT INTO `card_info` VALUES (36,'Jeff Card','gAAAAABkxa2jf5yHdi3FzseSKEmOO6RAtqmkCpuUiWg1C7kHvA7A6MosU7CWjN7nGPtPkjhYL2crFkriYqLp5DkopUfsOPr06BRw749IWmvOZLR7ZCBjHyI=','2025/11','gAAAAABkxa2jrG_L0iLmIr_ULzbsN6HCwXHdkYQkzS5DGZBLN_t2KXwZf5uk95wrafYosUC87TPsyqENtyJ4fwgrL6UxWkBaZw==','10','55'),(37,'Jeff Neww','gAAAAABkxa3F7sX3syWd_8gI4gi7iswMHp4NEMrQMQYwkNaZcWh_q6LOKM0_fpI_yXlilbGX1z7AAW4z82j9StvLS56cKuuOv2xJz4IzN2Ly0EGkOVF5MXo=','2025/05','gAAAAABkxa3FOxBH2OmVYpriRrDiRafMit7NCydLCEy59fAXEll63hGKKnpBxVmhQPxHEPrRHfYYvrFNF29NxQRZN_lXPb169Q==','10','55');
/*!40000 ALTER TABLE `card_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pwd_hist`
--

DROP TABLE IF EXISTS `pwd_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pwd_hist` (
  `hist_id` int NOT NULL AUTO_INCREMENT,
  `pwd_histcol` varchar(100) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`hist_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pwd_hist`
--

LOCK TABLES `pwd_hist` usersWRITE;
/*!40000 ALTER TABLE `pwd_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `pwd_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_ID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_no` varchar(11) NOT NULL,
  `rate_limit` varchar(1) NOT NULL DEFAULT '0',
  `otp_attempt` varchar(1) NOT NULL DEFAULT '0',
  `google_id` varchar(50),
  `securityquestion` varchar(100) NOT NULL,
  `securityanswer` varchar(100) NOT NULL,
  PRIMARY KEY (`user_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Audit Log Table
--
DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE `audit_logs`(
    `id` int(11) NOT NULL auto_increment ,
    `msg` varchar(100) NOT NULL ,
    `type` varchar(50) NOT NULL ,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB auto_increment = 2 default charset =utf8;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
-- INSERT INTO `users` VALUES (53,'Jeff1234','$2b$12$cREQQza9kUw6cbdGniBZNeuIiiqDHrFNd15BE6yvjdB4AN0BRnJ4C','gAAAAABkxMr95MVocKhWowtbGuBtoMyHTM-EjUGuk81DC-xZSRHfSBh8LucfaPR4iVFH76ukEditydAr7X9MFNlHaDcF49Z2Hg==','+6583098239','2','0'),(55,'Jeff123','$2b$12$0z6a9AnPOj9TTcOh8koG.O31Pxk2BEqLuduriaoxDQxsTwAwLvt4W','gAAAAABkxQBR11ARl2SdS-A82ZEC81zqEdY_6yLudN1NMcf9_V2VkZ4vB1yY6xAZMJlV2_gq8T4t8ZuKrmrSvMZoWrqQJSd9FA==','+6583098239','0','0'),(56,'Vmuser1234','$2b$12$zouVuw6FM8on9ZsdHkuOWu3e2b40pXBJTEazeeuhjSxrP2VkUQ3Ka','gAAAAABkxQhNvOp4nib-oSOBNqAbILVLyVX3u_q1e2bdCK9HScKxqaaKBbm-fO9jLXJ8acvIg1W4bwbBib94HwEcj8YxkT9ohA==','+6583098239','0','0'),(57,'Default','$2b$12$D/zHQKSVo2n2gpdUHrVvP.XRLTwjSoQGZqZH03Pgp1fyyE3dcgC4K','gAAAAABk0iu-SFypV0daZvTaQt_BkzZ3S6CcTiku70Aj5OTxIXtccblQxgK9dX2QGipOGMLiOYN0U6r8fC3g_QUx-EJw2btY1w==','+6583098239','0','0');
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

-- Dump completed on 2023-08-10 21:42:56
