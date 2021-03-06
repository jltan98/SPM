SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `LMS` 
--
CREATE DATABASE IF NOT EXISTS `LMS` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `LMS`;

-- --------------------------------------------------------


--
-- Table structure for table `Learner`
--

DROP TABLE IF EXISTS `learner`;
CREATE TABLE IF NOT EXISTS `learner` (
  `learnerName` varchar(64) NOT NULL,
  `learnerID` varchar(64) NOT NULL,
  `learnerContact` varchar(256) NOT NULL,
  `coursesTaken` text NOT NULL,
  `password` varchar (256) NOT NULL,
  PRIMARY KEY (`learnerID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `learner` (`learnerName`, `learnerID`, `learnerContact`, `coursesTaken`, `password`) VALUES
('Alivia', 'L001', 'alivia@lms.com', "IS111, IS213, IS215", SHA1('learner1')),
('Stella', 'L002', 'stella@lms.com', "IS110, IS111", SHA1('learner2')),
('Natalie', 'L003', 'natalie@lms.com', "IS212", SHA1('learner3')),
('Lyndy', 'L004', 'lyndy@lms.com', "IS110", SHA1('learner4')),
('Mabel', 'L005', 'mabel@lms.com', "", SHA1('learner5'));

DROP TABLE IF EXISTS `trainer`;
CREATE TABLE IF NOT EXISTS `trainer` (
  `trainerName` varchar(64) NOT NULL,
  `trainerID` varchar(64) NOT NULL,
  `trainerContact` varchar(256) NOT NULL,
  `password` varchar (256) NOT NULL,
  `skills` text NOT NULL,
  `experience` text NOT NULL,
  `coursesTaught` text NOT NULL,
  PRIMARY KEY (`trainerID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `trainer` (`trainerName`, `trainerID`, `trainerContact`, `password`, `skills`, `experience`, `coursesTaught`) VALUES
('Anne', 'T001', 'anne@lms.com', SHA1('trainer1'), "Process Change Management, Aftersales IT Support, Software Development", "8 years experience in IT operation", "IS111, IS212, IS213, IS216"),
('Bill', 'T002', 'bill@lms.com', SHA1('trainer2'),"Business Analytics, Product Management, IT Solutions and Support", "5 years experience in IT product analysis, 2 years experience in sales and support", "IS111, IS212, IS214"),
('Catty', 'T003', 'catty@lms.com', SHA1('trainer3'),"Product Marketing, IT Solutions and Support", "5 years experience in Sales and Marketing, 3 years experience in IT support", "IS111, IS213"),
('Dia', 'T004', 'dia@lms.com', SHA1('trainer4'),"Product Support, Customer Relationship Management", "10 years experience in customer service for IT products", "IS200, IS111, IS446"),
('Elin', 'T005', 'elin@lms.com', SHA1('trainer5'),"IT Support, Product Management", "2 years experience in IT support, 3 year experience as senior product manager", "IS200, IS111, IS214");

DROP TABLE IF EXISTS `administrator`;
CREATE TABLE IF NOT EXISTS `administrator` (
  `adminName` varchar(64) NOT NULL,
  `adminID` varchar(64) NOT NULL,
  `adminContact` varchar(256) NOT NULL,
  `password` varchar (256) NOT NULL,
  PRIMARY KEY (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `administrator` (`adminName`, `adminID`, `adminContact`, `password`) VALUES
('Estella', 'admin001', 'estella@lms.com', SHA1('admin1')),
('Finn', 'admin002', 'finn@lms.com', SHA1('admin2')),
('Anson', 'adminL003', 'anson@lms.com', SHA1('admin3')),
('Dawn', 'admin004', 'dawn@lms.com', SHA1('admin4')),
('George', 'admin005', 'george@lms.com', SHA1('admin5'));

DROP TABLE IF EXISTS `course`;
CREATE TABLE IF NOT EXISTS `course` (
  `courseID` varchar(64) NOT NULL,
  `courseName` varchar(64) NOT NULL,
  `courseDescription` text NOT NULL,
  `prerequisite` text NOT NULL,
  `noOfClasses` int(11) NOT NULL,
  `classes` text NOT NULL,
  `subjectcategory` varchar(256) NOT NULL,
  PRIMARY KEY (`courseID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `course` (`courseID`, `courseName`, `courseDescription`, `prerequisite`, `noOfClasses`, `classes`, `subjectcategory`) VALUES
('IS212', 'Software Project Management', '...', "IS111, IS213", 2, "G1, G2", 'Project Management'),
('IS111', 'Python Programming', '...', "", 5, "G1, G2, G3, G4, G5", 'Programming'),
('IS213', 'Solution Development', '...', "IS111", 2, "G1, G2", 'Programming'),
('IS214', 'Analytics Foundation', '...', "IS111", 1, "G1", 'Analytics'),
('IS200', 'Customer Support', '...', "IS111", 2, "G1, G2", 'Support');


DROP TABLE IF EXISTS `enrolmentPeriod`;
CREATE TABLE IF NOT EXISTS `enrolmentPeriod` (
  `enrolmentPeriodID` varchar(64) NOT NULL,
  `enrolmentStartDate` datetime NOT NULL,
  `enrolmentEndDate` datetime NOT NULL,
  PRIMARY KEY (enrolmentPeriodID)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `enrolmentPeriod` (`enrolmentPeriodID`, `enrolmentStartDate`, `enrolmentEndDate`) VALUES
('FY20/21 Session 1', '2020-10-15 00:00:00', '2021-11-30 00:00:00'),
('FY20/21 Session 2', '2021-10-15 00:00:00', '2021-11-30 00:00:00');


DROP TABLE IF EXISTS `classes`;
CREATE TABLE IF NOT EXISTS `classes` (
  `classID` varchar(64) NOT NULL,
  `courseID` varchar(64) NOT NULL,
  `noOfSlots` int(11) NOT NULL,
  `trainerAssignedID` varchar(64) NOT NULL,
  `startDate` datetime NOT NULL,
  `endDate` datetime NOT NULL,
  `enrolmentPeriodID` varchar(64) NOT NULL,
  PRIMARY KEY (`classID`, `courseID`, `enrolmentPeriodID`),
  KEY `FK_courseID` (`courseID`),
  KEY `FK_trainerID` (`trainerAssignedID`),
  KEY `FK_enrolmentPeriodID` (`enrolmentPeriodID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `classes` (`classID`, `courseID`, `noOfSlots`, `trainerAssignedID`, `startDate`, `endDate`, `enrolmentPeriodID`) VALUES
('G1', 'IS212', 20, 'T001', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G2', 'IS212', 20, 'T002', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G1', 'IS111', 15, 'T001', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G2', 'IS111', 15, 'T002', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G3', 'IS111', 15, 'T003', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G4', 'IS111', 15, 'T004', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G5', 'IS111', 15, 'T005', '2022-02-05 00:00:00', '2022-10-05 00:00:00', 'FY20/21 Session 2'),
('G1', 'IS213', 20, 'T001', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G2', 'IS213', 20, 'T003', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G1', 'IS214', 20, 'T002', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G1', 'IS200', 20, 'T004', '2022-01-10 00:00:00', '2022-06-30 00:00:00', 'FY20/21 Session 2'),
('G2', 'IS200', 20, 'T005', '2022-02-05 00:00:00', '2022-10-05 00:00:00', 'FY20/21 Session 2'),
('G1', 'IS200', 20, 'T004', '2021-01-10 00:00:00', '2021-06-30 00:00:00', 'FY20/21 Session 1'),
('G2', 'IS200', 20, 'T005', '2021-02-05 00:00:00', '2021-10-05 00:00:00', 'FY20/21 Session 1'),
('G1', 'IS212', 20, 'T001', '2021-01-10 00:00:00', '2021-06-30 00:00:00', 'FY20/21 Session 1'),
('G2', 'IS212', 20, 'T002', '2021-02-05 00:00:00', '2021-10-05 00:00:00', 'FY20/21 Session 1');

DROP TABLE IF EXISTS `application`;
CREATE TABLE IF NOT EXISTS `application` (
  `applicationID` int(11) NOT NULL AUTO_INCREMENT,
  `applicationLearnerID` varchar(64) NOT NULL,
  `applicationClassID` varchar(64) NOT NULL,
  `applicationCourseID` varchar(64) NOT NULL,
  `applicationStatus` varchar(64) NOT NULL,
  `adminID` varchar(64) NOT NULL,
  `enrolmentPeriodID` varchar(64) NOT NULL,
  `applicationDate` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`applicationID`),
  KEY `FK_learnerID` (`applicationLearnerID`),
  KEY `FK_classID` (`applicationClassID`),
  KEY `FK_courseID` (`applicationCourseID`),
  KEY `FK_adminID` (`adminID`),
  KEY `FK_enrolmentPeriodID` (`enrolmentPeriodID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `application` (`applicationID`, `applicationLearnerID`, `applicationClassID`, `applicationCourseID`, `applicationStatus`, `adminID`, `enrolmentPeriodID`, `applicationDate`) VALUES
(1, 'L001', 'G1', 'IS212', 'Processing', 'admin001', 'FY20/21 Session 2', CURRENT_TIMESTAMP),
(2, 'L002', 'G1', 'IS214', 'Processing', 'admin002', 'FY20/21 Session 2', CURRENT_TIMESTAMP),
(3, 'L003', 'G3', 'IS213', 'Processing', 'admin003', 'FY20/21 Session 2', CURRENT_TIMESTAMP),
(4, 'L004', 'G1', 'IS212', 'Unsuccessful', 'admin001', 'FY20/21 Session 1', CURRENT_TIMESTAMP),
(5, 'L005', 'G3', 'IS200', 'Unsuccessful', 'admin005', 'FY20/21 Session 1', CURRENT_TIMESTAMP);


DROP TABLE IF EXISTS `quizzes`;
CREATE TABLE IF NOT EXISTS `quizzes` (
  `quizID` int(11) NOT NULL,
  `classID` varchar(10) NOT NULL,
  `sectionID` varchar(5) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`quizID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `quizzes` (`quizID`, `classID`, `sectionID`, `active`) VALUES
(1, 'G1', 'IS111', 1);


DROP TABLE IF EXISTS `quizinfo`;
CREATE TABLE IF NOT EXISTS `quizinfo` (
  `quizID` int(11) NOT NULL,
  `questionNumber` int(11) NOT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `selections` json NOT NULL,
  PRIMARY KEY (`quizID`,`questionNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `quizinfo` (`quizID`, `questionNumber`, `question`, `answer`, `selections`) VALUES
(1, 1, 'What came first', 'Chicken', '{\"selection\": [\"chicken\", \"egg\", \"hen\", \"rooster\"]}'),
(1, 2, 'What is the best drink?', 'Coffee', '{\"selection\": [\"milo\", \"coffee\", \"tea\", \"me\"]}');

COMMIT;
