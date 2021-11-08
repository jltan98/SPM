-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3308
-- Generation Time: Nov 08, 2021 at 08:52 AM
-- Server version: 8.0.18
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lms`
--

-- --------------------------------------------------------

--
-- Table structure for table `quizinfo`
--

DROP TABLE IF EXISTS `quizinfo`;
CREATE TABLE IF NOT EXISTS `quizinfo` (
  `quizID` int(11) NOT NULL,
  `questionNumber` int(11) NOT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `selections` json NOT NULL,
  PRIMARY KEY (`quizID`,`questionNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quizinfo`
--

INSERT INTO `quizinfo` (`quizID`, `questionNumber`, `question`, `answer`, `selections`) VALUES
(1, 1, 'What came first', 'Chicken', '{\"selection\": [\"chicken\", \"egg\", \"hen\", \"rooster\"]}'),
(1, 2, 'What is the best drink?', 'Coffee', '{\"selection\": [\"milo\", \"coffee\", \"tea\", \"me\"]}');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
