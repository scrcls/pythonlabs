DROP TABLE IF EXISTS `department`;
CREATE TABLE `department` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(16) NOT NULL,
    `deptCode` varchar(4) NOT NULL,
    `level` tinyint(2) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`deptCode`)
    UNIQUE (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(5) NOT NULL,
    `email` varchar(64) NOT NULL,
    `loginId` varchar(5) NOT NULL,
    `deptId` int(11) NOT NULL,
    `sex` varchar(1) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`email`),
    UNIQUE (`loginId`),
    FOREIGN KEY (`deptId`) REFERENCES `department` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `depart_leader`;
CREATE TABLE `depart_leader` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `deptId` int(11) NOT NULL,
    `userId` int(11) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`deptId`) REFERENCES `department` (`id`),
    FOREIGN KEY (`userId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `worker_leader`;
CREATE TABLE `worker_leader` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `workerId` int(11) NOT NULL,
    `leaderId` int(11) NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY (`workerId`) REFERENCES `user` (`id`),
    FOREIGN KEY (`leaderId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



