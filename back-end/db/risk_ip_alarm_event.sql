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

 Date: 13/02/2023 16:28:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for risk_ip_alarm_event
-- ----------------------------
DROP TABLE IF EXISTS `risk_ip_alarm_event`;
CREATE TABLE `risk_ip_alarm_event` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `ip_subject` varchar(255) NOT NULL COMMENT '攻击者ip',
  `ip_object` varchar(255) NOT NULL COMMENT '受害者ip',
  `attack_type` varchar(255) DEFAULT NULL COMMENT '攻击类型及编号',
  `reason` varchar(255) DEFAULT NULL COMMENT '高风险原因',
  PRIMARY KEY (`event_id`),
  UNIQUE KEY `risk_unique_ipsub_ipobj_attacktype` (`ip_subject`,`ip_object`,`attack_type`),
  KEY `ix_risk_ip_alarm_event_ip_object` (`ip_object`),
  KEY `ix_risk_ip_alarm_event_ip_subject` (`ip_subject`),
  CONSTRAINT `risk_ip_alarm_event_ibfk_1` FOREIGN KEY (`ip_subject`) REFERENCES `ip_entity` (`ip`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `risk_ip_alarm_event_ibfk_2` FOREIGN KEY (`ip_object`) REFERENCES `ip_entity` (`ip`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
