SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `LearningManagementSystem` 
--
CREATE DATABASE IF NOT EXISTS `LearningManagementSystem` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `LearningManagementSystem`;

-- --------------------------------------------------------


--
-- Table structure for table `Learner`
--

DROP TABLE IF EXISTS `learner`;
CREATE TABLE IF NOT EXISTS `learner` (
  `learnerName` varchar(64) NOT NULL,
  `learnerID` varchar(64) NOT NULL,
  `learnerContact` varchar(255) NOT NULL,
  `coursesTaken` text NOT NULL,
  PRIMARY KEY (`learnerID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `learner` (`learnerName`, `learnerID`, `learnerContact`, `coursesTaken`) VALUES
('Alivia', 'L001', 'alivia@lms.com', "['IS111', 'IS213', 'IS215']"),
('Stella', 'L002', 'stella@lms.com', "['IS110', 'IS111']"),
('Natalie', 'L003', 'natalie@lms.com', "['IS212']"),
('Lyndy', 'L004', 'lyndy@lms.com', "['IS110']"),
('Mabel', 'L005', 'mabel@lms.com', "[]");

DROP TABLE IF EXISTS `trainer`;
CREATE TABLE IF NOT EXISTS `trainer` (
  `trainerName` varchar(64) NOT NULL,
  `trainerID` varchar(64) NOT NULL,
  `trainerContact` varchar(255) NOT NULL,
  `skills` text NOT NULL,
  `experience` text NOT NULL,
  `coursesTaught` text NOT NULL,
  PRIMARY KEY (`trainerID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `trainer` (`trainerName`, `trainerID`, `trainerContact`, `skills`, `experience`, `coursesTaught`) VALUES
('Anne', 'T001', 'anne@lms.com', "['Process Change Management', 'Aftersales IT Support', 'Software Development']", "8 years experience in IT operation", "['IS111', 'IS212', 'IS213', 'IS216']"),
('Bill', 'T002', 'bill@lms.com', "['Business Analytics', 'Product Management', 'IT Solutions and Support']", "5 years experience in IT product analysis and 2 years experience in sales and support", "['IS111', 'IS212', 'IS214']"),
('Catty', 'T003', 'catty@lms.com', "['Product Marketing', 'IT Solutions and Support']", "5 years experience in Sales and Marketing and 3 years experience in IT support", "['IS111', 'IS213']"),
('Dia', 'T004', 'dia@lms.com', "['Product Support', 'Customer Relationship Management']", "10 years experience in customer service for IT products", "['IS200', 'IS111', 'IS446']"),
('Elin', 'T005', 'elin@lms.com', "['IT Support', 'Product Management']", "2 years experience in IT support and 3 year experience as senior product manager", "['IS200', 'IS111', 'IS214']");

DROP TABLE IF EXISTS `administrator`;
CREATE TABLE IF NOT EXISTS `administrator` (
  `adminName` varchar(64) NOT NULL,
  `adminID` varchar(64) NOT NULL,
  `adminContact` varchar(255) NOT NULL,
  PRIMARY KEY (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `administrator` (`adminName`, `adminID`, `adminContact`) VALUES
('Estella', 'admin001', 'estella@lms.com'),
('Finn', 'admin002', 'finn@lms.com'),
('Anson', 'adminL003', 'anson@lms.com'),
('Dawn', 'admin004', 'dawn@lms.com'),
('George', 'admin005', 'george@lms.com');

DROP TABLE IF EXISTS `course`;
CREATE TABLE IF NOT EXISTS `course` (
  `courseID` varchar(64) NOT NULL,
  `courseName` varchar(64) NOT NULL,
  `courseDescription` text NOT NULL,
  `prerequisite` text NOT NULL,
  `noOfClasses` int(11) NOT NULL,
  `classes` text NOT NULL,
  `subjectcategory` varchar(255) NOT NULL,
  PRIMARY KEY (`courseID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `Course` (`courseID`, `courseName`, `courseDescription`, `prerequisite`, `noOfClasses`, `classes`, `subjectcategory`) VALUES
('IS212', 'Software Project Management', '...', "['IS111', 'IS213']", 2, "['G1', 'G2']", 'Project Management'),
('IS111', 'Python Programming', '...', "[]", 5, "['G1', 'G2', 'G3', 'G4', 'G5']", 'Programming'),
('IS213', 'Solution Development', '...', "['IS111']", 2, "['G1', 'G2']", 'Programming'),
('IS214', 'Analytics Foundation', '...', "['IS111']", 1, "['G1']", 'Analytics'),
('IS200', 'Customer Support', '...', "['IS111']", 2, "['G1', 'G2']", 'Support');

DROP TABLE IF EXISTS `classes`;
CREATE TABLE IF NOT EXISTS `classes` (
  `classID` varchar(64) NOT NULL,
  `courseID` varchar(64) NOT NULL,
  `noOfSlots` int(11) NOT NULL,
  `trainerAssignedID` varchar(64) NOT NULL,
  `startDate` datetime NOT NULL,
  `endDate` datetime NOT NULL,
  PRIMARY KEY (`classID`, `courseID`),
  KEY `FK_courseID` (`courseID`),
  KEY `FK_trainerID` (`trainerAssignedID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `classes` (`classID`, `courseID`, `noOfSlots`, `trainerAssignedID`, `startDate`, `endDate`) VALUES
('G1', 'IS212', 20, 'T001', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G2', 'IS212', 20, 'T002', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G1', 'IS111', 15, 'T001', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G2', 'IS111', 15, 'T002', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G3', 'IS111', 15, 'T003', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G4', 'IS111', 15, 'T004', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G5', 'IS111', 15, 'T005', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G1', 'IS213', 20, 'T001', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G2', 'IS213', 20, 'T003', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G1', 'IS214', 20, 'T002', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G1', 'IS200', 20, 'T004', '2021-10-01 00:00:00', '2021-11-30 00:00:00'),
('G2', 'IS200', 20, 'T005', '2021-10-01 00:00:00', '2021-11-30 00:00:00');

DROP TABLE IF EXISTS `application`;
CREATE TABLE IF NOT EXISTS `application` (
  `applicationID` int(11) NOT NULL AUTO_INCREMENT,
  `applicationLearnerID` varchar(64) NOT NULL,
  `applicationClassID` varchar(64) NOT NULL,
  `applicationStatus` varchar(64) NOT NULL,
  `regStartDate` datetime NOT NULL,
  `regEndDate` datetime NOT NULL,
  `adminID` varchar(64) NOT NULL,
  PRIMARY KEY (`applicationID`),
  KEY `FK_learnerID` (`applicationLearnerID`),
  KEY `FK_classID` (`applicationClassID`),
  KEY `FK_adminID` (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `application` (`applicationID`, `applicationLearnerID`, `applicationClassID`, `applicationStatus`, `regStartDate`, `regEndDate`, `adminID`) VALUES
(1, 'L001', 'G1', 'Draft','2021-08-01 00:00:00', '2021-09-01 00:00:00', 'admin001'),
(2, 'L002', 'G1', 'Processing', '2021-08-01 00:00:00', '2021-09-01 00:00:00', 'admin002'),
(3, 'L003', 'G3', 'Processing', '2021-08-01 00:00:00', '2021-09-01 00:00:00', 'admin003'),
(4, 'L004', 'G1', 'Draft', '2021-08-01 00:00:00', '2021-09-01 00:00:00', 'admin004'),
(5, 'L005', 'G3', 'Draft', '2021-08-01 00:00:00', '2021-09-01 00:00:00', 'admin005');


COMMIT;
