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
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `msg` varchar(100) NOT NULL,
  `logtype` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
INSERT INTO `audit_logs` VALUES (2,'Successful Registration for user \'Jeff123\' via username/password at time: 2023-08-14 10:30:21','register'),(3,'Successful registration for user \'Jeff123\' via username/password at time: 2023-08-14 10:30:21','registration'),(4,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:36:02','login'),(5,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:36:02','login'),(6,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:37:23','login'),(7,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:37:23','login'),(8,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:42:02','login'),(9,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:42:02','login'),(10,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:45:01','login'),(11,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:45:01','login'),(12,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:45:47','login'),(13,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:45:47','login'),(14,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:46:15','login'),(15,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:46:15','login'),(16,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:50:31','login'),(17,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:50:31','login'),(18,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:51:21','login'),(19,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 12:51:21','login'),(20,'Successful Registration for user \'Default\' via username/password at time: 2023-08-14 13:54:34','register'),(21,'Unsuccessful registration for user \'Default\' via username/password at time: 2023-08-14 13:55:33','registration'),(22,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:55:56','login'),(23,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:55:57','login'),(24,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:55:57','login'),(25,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:55:57','login'),(26,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:56:28','login'),(27,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:56:28','login'),(28,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:56:40','login'),(29,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:56:40','login'),(30,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:56:41','login'),(31,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:56:41','login'),(32,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:59:12','login'),(33,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:59:12','login'),(34,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 13:59:12','login'),(35,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:09','login'),(36,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:09','login'),(37,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:10','login'),(38,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:10','login'),(39,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:17','login'),(40,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:17','login'),(41,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:17','login'),(42,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:17','login'),(43,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:21','login'),(44,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:21','login'),(45,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:00:22','login'),(46,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:21','login'),(47,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:21','login'),(48,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:21','login'),(49,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:21','login'),(50,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:26','login'),(51,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:26','login'),(52,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:27','login'),(53,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:27','login'),(54,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:49','login'),(55,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:49','login'),(56,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:01:50','login'),(57,'Unsuccessful Login for user \'Jeff12344\' via username/password at time: 2023-08-14 14:10:18','login'),(58,'Unsuccessful Login for user \'Jeff12344\' via username/password at time: 2023-08-14 14:10:28','login'),(59,'Successful Registration for user \'NewUser\' via username/password at time: 2023-08-14 14:11:39','register'),(60,'Successful registration for user \'NewUser\' via username/password at time: 2023-08-14 14:11:39','registration'),(61,'Successful Registration for user \'NewJeff\' via username/password at time: 2023-08-14 14:12:41','register'),(62,'Successful registration for user \'NewJeff\' via username/password at time: 2023-08-14 14:12:41','registration'),(63,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:34:17','login'),(64,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:34:17','login'),(65,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:36:26','login'),(66,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:36:26','login'),(67,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 14:39:59','login'),(68,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 15:19:46','login'),(69,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 15:22:03','login'),(70,'Successful Login for user \'Jeff123\' via username/password at time: 2023-08-14 15:22:03','login'),(71,'Successful Registration for user \'PreUser\' via username/password at time: 2023-08-14 16:00:00','register'),(72,'Unsuccessful registration for user \'PreUser\' via username/password at time: 2023-08-14 16:01:17','registration'),(73,'Unsuccessful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:03:57','login'),(74,'Unsuccessful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:03:57','login'),(75,'Unsuccessful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:03:58','login'),(76,'Unsuccessful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:03:58','login'),(77,'Unsuccessful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:04:08','login'),(78,'Unsuccessful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:04:08','login'),(79,'Unsuccessful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:04:09','login'),(80,'Unsuccessful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:04:09','login'),(81,'Successful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:04:43','login'),(82,'Successful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:04:43','login'),(83,'Unsuccessful Login for user \'T4Class\' via username/password at time: 2023-08-14 16:06:52','login'),(84,'Unsuccessful Login for user \'T4Class\' via username/password at time: 2023-08-14 16:07:27','login'),(85,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:07','login'),(86,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:07','login'),(87,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:08','login'),(88,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:08','login'),(89,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:18','login'),(90,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:19','login'),(91,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:19','login'),(92,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:19','login'),(93,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:42','login'),(94,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:43','login'),(95,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:08:43','login'),(96,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:10:55','login'),(97,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:10:56','login'),(98,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:10:56','login'),(99,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:10:56','login'),(100,'Successful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:11:16','login'),(101,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:18:08','login'),(102,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:18:08','login'),(103,'Unsuccessful Login for user \'Jeff123\' via username/password at time: 2023-08-14 16:18:08','login'),(104,'Successful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:18:42','login'),(105,'Successful Login for user \'PreUser\' via username/password at time: 2023-08-14 16:19:35','login');
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

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
  `budget` varchar(4) DEFAULT '0',
  `user_id` varchar(2) NOT NULL,
  PRIMARY KEY (`card_ID`),
  KEY `user_id_idx` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card_info`
--

LOCK TABLES `card_info` WRITE;
/*!40000 ALTER TABLE `card_info` DISABLE KEYS */;
INSERT INTO `card_info` VALUES (36,'Jeff Card','gAAAAABkxa2jf5yHdi3FzseSKEmOO6RAtqmkCpuUiWg1C7kHvA7A6MosU7CWjN7nGPtPkjhYL2crFkriYqLp5DkopUfsOPr06BRw749IWmvOZLR7ZCBjHyI=','2025/11','gAAAAABkxa2jrG_L0iLmIr_ULzbsN6HCwXHdkYQkzS5DGZBLN_t2KXwZf5uk95wrafYosUC87TPsyqENtyJ4fwgrL6UxWkBaZw==','10','55'),(37,'Jeff Neww','gAAAAABkxa3F7sX3syWd_8gI4gi7iswMHp4NEMrQMQYwkNaZcWh_q6LOKM0_fpI_yXlilbGX1z7AAW4z82j9StvLS56cKuuOv2xJz4IzN2Ly0EGkOVF5MXo=','2025/05','gAAAAABkxa3FOxBH2OmVYpriRrDiRafMit7NCydLCEy59fAXEll63hGKKnpBxVmhQPxHEPrRHfYYvrFNF29NxQRZN_lXPb169Q==','10','55'),(38,'Jeff Card','gAAAAABk2a-NpoNWdLlwyQpLbnFx3unh9HCcEy7jWSmVYclgj-VzRE1s78-0qChkpY6OAc9SvQrdgbnYcm_MD4evI4n0gZuhV_s0kLEiC7EBpSfxma9xHxY=','2025/05','gAAAAABk2a-NNpbyGR0sWyAJbJYr2qeT26xsCuJoSJE1lvk5nfxgZ4FOTkN2Z9bdiEI3mR3eQkt2JzH7cCeZv298IgCYzooJvQ==','100','58'),(39,'Olfsen Card','gAAAAABk2eA05BCzzhQ0fXo4hC86KNuU5XQpJxxRKJASoyhUlHDkUiDt6zGQTNsoPdRirgXkFq_K7Xj9y-OA_cSUYNuk9hXXhpaZtduXdK88MCDN-CjOTwE=','2020/11','gAAAAABk2eA0jlrgJMXBNIZ38ALkaAIOBcK6MojZpx85O18smjaffR2yaLmmq1TAN65N-gUr8z0HO-9-UBF-f3kWd9rGQNoi0Q==','100','62');
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
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `card_num` varchar(100) NOT NULL,
  `cost` varchar(4) NOT NULL,
  `transaction` varchar(100) NOT NULL,
  `user_id` varchar(2) NOT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,'1111111111111111','20','new1','58'),(2,'1111111111111111','5','1=1;--','58'),(3,'1111111111111111','5','<script>alert(0)<script>\r\n','58'),(4,'1234123412341234','20','<script> alert(0) </script>','62');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
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
  `google_id` varchar(50) DEFAULT NULL,
  `securityquestion` varchar(100) NOT NULL,
  `securityanswer` varchar(100) NOT NULL,
  PRIMARY KEY (`user_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (58,'Jeff123','$2b$12$9rJGVWbEzR9.YwpdU4dvZuEo1UdSD2OOUWI3UeioPEIh55EqxRfr2','gAAAAABk2ZG9WgSZiTnkCQug14n3T0MCNxC3y1UjgfHJzLGlQhKAcQi0JPZyIKEo5k8WW4r17BXrVGBMbT_uzIcWklJERBGhDfhJ1MovCKcnhDrMliS6NQY=','+6589038239','0','0','0','Q1: Will I play Genshin Impact?','No'),(59,'Default','$2b$12$2II/ZaBGVbkTXyGV6whxhOhUBZy9eKSiUJZPuq24OD4Otr2AL9A6K','gAAAAABk2cGa7-A1ZKsJ7hk79GDnI8nebFXKuPHoDGqYxNWqN3qAeHPyNL_w3Kz9yrFvjyPEQmrdYTa0vRBiNWLTU6X5z2Wrag==','+6583098239','0','0','0','Q1: Will I play Genshin Impact?','null'),(60,'NewUser','$2b$12$JzJfGJ4rP2IufXJA18bwPej3ZRuhrpJGkNeIDhZFpQce.FpUoXDmO','gAAAAABk2cWbFVYLTGcCh3Un0gj7xO9gfk2-2pXq0K4345Plcv3pF0rIxrlkpLU0esQmHGtwzB-1KIOYWOg9sdY-4TaPLLfyL5vDhjTx_fSFb3Itdsg_e7s=','+6589038239','0','0','0','Q1: Will I play Genshin Impact?','No'),(61,'NewJeff','$2b$12$XBSbw2OTB5nGMvrWpPx4iOtqi/IqK7OY14xdPz2.X4bImVNAGpZW2','gAAAAABk2cXZ7k3gjCWpVA1UcHNamtIZRIeesac05T2w29qIeAHagR523hL-_kKs97CMChzoNibQMNcDfZMXud1qzvq3_adDOg==','+6589038239','0','0','0','Q1: Will I play Genshin Impact?','No'),(62,'PreUser','$2b$12$kaVdvldXwR5rDdwrPBqTeOA8/e0ZMJ8T9DDHQvMhh9x63/cQ9gUEy','gAAAAABk2d8A95pHpqr2op1Cjh86N__5eDBUUlJ8zJvonW8QmsszX3vTNRcazjpEF8xoxyU74yWMo0BMgtFEoKWO-QJd2_TsEHfiqV1BaC2gUo0ZYmzuxxM=','+6589038239','2','0','0','Q2: What is 2+2?','4'),(63,'Olfsen V','$2b$12$2KBJ6o8rUJgHBKjA3ldqy.uKnhSay0GMTSv8uC8EkQScdtg9CU.JG','gAAAAABk2NL8ZhwyQuPZUo6a6rvNfejC9c51J51GiTAm6xVizxOWxliQofE11vCNVEn52P2DtAGRpm7EiaGgHdo5M2QTOcUMiw==','+6583098239','0','0','106069191997022263462','Q2: What is 2+2?','4');
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

-- Dump completed on 2023-08-15 22:29:23
