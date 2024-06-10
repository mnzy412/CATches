-- 데이터베이스와 테이블 생성
DROP DATABASE IF EXISTS catchesdb;
CREATE DATABASE IF NOT EXISTS catchesdb;
USE catchesdb;

CREATE TABLE `users` (
    `user_key` INT NOT NULL AUTO_INCREMENT COMMENT '회원 고유 식별자',
    `email` VARCHAR(50) NOT NULL COMMENT '회원 이메일',
    `password` VARCHAR(255) NOT NULL COMMENT '회원 비밀번호',
	`user_phone` VARCHAR(20) NULL,
    `user_name` VARCHAR(20) NULL COMMENT '사용자명',
    `status` ENUM('active', 'deleted') NOT NULL COMMENT '회원 상태(활성화, 탈퇴)',
    `user_nick` VARCHAR(20) NOT NULL COMMENT '랜덤 배정 닉네임',
    `deleted_at` DATETIME NULL COMMENT '탈퇴 시점',
    PRIMARY KEY (`user_key`)
);

CREATE TABLE `case_info` (
    `case_key` INT NOT NULL AUTO_INCREMENT COMMENT '사례의 고유 식별자',
    `user_key` INT NOT NULL COMMENT '회원 고유 식별자',
    `platform_key` INT NOT NULL COMMENT '플랫폼의 고유 식별자',
    `bank_key` INT NOT NULL COMMENT '은행 정보의 고유 식별자',
    `case_date` DATE NOT NULL,
    `case_status` ENUM('complete', 'continue') NOT NULL,
    PRIMARY KEY (`case_key`),
    FOREIGN KEY (`user_key`) REFERENCES `users` (`user_key`)
);

CREATE TABLE `platform` (
    `platform_key` INT NOT NULL AUTO_INCREMENT COMMENT '플랫폼의 고유 식별자',
    `platform_name` VARCHAR(50) NOT NULL COMMENT '플랫폼 이름 (트위터, 당근마켓 등)',
    `platform_url` VARCHAR(50) NULL COMMENT '사기 게시물의 URL',
    `suspent_id` VARCHAR(20) NULL COMMENT '용의자 사용 플랫폼 ID',
    PRIMARY KEY (`platform_key`)
);

CREATE TABLE `polices` (
    `police_key` INT NOT NULL COMMENT '경찰 정보 고유 식별자',
    `police_name` VARCHAR(20) NOT NULL COMMENT '경찰의 이름',
    `police_location` VARCHAR(20) NOT NULL COMMENT '경찰의 관할 지역',
    PRIMARY KEY (`police_key`)
);

CREATE TABLE `suspects` (
    `suspect_key` INT NOT NULL AUTO_INCREMENT COMMENT '용의자의 고유 식별자',
    `police_key` INT NULL COMMENT '경찰 정보 고유 식별자',
    `suspect_phone` VARCHAR(20) NULL COMMENT '용의자 연락처',
    `suspect_status` ENUM('arrested', 'unarrested') NOT NULL COMMENT '용의자의 검거 상태',
    `suspect_sex` ENUM('F','M') NULL,
    `suspect_age` INT NULL,
    `suspect_credit` INT NULL,
    `suspect_country` VARCHAR(50) NULL,
    PRIMARY KEY (`suspect_key`),
    FOREIGN KEY (`police_key`) REFERENCES `polices` (`police_key`)
);

CREATE TABLE `case_detail` (
    `case_detail_key` INT NOT NULL AUTO_INCREMENT COMMENT '디테일 고유 식별자',
    `case_key` INT NOT NULL COMMENT '사례의 고유 식별자',
    `case_type` VARCHAR(50) NOT NULL,
    `case_item` VARCHAR(50) NOT NULL,
    `case_price` DECIMAL(10,2) NULL,
    `bank_date` DATE NULL,
    `case_content` TEXT NULL,
    PRIMARY KEY (`case_detail_key`),
    FOREIGN KEY (`case_key`) REFERENCES `case_info` (`case_key`)
);


CREATE TABLE `phishing_info` (
    `phishing_key` INT NOT NULL AUTO_INCREMENT COMMENT '피싱 사이트의 고유 식별자',
    `user_key` INT NOT NULL COMMENT '회원 고유 식별자',
    `phishing_count` INT NOT NULL COMMENT '조회 수',
    `phishing_date` DATE NOT NULL COMMENT '등록일',
    `phishing_url` VARCHAR(255) NULL,
    PRIMARY KEY (`phishing_key`),
    FOREIGN KEY (`user_key`) REFERENCES `users` (`user_key`)
);

CREATE TABLE `phishing_detail` (
    `phishing_detail_key` INT NOT NULL AUTO_INCREMENT COMMENT '디테일 고유 식별자',
    `phishing_key` INT NOT NULL COMMENT '피싱 사이트의 고유 식별자',
    `site_type` VARCHAR(50) NOT NULL COMMENT '피해 유형',
    `site_name` VARCHAR(50) NULL,
    `site_content` TEXT NULL COMMENT '사건에 대한 설명',
    PRIMARY KEY (`phishing_detail_key`),
    FOREIGN KEY (`phishing_key`) REFERENCES `phishing_info` (`phishing_key`)
);

CREATE TABLE `bank_code` (
    `bank_code` INT NOT NULL AUTO_INCREMENT,
    `bank_name` VARCHAR(20) NULL,
    PRIMARY KEY (`bank_code`)
);

CREATE TABLE `bank` (
    `bank_key` INT NOT NULL AUTO_INCREMENT COMMENT '은행 정보의 고유 식별자',
    `suspect_key` INT NOT NULL COMMENT '용의자의 고유 식별자',
    `bank_account` VARCHAR(50) NOT NULL COMMENT '용의자 계좌번호',
    `bank_nickname` VARCHAR(50) NOT NULL COMMENT '명의자 성명',
    `bank_code` INT NOT NULL,
    PRIMARY KEY (`bank_key`),
    FOREIGN KEY (`suspect_key`) REFERENCES `suspects` (`suspect_key`),
    FOREIGN KEY (`bank_code`) REFERENCES `bank_code` (`bank_code`)
);

-- 사용자 권한 설정
-- 0. 기존 사용자가 있다면 삭제
DROP USER IF EXISTS 'yunseo'@'localhost';
DROP USER IF EXISTS 'songha'@'localhost';
DROP USER IF EXISTS 'heeseo'@'localhost';
DROP USER IF EXISTS 'mnzy'@'localhost';

-- 1. 총괄 책임자 (Yunseo)
CREATE USER 'yunseo'@'localhost' IDENTIFIED BY '0000';
GRANT ALL PRIVILEGES ON catchesdb.* TO 'yunseo'@'localhost';

-- 2. 일반 관리자 (Songha)
CREATE USER 'songha'@'localhost' IDENTIFIED BY '0000';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.case_info TO 'songha'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.case_detail TO 'songha'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.platform TO 'songha'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.suspects TO 'songha'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.bank TO 'songha'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.bank_code TO 'songha'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.phishing_info TO 'songha'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.phishing_detail TO 'songha'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.polices TO 'songha'@'localhost';
-- No access to the users table

-- 3. 내부 직원 (Heeseo)
CREATE USER 'heeseo'@'localhost' IDENTIFIED BY '0000';
GRANT SELECT ON catchesdb.case_detail TO 'heeseo'@'localhost';

-- 4. 사용자 (Mnzy)
CREATE USER 'mnzy'@'localhost' IDENTIFIED BY '0000';
GRANT SELECT, INSERT, UPDATE, DELETE ON catchesdb.users TO 'mnzy'@'localhost';
-- Further restrictions can be applied via application logic to ensure mnzy can only access their own records

-- Apply changes
FLUSH PRIVILEGES;