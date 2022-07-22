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

 Date: 20/07/2022 15:24:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ip_alarm_event
-- ----------------------------
DROP TABLE IF EXISTS `ip_alarm_event`;
CREATE TABLE `ip_alarm_event`  (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `ip_subject` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '攻击者ip',
  `ip_object` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '受害者ip',
  `dev_info` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '告警来源设备',
  `hostname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '告警来源ip',
  `timestamp` timestamp NOT NULL COMMENT '告警发生时间',
  `attack_stage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '攻击阶段',
  `attack_status` int NULL DEFAULT NULL COMMENT '攻击状态',
  `dev_category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '触发告警的规则类型',
  `dev_rule` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '触发告警的规则',
  `degree` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '程度',
  `forbid_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '该请求是否被防火墙阻断',
  `req_method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'http请求方式',
  `threat_phase` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '威胁的阶段',
  `kill_chain` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '单个杀伤链',
  `kill_chain_all` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '全杀伤链',
  `attack_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '攻击类型及编号',
  `attack_type_all` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '攻击类型及编号',
  `att_ck_all` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '攻击类型及编号',
  `att_ck` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '攻击类型及编号',
  PRIMARY KEY (`event_id`) USING BTREE,
  INDEX `ip_subject_foreign_key`(`ip_subject`) USING BTREE,
  INDEX `ip_object_foreign_key`(`ip_object`) USING BTREE,
  CONSTRAINT `ip_subject_foreign_key` FOREIGN KEY (`ip_subject`) REFERENCES `ip_entity` (`ip`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ip_object_foreign_key` FOREIGN KEY (`ip_object`) REFERENCES `ip_entity` (`ip`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ip_alarm_event
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
