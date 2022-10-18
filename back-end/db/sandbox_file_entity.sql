/*
 Navicat MySQL Data Transfer

 Source Server         : test1
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : test_sandbox

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sandbox_file_entity
-- ----------------------------
DROP TABLE IF EXISTS `sandbox_file_entity`;
CREATE TABLE `sandbox_file_entity`  (
  `sha1` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `file_name` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  `file_type` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  `md5` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  `submit_time` timestamp NOT NULL COMMENT '提交时间',
  `threat_level` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL COMMENT '威胁等级',
  `multi_engines` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL COMMENT '反病毒扫描引擎检出率',
  `sandbox_type_list` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL COMMENT '沙箱运行环境',
  `threat_score` int NULL DEFAULT NULL COMMENT '文件威胁分值',
  `sandbox_behaviors` varchar(2055) CHARACTER SET utf8mb4 NULL DEFAULT NULL COMMENT '文件行为检测',
  `multiengines_results` varchar(2055) CHARACTER SET utf8mb4 NULL DEFAULT NULL COMMENT '反病毒引擎检测结果',

  PRIMARY KEY (`sha1`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sandbox_file_entity
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
