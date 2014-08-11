CREATE TABLE IF NOT EXISTS `domains` (
  `domain_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) NOT NULL,
  `ext` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0:普通域名,1:泛域名',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0',
  `last_update_time` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`domain_id`),
  UNIQUE KEY `name` (`domain`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `routers` (
  `router_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `domain_id` int(10) unsigned NOT NULL,
  `source_id` int(10) unsigned NOT NULL,
  `server_id` int(10) unsigned NOT NULL,
  `source_mode` tinyint(1) unsigned NOT NULL COMMENT '0:master,1:backup,2:hash',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0',
  `last_update_time` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`router_id`),
  UNIQUE KEY `domain_id` (`domain_id`,`source_id`,`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `servers` (
  `server_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) NOT NULL,
  `token` char(32) NOT NULL,
  `last_update_time` int(10) unsigned NOT NULL DEFAULT '0',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `sources` (
  `source_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `domain_id` int(10) unsigned NOT NULL,
  `address` varchar(255) NOT NULL COMMENT '源站IP或者域名',
  `create_time` int(10) unsigned NOT NULL DEFAULT '0',
  `last_update_time` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`source_id`),
  KEY `domain_id` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
