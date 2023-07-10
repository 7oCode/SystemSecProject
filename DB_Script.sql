CREATE DATABASE IF NOT EXISTS `sys_sec` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `sys_sec`;
CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`username` varchar(50) NOT NULL,
	`password` varchar(255) NOT NULL,
	`email` varchar(100) NOT NULL,
	PRIMARY KEY (`id`)
);
CREATE TABLE IF NOT EXISTS `card_info`(
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`card_no` varchar(50) NOT NULL,
	`first_name` varchar(255) NOT NULL,
	`last_name` varchar(100) NOT NULL,
    `exp_date` date NOT NULL,
    `cvv` varchar(3) NOT NULL,
	PRIMARY KEY (`id`)
)
 ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
