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

DROP TABLE IF EXISTS `card_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card_info` (
  `card_ID` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(50) NOT NULL,
  `card_num` varchar(255) NOT NULL,
  `exp_date` varchar(7) NOT NULL,
  `cvv` varchar(255) NOT NULL,
  `budget` int DEFAULT '0',
  `user_id` int NOT NULL,
  PRIMARY KEY (`card_ID`),
  KEY `user_id_idx` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card_info`
--

LOCK TABLES `card_info` WRITE;
/*!40000 ALTER TABLE `card_info` DISABLE KEYS */;
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

LOCK TABLES `pwd_hist` WRITE;
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
  PRIMARY KEY (`user_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (37,'Default','$2b$12$.yDDrmzYty6mdz.au1jIRuXwadLwhHvLu0JlaAgiaev0BvP7txhSC','gAAAAABks60Y6Umrdnb6-IOOLAcdwz18HPgRGsE4WjcfReG639XJOlASWYISaAxHK97qeadaCMDmf_-2IK1m_fRAQ81C3ColTqQXYjDwrzNrblC8E7rw1No=','+6597442152','0','0'),(42,'NewUser','$2b$12$mcmLyymgLOQDeE2AsVJC6uOKHbV0de4C1k8tC50SCC9OetYd579sm','gAAAAABktKvZxc6WhHI9j2yq4UmjcBNLiIwYCCCFEaPX0_4Lfi9iCZXGFBmD4reDS0-1OanUyS8z7tzHkdd6sOr6xXk5biwowg==','+6583098239','0','0'),(43,'Another123','$2b$12$uxi1bU6iOqG.DyfVXARCAeAR2mL7Nq6G9bPpA4xwMdpsdUrSv2Chy','gAAAAABktLFjG3_CnMCn03zP31H08wDCoHuAlptefuA0JHjwaqra5v91Zzqfn5Bk9CzgmBG8wGFCpNnMIvBKvYElTFBMJA-kri1nhGPg3J-lLPLe5t_ytDA=','+6597442152','0','0'),(44,'AnotherUse','$2b$12$P3gDv88xLWaEzXDFTp/F9OQDDThA9vlEN9wAkaOAYYXamCmAyawMu','gAAAAABktLHwZ7uUbxxfBehV0qpjaAqiktGQbYfipqjWlfYDgOJOuXPkBqreduaW_ypxU-5jc-l84ashwomhgUT5nRB6JbE7lA==','+6589038239','0','0'),(45,'JeffNew','$2b$12$RhuRBXf.CU1lWGGQ/M8qnOYnVrDUQvTOzuAnP.33utsh7noCqWevi','gAAAAABktMtrrV4I9pKe9eJQwkB7n6aK6xHCHLP0N2mpvy3FHvQncd84QMhhv8nU6EnP_2-uY462eVgtyxL1Y1tig8_y9pOO8VjZ3OXKmByqMW00ITy0MtM=','+6589038239','0','0'),(46,'TestUser','$2b$12$CLSw9cNrQRX8VpV7HJevHeLiuVWowqReRahJCI6dFlGbJJS.4TZxa','gAAAAABktNwcil7Gtlt-xuqG-ONqA-R3hvzlSx2qZpYjh6gGFRiREslzfFg5EdIlZTdezN6JdCztuUiAkK9_8rd2XnzTBe5weBxCWxfXAN9ZnsPcv87WMWs=','+6589038239','0','0');
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

-- Dump completed on 2023-07-21 19:55:46
