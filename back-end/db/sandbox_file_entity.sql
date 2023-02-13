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

 Date: 13/02/2023 16:28:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sandbox_file_entity
-- ----------------------------
DROP TABLE IF EXISTS `sandbox_file_entity`;
CREATE TABLE `sandbox_file_entity` (
  `sha1` varchar(255) NOT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `file_type` varchar(255) DEFAULT NULL,
  `md5` varchar(255) DEFAULT NULL,
  `submit_time` timestamp NOT NULL COMMENT '提交时间时间',
  `threat_level` varchar(255) DEFAULT NULL COMMENT '威胁等级',
  `multi_engines` varchar(255) DEFAULT NULL COMMENT '反病毒扫描引擎检出率',
  `sandbox_type_list` varchar(255) DEFAULT NULL COMMENT '沙箱运行环境',
  `threat_score` int DEFAULT NULL COMMENT '文件威胁分值',
  `sandbox_behaviors` varchar(2055) DEFAULT NULL COMMENT '文件行为检测',
  `multiengines_results` varchar(2055) DEFAULT NULL COMMENT '反病毒引擎检测结果',
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
