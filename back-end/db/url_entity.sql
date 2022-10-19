/*
 Navicat Premium Data Transfer

 Source Server         : test0
 Source Server Type    : MySQL
 Source Server Version : 80030 (8.0.30)
 Source Host           : localhost:3306
 Source Schema         : test_sandbox

 Target Server Type    : MySQL
 Target Server Version : 80030 (8.0.30)
 File Encoding         : 65001

 Date: 19/10/2022 15:51:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for url_entity
-- ----------------------------
DROP TABLE IF EXISTS `url_entity`;
CREATE TABLE `url_entity` (
  `url` varchar(255) NOT NULL,
  `history_dns` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '历史dns',
  `severity` tinyint DEFAULT NULL COMMENT '威胁等级',
  PRIMARY KEY (`url`),
  KEY `dns_url` (`history_dns`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;