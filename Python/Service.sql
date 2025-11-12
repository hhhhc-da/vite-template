/*
 Navicat Premium Dump SQL

 Source Server         : Windows-PDCN
 Source Server Type    : PostgreSQL
 Source Server Version : 180000 (180000)
 Source Host           : 192.168.1.72:5432
 Source Catalog        : Service
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 180000 (180000)
 File Encoding         : 65001

 Date: 12/11/2025 22:34:08
*/


-- ----------------------------
-- Table structure for username
-- ----------------------------
DROP TABLE IF EXISTS "public"."username";
CREATE TABLE "public"."username" (
  "id" int8 NOT NULL,
  "usr" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "pwd" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "eml" varchar(255) COLLATE "pg_catalog"."default",
  "phn" varchar(255) COLLATE "pg_catalog"."default",
  "pri" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Primary Key structure for table username
-- ----------------------------
ALTER TABLE "public"."username" ADD CONSTRAINT "username_pkey" PRIMARY KEY ("id");
