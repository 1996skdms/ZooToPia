-- --------------------------------------------------------
-- 호스트:                          j5a602.p.ssafy.io
-- 서버 버전:                        8.0.25-0ubuntu0.20.04.3 - (Ubuntu)
-- 서버 OS:                        Linux
-- HeidiSQL 버전:                  11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- bigdata 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `bigdata` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bigdata`;

-- 테이블 bigdata.hoga 구조 내보내기
CREATE TABLE IF NOT EXISTS `hoga` (
  `ordering` int NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `ask_price` varchar(20) DEFAULT NULL,
  `ask_volume` varchar(30) DEFAULT NULL,
  `bid_price` varchar(20) DEFAULT NULL,
  `bid_volume` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`ordering`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 bigdata.opendart 구조 내보내기
CREATE TABLE IF NOT EXISTS `opendart` (
  `corp_code` varchar(20) NOT NULL,
  `corp_name` varchar(100) DEFAULT NULL,
  `stock_code` varchar(20) DEFAULT NULL,
  `modify_date` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`corp_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 bigdata.scheduler_check 구조 내보내기
CREATE TABLE IF NOT EXISTS `scheduler_check` (
  `date` datetime NOT NULL,
  `is_call` tinyint NOT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 bigdata.stock 구조 내보내기
CREATE TABLE IF NOT EXISTS `stock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) DEFAULT NULL,
  `market` varchar(20) DEFAULT NULL,
  `NAME` varchar(100) DEFAULT NULL,
  `sector` varchar(100) DEFAULT NULL,
  `region` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10467 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 bigdata.stock_data 구조 내보내기
CREATE TABLE IF NOT EXISTS `stock_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) DEFAULT NULL,
  `date` timestamp NULL DEFAULT NULL,
  `open` int DEFAULT NULL,
  `high` int DEFAULT NULL,
  `low` int DEFAULT NULL,
  `close` int DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4639466 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 bigdata.stock_posi_negative 구조 내보내기
CREATE TABLE IF NOT EXISTS `stock_posi_negative` (
  `code` varchar(6) NOT NULL,
  `date` datetime NOT NULL,
  `score` float DEFAULT NULL,
  PRIMARY KEY (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
