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

 Date: 13/02/2023 16:37:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ip_alarm_event
-- ----------------------------
DROP TABLE IF EXISTS `ip_alarm_event`;
CREATE TABLE `ip_alarm_event` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `ip_subject` varchar(255) NOT NULL COMMENT '攻击者ip',
  `ip_object` varchar(255) NOT NULL COMMENT '受害者ip',
  `attack_type` varchar(255) DEFAULT NULL COMMENT '攻击类型及编号',
  `dev_info` varchar(255) NOT NULL COMMENT '告警来源设备',
  `hostname` varchar(255) NOT NULL COMMENT '告警来源ip',
  `timestamp` timestamp NOT NULL COMMENT '告警发生时间',
  `attack_stage` varchar(255) DEFAULT NULL COMMENT '攻击阶段',
  `attack_status` varchar(255) DEFAULT NULL COMMENT '攻击状态',
  `dev_category` varchar(255) DEFAULT NULL COMMENT '触发告警的规则类型',
  `dev_rule` varchar(255) DEFAULT NULL COMMENT '触发告警的规则',
  `degree` varchar(255) DEFAULT NULL COMMENT '程度',
  `forbid_status` varchar(255) DEFAULT NULL COMMENT '该请求是否被防火墙阻断',
  `req_method` varchar(255) DEFAULT NULL COMMENT 'http请求方式',
  `threat_phase` varchar(255) DEFAULT NULL COMMENT '威胁的阶段',
  `kill_chain` varchar(255) DEFAULT NULL COMMENT '单个杀伤链',
  `kill_chain_all` varchar(255) DEFAULT NULL COMMENT '全杀伤链',
  `count` int DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  UNIQUE KEY `unique_ipsub_ipobj_attacktype` (`ip_subject`,`ip_object`,`attack_type`),
  KEY `ix_ip_alarm_event_ip_subject` (`ip_subject`),
  KEY `ix_ip_alarm_event_ip_object` (`ip_object`),
  CONSTRAINT `ip_alarm_event_ibfk_1` FOREIGN KEY (`ip_subject`) REFERENCES `ip_entity` (`ip`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ip_alarm_event_ibfk_2` FOREIGN KEY (`ip_object`) REFERENCES `ip_entity` (`ip`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
