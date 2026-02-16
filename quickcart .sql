-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 06, 2026 at 03:04 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `quickcart`
--

-- --------------------------------------------------------

--
-- Table structure for table `brand`
--

CREATE TABLE `brand` (
  `Brand_Id` int(11) DEFAULT NULL,
  `Brand_Nm` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `brand`
--

INSERT INTO `brand` (`Brand_Id`, `Brand_Nm`) VALUES
(101, 'Apple'),
(102, 'Samsung'),
(103, 'Dell'),
(104, 'HP'),
(105, 'Nike'),
(106, 'Adidas'),
(107, 'Puma'),
(108, 'Zara'),
(109, 'Raymond'),
(110, 'Philips'),
(111, 'Whirlpool'),
(112, 'Haier'),
(113, 'IFB'),
(114, 'Dove'),
(115, 'Nivea'),
(116, 'Lakme'),
(117, 'Mamaearth'),
(118, 'Tata'),
(119, 'Amul'),
(120, 'Nestle'),
(121, 'Britannia');

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `Comp_Id` int(11) DEFAULT NULL,
  `Comp_NM` varchar(200) DEFAULT NULL,
  `Comp_Addr` varchar(300) DEFAULT NULL,
  `Comp_Phone` varchar(50) DEFAULT NULL,
  `Comp_Email` varchar(400) DEFAULT NULL,
  `Comp_city` varchar(100) DEFAULT NULL,
  `Comp_Descr` text DEFAULT NULL,
  `Comp_Password` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`Comp_Id`, `Comp_NM`, `Comp_Addr`, `Comp_Phone`, `Comp_Email`, `Comp_city`, `Comp_Descr`, `Comp_Password`) VALUES
(401, 'Apple Inc.', 'Cupertino,CA,USA', '2345768709', 'contact@apple.com', 'Cupertino', 'Global tech company known for iPhone and Mac', 'Apple_123'),
(402, 'Samsung Electronics', 'Suwon,South Korea', '7846877609', 'support@samsung.com', 'Suwon', 'Electronics and smartphone manufacturing leader', 'Samsung_223'),
(403, 'Dell Technologies', 'Round Rock,TX,USA', '1800244560', 'help@dell.com', 'Round Rock', 'PCs,laptops, and enterprise solutions', 'Dell_789'),
(404, 'HP Inc.', 'Palo Alto,CA,USA', '9012345840', 'support@hp.com', 'Palo Alto', 'Computers and printing products', 'HP_678'),
(405, 'Nike Inc.', 'Beaverton,OR,USA', '2446757600', 'care@nike.com', 'Beaverton', 'Athletic footwear and apparel company', 'Nike_8903'),
(406, 'Adidas AG', 'Herzogenaurach,Germany', '1245391222', 'info@adidas.com', 'Herzogenaurach', 'Global sportswear brand', 'Adidas_657'),
(407, 'Puma SE', 'Herzogenaurach,Germany', '9565235060', 'support@puma.com', 'Herzogenaurach', 'International sportswear company', 'Puma_001'),
(408, 'Zara International', 'Arteixo,Spain', '3498530601', 'help@zara.com', 'Arteixo', 'Global fast-fashion brand', 'Zara_590'),
(409, 'Raymond Ltd.', 'Mumbai,India', '3498530601', 'contact@raymond.in', 'Mumbai', 'Textiles and men`s clothing manufacturer', 'Raymond_590'),
(410, 'Philips India', 'Gurgaon,India', '1700985631', 'care@philips.com', 'Gurgaon', 'Health and home appliances', 'Philips_78900'),
(411, 'Whirlpool India', 'Pune,India', '7865998764', 'support@whirlpool.com', 'Pune', 'Refrigerators and washing machines', 'Whirlpool_007'),
(412, 'Haier India', 'New Delhi,India', '1652350060', 'service@haierindia.com', 'New Delhi', 'Appliances and electronics manufacturer', 'Haier_121'),
(413, 'IFB Industries', 'Bangalore,India', '8700530601', 'info@ifbglobal.com', 'Bangalore', 'Home appliances and solutions', 'IFB_780'),
(414, 'Dove(HUL)', 'Mumbai,India', '7956805660', 'care@hul.co.in', 'Mumbai', 'Personal care brand by Hindustan Unilever', 'Dove_900'),
(415, 'Nivea India', 'Mumbai,India', '5566998764', 'nivea@beiersdorf.com', 'Mumbai', 'Skincare and body care company', 'Nivea_812'),
(416, 'Lakme(HUL)', 'Mumbai,India', '4470891234', 'contact@lakmeindia.com', 'Mumbai', 'Cosmetics brand owned by Hindustan Unilever', 'Lakme_7821'),
(417, 'Mamaearth', 'Gurgaon,India', '6789125670', 'support@mamaearth.in', 'Gurgaon', 'Natural skincare and beauty products', 'Mamaearth_080'),
(418, 'Tata Consumer Products', 'Mumbai,India', '8600546578', 'care@tataconsumer.com', 'Mumbai', 'Salt,tea,and grocery brand of Tata Group', 'Tata_3940'),
(419, 'Amul(GCMMF)', 'Anand,Gujarat', '9745305622', 'info@amul.coop', 'Anand', 'India`s largest dairy and FMCG company', 'Amul_142'),
(420, 'Nestle India', 'Gurgaon,India', '3370895576', 'wecare@in.nestle.com', 'Gurgaon', 'Food and beverage giant', 'Nestle_201'),
(421, 'Britannia Industries', 'Bangalore,India', '8009004556', 'customercare@britindia.com', 'Bangalore', 'Biscuits and bakery product manufacturer', 'britannia_675'),
(422, 'mango', 'sadashivnager', '7895421096', 'mango@gmail.com', 'kolhapur', 'Mano shop', 'Mango@123');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `Cust_Id` int(11) DEFAULT NULL,
  `Cust_Nm` varchar(100) DEFAULT NULL,
  `Cust_Addr` varchar(255) DEFAULT NULL,
  `Cust_Phone` varchar(15) DEFAULT NULL,
  `Cust_Email` varchar(100) DEFAULT NULL,
  `Cust_Pincode` varchar(10) DEFAULT NULL,
  `Cust_Password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`Cust_Id`, `Cust_Nm`, `Cust_Addr`, `Cust_Phone`, `Cust_Email`, `Cust_Pincode`, `Cust_Password`) VALUES
(501, 'ABC', 'pune', '3456329058', 'A@gmail.com', '416210', 'ABC_34'),
(502, 'XYZ', 'mumbai', '3421679040', 'XYZ@gmail.com', '416212', 'xyz123'),
(503, 'Omkar Swami', 'sadashivnager', '9766875410', 'swamiomkar@gmail.com', '416235', 'Omkar@123');

-- --------------------------------------------------------

--
-- Table structure for table `itemcat`
--

CREATE TABLE `itemcat` (
  `Cat_Id` int(11) DEFAULT NULL,
  `Cat_Nm` varchar(400) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `itemcat`
--

INSERT INTO `itemcat` (`Cat_Id`, `Cat_Nm`) VALUES
(201, 'Electronics'),
(202, 'Fashion'),
(203, 'Home Appliances'),
(204, 'Beauty and Personal care'),
(205, 'Grocery and FMCG');

-- --------------------------------------------------------

--
-- Table structure for table `itemmaster`
--

CREATE TABLE `itemmaster` (
  `Item_Id` int(11) DEFAULT NULL,
  `Item_Nm` varchar(500) DEFAULT NULL,
  `Comp_Id` int(11) DEFAULT NULL,
  `Cat_Id` int(11) DEFAULT NULL,
  `Brand_Id` int(11) DEFAULT NULL,
  `Item_Rate` float DEFAULT NULL,
  `Item_Stock` int(11) DEFAULT NULL,
  `Item_Descr` text DEFAULT NULL,
  `Item_Photo` varchar(600) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `itemmaster`
--

INSERT INTO `itemmaster` (`Item_Id`, `Item_Nm`, `Comp_Id`, `Cat_Id`, `Brand_Id`, `Item_Rate`, `Item_Stock`, `Item_Descr`, `Item_Photo`) VALUES
(301, 'iphone', 401, 201, 101, 50000, 15, 'Latest Apple iPhone with 128GB storage', '301_iphone 14.png'),
(302, 'Samsung Galaxy S23', 402, 201, 102, 25000, 25, 'Samsung flagship with AMOLED display', '302_Samsung  galaxy  s23.png'),
(303, 'Dell Inspiron 15', 403, 201, 103, 45000, 7, '15-inch laptop with i5 processor', '303_dell laptop15.png'),
(305, 'Nike Running Shoes', 405, 202, 105, 4999, 47, 'Lightweight and comfortable', '305_shoes.jpg'),
(306, 'watch', 402, 201, 102, 25000, 18, 'watch', '306_digital watch.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `orderdetails`
--

CREATE TABLE `orderdetails` (
  `Order_DetId` int(11) DEFAULT NULL,
  `Order_Id` int(11) DEFAULT NULL,
  `Item_Id` int(11) DEFAULT NULL,
  `Item_Rate` decimal(10,2) DEFAULT NULL,
  `Item_Qty` int(11) DEFAULT NULL,
  `Item_Amt` decimal(10,2) DEFAULT NULL,
  `Comp_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderdetails`
--

INSERT INTO `orderdetails` (`Order_DetId`, `Order_Id`, `Item_Id`, `Item_Rate`, `Item_Qty`, `Item_Amt`, `Comp_id`) VALUES
(1, 1, 303, '45000.00', 1, '45000.00', 403),
(2, 1, 302, '25000.00', 2, '50000.00', 402),
(3, 1, 306, '25000.00', 1, '25000.00', 402),
(4, 2, 302, '25000.00', 1, '25000.00', 402),
(5, 2, 305, '4999.00', 2, '9998.00', 405);

-- --------------------------------------------------------

--
-- Table structure for table `ordermaster`
--

CREATE TABLE `ordermaster` (
  `Order_Id` int(11) DEFAULT NULL,
  `Order_Date` date DEFAULT NULL,
  `OrderCust_Id` int(11) DEFAULT NULL,
  `Order_Amt` decimal(10,2) DEFAULT NULL,
  `Order_GSTAmt` decimal(10,2) DEFAULT NULL,
  `Order_GrandTot` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ordermaster`
--

INSERT INTO `ordermaster` (`Order_Id`, `Order_Date`, `OrderCust_Id`, `Order_Amt`, `Order_GSTAmt`, `Order_GrandTot`) VALUES
(1, '2026-01-27', 503, '120000.00', '6000.00', '126000.00'),
(2, '2026-01-27', 503, '34998.00', '1749.90', '36747.90');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `Pay_Id` int(11) DEFAULT NULL,
  `Pay_Date` date DEFAULT NULL,
  `Order_Id` int(11) DEFAULT NULL,
  `Order_GrandTot` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`Pay_Id`, `Pay_Date`, `Order_Id`, `Order_GrandTot`) VALUES
(1, '2026-01-21', 1, '31073.00'),
(2, '2026-01-21', 2, '218500.00'),
(3, '2026-01-21', 3, '63.00'),
(4, '2026-01-27', 4, '133350.00'),
(5, '2026-01-27', 1, '138598.95'),
(6, '2026-01-27', 2, '173250.00'),
(7, '2026-01-27', 1, '126000.00'),
(8, '2026-01-27', 2, '36747.90');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
