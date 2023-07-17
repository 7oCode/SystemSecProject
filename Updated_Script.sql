CREATE DATABASE  IF NOT EXISTS `sys_sec` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sys_sec`;
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
  `id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(50) NOT NULL,
  `card_num` varchar(255) NOT NULL,
  `exp_date` varchar(7) NOT NULL,
  `cvv` varchar(255) NOT NULL,
  `budget` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card_info`
--

LOCK TABLES `card_info` WRITE;
/*!40000 ALTER TABLE `card_info` DISABLE KEYS */;
INSERT INTO `card_info` VALUES (6,'Jeff Card','gAAAAABkrMHVlb2moEXjWg26_2XW0n6i-csWDA3t8NahJG1rO9Q-VslbcQBIMF7VTm8f0nPX_3jx4YAWZAhTlAVdYjsQiO5B9NuGGvzaJUAHiOsLvxS6wjE=','2025/05','gAAAAABkrMHVotZbFy7PHyY8WHQztVJVq7pBGIoNonbSDU5DdoPLaU5Ywr5UdlqnLlt3PZPho0-1VGrABKpCmXfhtVvTtMNZVQ==',NULL);
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
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
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
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_no` varchar(11) NOT NULL,
  `rate_limit` varchar(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (37,'Default','$2b$12$.yDDrmzYty6mdz.au1jIRuXwadLwhHvLu0JlaAgiaev0BvP7txhSC','gAAAAABks60Y6Umrdnb6-IOOLAcdwz18HPgRGsE4WjcfReG639XJOlASWYISaAxHK97qeadaCMDmf_-2IK1m_fRAQ81C3ColTqQXYjDwrzNrblC8E7rw1No=','+6597442152','0'),(38,'NewUser','$2b$12$a6UIfurjhi21jZxFbgy01emeAHafaADfo2VkJTYlgDZv4WzkhICZu','gAAAAABks7N88ENsPEwpsO1-3mx5Ow2T5OyR5K99D0jjjzwwUKiNXfnx3vnkhu9-jgx7HZm026H_itaX_fgbWqP1BnHBazxy_A==','+6589038239','0'),(39,'JeffNew','$2b$12$7rgvknz1xqjvFQ7ZWo4mkOE0zk4p7LkETpOREz3D87R0asSXdA/lO','gAAAAABktKANXe_euZII1neVVDRSB7RcNILs9j1VG0plwOHtIppFrc0YNo5HxU4rXuaSC3zubLUZcu6ZZuRo_i3iOnBTmIDukQ==','+6589038239','0');
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

-- Dump completed on 2023-07-17 10:23:43
