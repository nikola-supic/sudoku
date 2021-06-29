-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 29, 2021 at 11:24 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sudoku`
--

-- --------------------------------------------------------

--
-- Table structure for table `levels`
--

CREATE TABLE `levels` (
  `id` int(11) NOT NULL,
  `creator` varchar(24) NOT NULL,
  `start` varchar(384) NOT NULL,
  `finish` varchar(384) NOT NULL,
  `record` int(11) NOT NULL DEFAULT 9999,
  `recorder` varchar(24) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `levels`
--

INSERT INTO `levels` (`id`, `creator`, `start`, `finish`, `record`, `recorder`) VALUES
(1, 'Sule', '[[1, 8, 5, 4, 2, 0, 0, 0, 0], [3, 7, 4, 5, 6, 0, 0, 0, 0], [9, 6, 2, 3, 7, 0, 0, 0, 0], [4, 9, 6, 8, 3, 0, 0, 0, 0], [2, 1, 8, 7, 4, 0, 0, 0, 0], [7, 5, 3, 1, 9, 0, 0, 0, 0], [5, 3, 1, 9, 8, 0, 0, 0, 0], [6, 4, 9, 2, 5, 0, 0, 0, 0], [8, 2, 7, 6, 1, 0, 0, 0, 0]]', '[[1, 8, 5, 4, 2, 9, 3, 7, 6],  [3, 7, 4, 5, 6, 1, 8, 9, 2], [9, 6, 2, 3, 7, 8, 5, 4, 1],  [4, 9, 6, 8, 3, 2, 7, 1, 5],  [2, 1, 8, 7, 4, 5, 6, 3, 9],  [7, 5, 3, 1, 9, 6, 4, 2, 8],  [5, 3, 1, 9, 8, 4, 2, 6, 7],  [6, 4, 9, 2, 5, 7, 1, 8, 3],  [8, 2, 7, 6, 1, 3, 9, 5, 4]]', 5, ''),
(4, 'Sule', '[[0, 0, 0, 4, 0, 7, 0, 0, 0], [0, 5, 8, 1, 2, 0, 0, 3, 0], [0, 0, 0, 0, 0, 3, 2, 1, 9], [2, 0, 7, 0, 0, 1, 5, 6, 0], [0, 9, 0, 0, 7, 8, 3, 4, 0], [0, 6, 0, 0, 4, 5, 1, 0, 0], [7, 8, 0, 0, 5, 4, 0, 0, 6], [0, 3, 0, 7, 0, 0, 0, 5, 1], [0, 2, 6, 8, 0, 0, 4, 0, 0], [], [], [], [], [], [], [], [], []]', '[[3, 1, 2, 4, 9, 7, 6, 8, 5], [9, 5, 8, 1, 2, 6, 7, 3, 4], [6, 7, 4, 5, 8, 3, 2, 1, 9], [2, 4, 7, 9, 3, 1, 5, 6, 8], [1, 9, 5, 6, 7, 8, 3, 4, 2], [8, 6, 3, 2, 4, 5, 1, 9, 7], [7, 8, 1, 3, 5, 4, 9, 2, 6], [4, 3, 9, 7, 6, 2, 8, 5, 1], [5, 2, 6, 8, 1, 9, 4, 7, 3]]', 1, ''),
(6, 'Sule', '[[2, 7, 0, 9, 8, 0, 5, 1, 0], [9, 0, 0, 6, 1, 3, 8, 0, 2], [0, 0, 8, 2, 0, 7, 0, 0, 4], [4, 0, 0, 1, 0, 6, 7, 3, 0], [6, 0, 0, 0, 0, 5, 0, 0, 0], [7, 0, 0, 0, 3, 0, 4, 0, 9], [5, 0, 4, 0, 0, 8, 9, 0, 6], [0, 0, 0, 4, 2, 0, 1, 0, 0], [8, 0, 9, 0, 0, 1, 3, 0, 0], [], [], [], [], [], [], [], [], []]', '[[2, 7, 6, 9, 8, 4, 5, 1, 3], [9, 4, 5, 6, 1, 3, 8, 7, 2], [1, 3, 8, 2, 5, 7, 6, 9, 4], [4, 8, 2, 1, 9, 6, 7, 3, 5], [6, 9, 3, 7, 4, 5, 2, 8, 1], [7, 5, 1, 8, 3, 2, 4, 6, 9], [5, 1, 4, 3, 7, 8, 9, 2, 6], [3, 6, 7, 4, 2, 9, 1, 5, 8], [8, 2, 9, 5, 6, 1, 3, 4, 7]]', 5, '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `levels`
--
ALTER TABLE `levels`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `levels`
--
ALTER TABLE `levels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
