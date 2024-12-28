-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 19, 2024 at 05:45 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `employee dpt`
--

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE IF NOT EXISTS `department` (
  `department_id` varchar(20) DEFAULT NULL,
  `department_name` varchar(50) DEFAULT NULL,
  `joining_date` varchar(12) NOT NULL,
  `attendance` varchar(20) NOT NULL,
  `performance_score` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`department_id`, `department_name`, `joining_date`, `attendance`, `performance_score`) VALUES
('D004', 'Service', '20-06-2023', '56', '6');

-- --------------------------------------------------------

--
-- Table structure for table `employee_dpt`
--

CREATE TABLE IF NOT EXISTS `employee_dpt` (
  `Employee_id` varchar(50) DEFAULT NULL,
  `Employee_Name` varchar(30) DEFAULT NULL,
  `Last_Name` varchar(35) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `Mail` varchar(50) DEFAULT NULL,
  `Address` varchar(55) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employee_dpt`
--


-- --------------------------------------------------------

--
-- Table structure for table `leave_details`
--

CREATE TABLE IF NOT EXISTS `leave_details` (
  `leave_id` int(20) DEFAULT NULL,
  `Employee_id` int(30) DEFAULT NULL,
  `leave_type` varchar(100) DEFAULT NULL,
  `leave_start` date DEFAULT NULL,
  `leave_end` date DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `leave_details`
--


-- --------------------------------------------------------

--
-- Table structure for table `payout_salary_details`
--

CREATE TABLE IF NOT EXISTS `payout_salary_details` (
  `payout_id` int(11) DEFAULT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `salary` int(11) DEFAULT NULL,
  `payout_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `payout_salary_details`
--

