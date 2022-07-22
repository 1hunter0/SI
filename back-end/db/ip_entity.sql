/*
 Navicat MySQL Data Transfer

 Source Server         : test1
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : threat_intelligence

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 20/07/2022 15:24:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ip_entity
-- ----------------------------
DROP TABLE IF EXISTS `ip_entity`;
CREATE TABLE `ip_entity`  (
  `ip` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `country` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  `province` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  `city` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  `isp` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  `latitude` decimal(10, 6) NULL DEFAULT NULL,
  `longitude` decimal(10, 6) NULL DEFAULT NULL,
  PRIMARY KEY (`ip`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ip_entity
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
