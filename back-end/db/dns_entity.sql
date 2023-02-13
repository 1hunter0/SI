/*
 Navicat Premium Data Transfer

 Source Server         : test0
 Source Server Type    : MySQL
 Source Server Version : 80030 (8.0.30)
 Source Host           : localhost:3306
 Source Schema         : test1

 Target Server Type    : MySQL
 Target Server Version : 80030 (8.0.30)
 File Encoding         : 65001

 Date: 13/02/2023 16:27:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dns_entity
-- ----------------------------
DROP TABLE IF EXISTS `dns_entity`;
CREATE TABLE `dns_entity` (
  `dns` varchar(255) NOT NULL,
  `analysis_ip` varchar(255) DEFAULT NULL COMMENT '解析ip',
  `related_url` varchar(255) DEFAULT NULL COMMENT '相关url',
  `severity` tinyint DEFAULT NULL COMMENT '威胁等级',
  `sample` varchar(255) DEFAULT NULL COMMENT '相关样本',
  `confidence` varchar(255) DEFAULT NULL COMMENT '置信度',
  `scene` varchar(255) DEFAULT NULL COMMENT '应用场景',
  `open_source` varchar(255) DEFAULT NULL COMMENT '开源情报',
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `dns_url` (`related_url`),
  KEY `dns_ip` (`analysis_ip`),
  CONSTRAINT `dns_ip` FOREIGN KEY (`analysis_ip`) REFERENCES `ip_entity` (`ip`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `dns_url` FOREIGN KEY (`related_url`) REFERENCES `url_entity` (`url`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
