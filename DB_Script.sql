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
	`fullname` varchar(50) NOT NULL,
	`card_num` varchar(16) NOT NULL,
	`exp_date` varchar() NOT NULL,
    `cvv` varchar(3) NOT NULL,
    PRIMARY KEY (`id`)
)
ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com');*/