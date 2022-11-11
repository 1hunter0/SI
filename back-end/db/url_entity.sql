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

 Date: 11/11/2022 20:16:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for url_entity
-- ----------------------------
DROP TABLE IF EXISTS `url_entity`;
CREATE TABLE `url_entity` (
  `url` varchar(255) NOT NULL,
  `history_dns` varchar(255) DEFAULT NULL COMMENT '历史dns',
  `severity` tinyint DEFAULT NULL COMMENT '威胁等级',
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
