CREATE TABLE `version` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `table_name` VARCHAR(32) NOT NULL,
    `table_version` INT UNSIGNED DEFAULT 0 NOT NULL,
    CONSTRAINT table_name_idx UNIQUE (`table_name`)
);

INSERT INTO version (table_name, table_version) values ('version','1');

CREATE TABLE `dialplan` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `dpid` INT(11) NOT NULL,
    `pr` INT(11) NOT NULL,
    `match_op` INT(11) NOT NULL,
    `match_exp` VARCHAR(64) NOT NULL,
    `match_len` INT(11) NOT NULL,
    `subst_exp` VARCHAR(64) NOT NULL,
    `repl_exp` VARCHAR(256) NOT NULL,
    `attrs` VARCHAR(64) NOT NULL
);

INSERT INTO version (table_name, table_version) values ('dialplan','2');

CREATE TABLE `dispatcher` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `setid` INT DEFAULT 0 NOT NULL,
    `destination` VARCHAR(192) DEFAULT '' NOT NULL,
    `flags` INT DEFAULT 0 NOT NULL,
    `priority` INT DEFAULT 0 NOT NULL,
    `attrs` VARCHAR(128) DEFAULT '' NOT NULL,
    `description` VARCHAR(64) DEFAULT '' NOT NULL
);

INSERT INTO version (table_name, table_version) values ('dispatcher','4');

CREATE TABLE `domain` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `domain` VARCHAR(64) NOT NULL,
    `did` VARCHAR(64) DEFAULT NULL,
    `last_modified` DATETIME DEFAULT '2000-01-01 00:00:01' NOT NULL,
    CONSTRAINT domain_idx UNIQUE (`domain`)
);

INSERT INTO version (table_name, table_version) values ('domain','2');

CREATE TABLE `domain_attrs` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `did` VARCHAR(64) NOT NULL,
    `name` VARCHAR(32) NOT NULL,
    `type` INT UNSIGNED NOT NULL,
    `value` VARCHAR(255) NOT NULL,
    `last_modified` DATETIME DEFAULT '2000-01-01 00:00:01' NOT NULL
);

CREATE INDEX domain_attrs_idx ON domain_attrs (`did`, `name`);

INSERT INTO version (table_name, table_version) values ('domain_attrs','1');

CREATE TABLE `htable` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `key_name` VARCHAR(64) DEFAULT '' NOT NULL,
    `key_type` INT DEFAULT 0 NOT NULL,
    `value_type` INT DEFAULT 0 NOT NULL,
    `key_value` VARCHAR(128) DEFAULT '' NOT NULL,
    `expires` INT DEFAULT 0 NOT NULL
);

INSERT INTO version (table_name, table_version) values ('htable','2');

CREATE TABLE `tenant` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `key_name` VARCHAR(64) DEFAULT '' NOT NULL,
    `key_type` INT DEFAULT 0 NOT NULL,
    `value_type` INT DEFAULT 0 NOT NULL,
    `key_value` VARCHAR(128) DEFAULT '' NOT NULL,
    `expires` INT DEFAULT 0 NOT NULL
);

INSERT INTO version (table_name, table_version) values ('tenant','1');

CREATE TABLE `trusted` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `src_ip` VARCHAR(50) NOT NULL,
    `proto` VARCHAR(4) NOT NULL,
    `from_pattern` VARCHAR(64) DEFAULT NULL,
    `ruri_pattern` VARCHAR(64) DEFAULT NULL,
    `tag` VARCHAR(64),
    `priority` INT DEFAULT 0 NOT NULL
);

CREATE INDEX peer_idx ON trusted (`src_ip`);

INSERT INTO version (table_name, table_version) values ('trusted','6');

CREATE TABLE `address` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `grp` INT(11) UNSIGNED DEFAULT 1 NOT NULL,
    `ip_addr` VARCHAR(50) NOT NULL,
    `mask` INT DEFAULT 32 NOT NULL,
    `port` SMALLINT(5) UNSIGNED DEFAULT 0 NOT NULL,
    `tag` VARCHAR(64)
);

INSERT INTO version (table_name, table_version) values ('address','6');

CREATE TABLE `rtpengine` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `setid` INT(10) UNSIGNED DEFAULT 0 NOT NULL,
    `url` VARCHAR(64) NOT NULL,
    `weight` INT(10) UNSIGNED DEFAULT 1 NOT NULL,
    `disabled` INT(1) DEFAULT 0 NOT NULL,
    `stamp` DATETIME DEFAULT '1900-01-01 00:00:01' NOT NULL,
    CONSTRAINT rtpengine_nodes UNIQUE (`setid`, `url`)
);

INSERT INTO version (table_name, table_version) values ('rtpengine','1');

CREATE TABLE `acc` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `method` VARCHAR(16) DEFAULT '' NOT NULL,
    `from_tag` VARCHAR(128) DEFAULT '' NOT NULL,
    `to_tag` VARCHAR(128) DEFAULT '' NOT NULL,
    `callid` VARCHAR(255) DEFAULT '' NOT NULL,
    `sip_code` VARCHAR(3) DEFAULT '' NOT NULL,
    `sip_reason` VARCHAR(128) DEFAULT '' NOT NULL,
    `time` DATETIME NOT NULL
);

CREATE INDEX callid_idx ON acc (`callid`);

INSERT INTO version (table_name, table_version) values ('acc','5');

CREATE TABLE `acc_cdrs` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `start_time` DATETIME DEFAULT '2000-01-01 00:00:00' NOT NULL,
    `end_time` DATETIME DEFAULT '2000-01-01 00:00:00' NOT NULL,
    `duration` FLOAT(10,3) DEFAULT 0 NOT NULL
);

CREATE INDEX start_time_idx ON acc_cdrs (`start_time`);

INSERT INTO version (table_name, table_version) values ('acc_cdrs','2');

CREATE TABLE `missed_calls` (
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    `method` VARCHAR(16) DEFAULT '' NOT NULL,
    `from_tag` VARCHAR(128) DEFAULT '' NOT NULL,
    `to_tag` VARCHAR(128) DEFAULT '' NOT NULL,
    `callid` VARCHAR(255) DEFAULT '' NOT NULL,
    `sip_code` VARCHAR(3) DEFAULT '' NOT NULL,
    `sip_reason` VARCHAR(128) DEFAULT '' NOT NULL,
    `time` DATETIME NOT NULL
);

CREATE INDEX callid_idx ON missed_calls (`callid`);

INSERT INTO version (table_name, table_version) values ('missed_calls','4');