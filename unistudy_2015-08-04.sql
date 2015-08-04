# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: localhost (MySQL 5.6.24)
# Database: unistudy
# Generation Time: 2015-08-04 14:43:46 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table lectures
# ------------------------------------------------------------

DROP TABLE IF EXISTS `lectures`;

CREATE TABLE `lectures` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `subject_id` int(5) NOT NULL,
  `name` char(255) NOT NULL DEFAULT '',
  `link` char(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `lectures` WRITE;
/*!40000 ALTER TABLE `lectures` DISABLE KEYS */;

INSERT INTO `lectures` (`id`, `subject_id`, `name`, `link`)
VALUES
	(1,1,'오리엔테이션','#'),
	(2,1,'Hello World','#');

/*!40000 ALTER TABLE `lectures` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table post
# ------------------------------------------------------------

DROP TABLE IF EXISTS `post`;

CREATE TABLE `post` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `writer` int(11) NOT NULL,
  `title` char(255) NOT NULL DEFAULT '',
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table subjects
# ------------------------------------------------------------

DROP TABLE IF EXISTS `subjects`;

CREATE TABLE `subjects` (
  `id` int(5) unsigned NOT NULL AUTO_INCREMENT,
  `group` char(255) DEFAULT NULL,
  `name` char(255) NOT NULL DEFAULT '',
  `message` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;

INSERT INTO `subjects` (`id`, `group`, `name`, `message`)
VALUES
	(1,'프로그래밍','Engineering Programming I',''),
	(2,'프로그래밍','Engineering Programming II',''),
	(3,'프로그래밍','Business Programming',''),
	(4,'수학','Calculus I',''),
	(5,'수학','Calculus II',''),
	(6,'수학','Applied Linear Algebra',''),
	(7,'수학','Differential Equation',''),
	(8,'과학','General Biology',''),
	(9,'과학','General Physics I',''),
	(10,'과학','General Physics II',''),
	(11,'과학','General Chemistry I',''),
	(12,'과학','General Chemistry II','');

/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `nickname` char(255) NOT NULL,
  `email` char(255) NOT NULL DEFAULT '',
  `password` char(255) NOT NULL DEFAULT '',
  `verify` int(1) NOT NULL DEFAULT '0',
  `ban` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `nickname`, `email`, `password`, `verify`, `ban`)
VALUES
	(1,'테스트','mu291@unist.ac.kr','99fb2f48c6af4761f904fc85f95eb56190e5d40b1f44ec3a9c1fa319',1,0),
	(8,'인듕','mu29@unist.ac.kr','99fb2f48c6af4761f904fc85f95eb56190e5d40b1f44ec3a9c1fa319',1,0);

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
