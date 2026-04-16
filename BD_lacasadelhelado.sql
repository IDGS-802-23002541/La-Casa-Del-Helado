CREATE DATABASE  IF NOT EXISTS `casadelhelado` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `casadelhelado`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: casadelhelado
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Lácteos'),(2,'Endulzantes'),(3,'Estabilizantes y Aditivos'),(4,'Frutas y Pulpas'),(5,'Saborizantes y Pastas'),(6,'Insumos de Ensamble'),(7,'Nieve'),(8,'Paletas'),(9,'Troles');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente_externo`
--

DROP TABLE IF EXISTS `cliente_externo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente_externo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `fechaRegistro` datetime DEFAULT NULL,
  `estatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente_externo`
--

LOCK TABLES `cliente_externo` WRITE;
/*!40000 ALTER TABLE `cliente_externo` DISABLE KEYS */;
INSERT INTO `cliente_externo` VALUES (1,'Juan','López','juan@gmail.com','$2b$12$clienteHash','4771111111','2026-04-10 10:00:00',1),(2,'María','Hernández','maria@gmail.com','$2b$12$clienteHash','4772222222','2026-04-10 10:10:00',1),(3,'Carlos','Ramírez','carlos@gmail.com','$2b$12$clienteHash','4773333333','2026-04-10 10:20:00',1),(4,'Fernanda','García','fernanda@gmail.com','$2b$12$clienteHash','4774444444','2026-04-10 10:30:00',1),(5,'Luis','Martínez','luis@gmail.com','$2b$12$clienteHash','4775555555','2026-04-10 10:40:00',1),(6,'Ana','Torres','ana@gmail.com','$2b$12$clienteHash','4776666666','2026-04-10 10:50:00',1),(7,'Pedro','Sánchez','pedro@gmail.com','$2b$12$clienteHash','4777777777','2026-04-10 11:00:00',1),(8,'Sofía','Flores','sofia@gmail.com','$2b$12$clienteHash','4778888888','2026-04-10 11:10:00',1),(9,'Diego','Vargas','diego@gmail.com','$2b$12$clienteHash','4779999999','2026-04-10 11:20:00',1),(10,'Lucía','Reyes','lucia@gmail.com','$2b$12$clienteHash','4770000000','2026-04-10 11:30:00',1),(11,'Aidee','Casillas','aideecasillas14@gmail.com','scrypt:32768:8:1$kxFdGuNTcHYtWdJ2$43a3321112d6c0d669913410b8d0b060da5930fca90d8f46dc372c610fe1af60f3617443071868c050e20fa9c93a932f31246a03b0eca3e63a991a8b267e49fb','4772943651','2026-04-15 17:08:59',1),(12,'damian','rdz','damian@gmail.com','scrypt:32768:8:1$ZXS02XhrGhOgxU78$a4450262aae7bf81e661425caeb0e45008c3fe362516090c5ca3a6d7db40dd9b4d89d466b2c59e99ca92c3a6edfe2026658883c84e4246de7f6cf7fd2668cebb','4723627422','2026-04-15 20:32:22',1);
/*!40000 ALTER TABLE `cliente_externo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compra`
--

DROP TABLE IF EXISTS `compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `factura` varchar(50) NOT NULL,
  `fechaCompra` date DEFAULT NULL,
  `idProveedor` int NOT NULL,
  `idUsuario` int NOT NULL,
  `estatus` tinyint(1) DEFAULT NULL,
  `fechaEliminacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idProveedor` (`idProveedor`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`idProveedor`) REFERENCES `proveedor` (`id`),
  CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compra`
--

LOCK TABLES `compra` WRITE;
/*!40000 ALTER TABLE `compra` DISABLE KEYS */;
INSERT INTO `compra` VALUES (1,'LB-2026-0310','2026-03-10',1,1,1,NULL),(2,'ST-2026-0312','2026-03-12',3,1,1,NULL),(3,'IF-2026-0314','2026-03-14',10,1,1,NULL),(4,'EH-2026-0317','2026-03-17',5,1,1,NULL),(5,'LV-2026-0320','2026-03-20',2,1,1,NULL),(6,'AD-2026-0324','2026-03-24',8,1,1,NULL),(7,'PB-2026-0328','2026-03-28',6,1,1,NULL),(8,'QI-2026-0401','2026-04-01',13,1,1,NULL),(9,'LB-2026-0403','2026-04-03',1,1,1,NULL),(10,'FM-2026-0407','2026-04-07',4,1,1,NULL),(11,'EH-2026-0410','2026-04-10',5,1,1,NULL),(12,'EL-2026-0415','2026-04-15',11,1,1,NULL),(13,'FAC23','2026-04-15',1,1,1,NULL);
/*!40000 ALTER TABLE `compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversiones`
--

DROP TABLE IF EXISTS `conversiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversiones` (
  `unidadBase` varchar(20) NOT NULL,
  `presentacion` varchar(20) NOT NULL,
  `factor` decimal(10,2) NOT NULL,
  PRIMARY KEY (`unidadBase`,`presentacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversiones`
--

LOCK TABLES `conversiones` WRITE;
/*!40000 ALTER TABLE `conversiones` DISABLE KEYS */;
INSERT INTO `conversiones` VALUES ('g','250g',250.00),('g','500g',500.00),('g','g',1.00),('g','kg',1000.00),('L','L',1.00),('L','ml',0.00),('ml','galon',3785.00),('ml','L',1000.00),('ml','medio_galon',1892.00),('ml','ml',1.00),('pza','100 pzas',100.00),('pza','200 pzas',200.00),('pza','500 pzas',500.00),('pza','caja_12',12.00),('pza','docena',12.00),('pza','pza',1.00);
/*!40000 ALTER TABLE `conversiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_compra`
--

DROP TABLE IF EXISTS `detalle_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idCompra` int NOT NULL,
  `idMateriaPrima` int NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `contenidoNeto` varchar(20) DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idCompra` (`idCompra`),
  KEY `idMateriaPrima` (`idMateriaPrima`),
  CONSTRAINT `detalle_compra_ibfk_1` FOREIGN KEY (`idCompra`) REFERENCES `compra` (`id`),
  CONSTRAINT `detalle_compra_ibfk_2` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_compra`
--

LOCK TABLES `detalle_compra` WRITE;
/*!40000 ALTER TABLE `detalle_compra` DISABLE KEYS */;
INSERT INTO `detalle_compra` VALUES (1,1,1,40.00,'1 L',640.00),(2,1,2,15.00,'1 L',525.00),(3,1,3,8.00,'1 L',280.00),(4,1,4,6.00,'1 kg',300.00),(5,1,5,10.00,'1 kg',350.00),(6,2,16,3.00,'1 kg',720.00),(7,2,18,3.00,'1 kg',660.00),(8,2,19,2.00,'1 kg',600.00),(9,2,17,2.00,'1 L',480.00),(10,3,8,2.00,'500g',360.00),(11,3,20,400.00,'200 pzas',320.00),(12,3,21,400.00,'100 pzas',240.00),(13,3,22,1000.00,'500 pzas',190.00),(14,4,11,8.00,'1 kg',240.00),(15,4,12,10.00,'1 kg',200.00),(16,4,13,8.00,'1 kg',160.00),(17,4,14,5.00,'1 kg',125.00),(18,4,15,10.00,'1 kg',150.00),(19,5,1,40.00,'1 L',640.00),(20,5,2,15.00,'1 L',525.00),(21,5,3,10.00,'1 L',350.00),(22,6,6,50.00,'1 kg',1250.00),(23,6,7,10.00,'1 kg',400.00),(24,7,11,6.00,'1 kg',180.00),(25,7,12,8.00,'1 kg',160.00),(26,7,15,8.00,'1 kg',120.00),(27,8,8,2.00,'500g',360.00),(28,8,9,8.00,'1 L',120.00),(29,9,1,50.00,'1 L',800.00),(30,9,2,20.00,'1 L',700.00),(31,9,3,12.00,'1 L',420.00),(32,9,5,12.00,'1 kg',420.00),(33,10,16,3.00,'1 kg',720.00),(34,10,18,2.00,'1 kg',440.00),(35,10,17,2.00,'1 L',480.00),(36,11,11,10.00,'1 kg',300.00),(37,11,12,10.00,'1 kg',200.00),(38,11,14,6.00,'1 kg',150.00),(39,11,15,10.00,'1 kg',150.00),(40,11,13,8.00,'1 kg',160.00),(41,12,20,400.00,'200 pzas',320.00),(42,12,21,400.00,'100 pzas',240.00),(43,12,22,1000.00,'500 pzas',190.00),(44,13,1,3.00,'L',50.00);
/*!40000 ALTER TABLE `detalle_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idPedido` int NOT NULL,
  `idPresentacion` int NOT NULL,
  `cantidad` int NOT NULL,
  `precioUnitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idPedido` (`idPedido`),
  KEY `idPresentacion` (`idPresentacion`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`id`),
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`idPresentacion`) REFERENCES `presentacion_venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
INSERT INTO `detalle_pedido` VALUES (1,1,1,2,18.00),(2,1,20,2,9.00),(3,2,14,1,150.00),(4,3,18,2,22.00),(5,4,14,1,150.00),(6,4,16,1,140.00),(7,4,20,3,9.00),(8,4,23,2,8.00),(9,5,1,4,18.00),(10,5,18,2,22.00),(11,6,15,1,140.00),(12,6,21,3,9.00),(13,6,23,2,8.00),(14,7,19,2,22.00),(15,8,14,1,150.00),(16,8,8,4,18.00),(17,9,1,4,18.00),(18,9,20,2,9.00),(19,9,22,2,9.00),(20,10,14,1,150.00),(21,11,16,1,140.00),(22,12,15,2,140.00),(23,12,18,2,22.00),(24,12,22,1,9.00),(25,13,18,4,22.00),(26,13,25,12,13.00),(27,14,1,2,18.00),(28,14,20,2,9.00),(29,15,14,1,150.00),(30,16,18,2,22.00),(31,17,14,1,150.00),(32,17,16,1,140.00),(33,17,20,3,9.00),(34,17,23,2,8.00),(35,18,1,4,18.00),(36,18,18,2,22.00),(37,19,15,1,140.00),(38,19,21,3,9.00),(39,19,23,2,8.00),(40,20,1,1,18.00),(41,20,2,2,18.00);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_receta`
--

DROP TABLE IF EXISTS `detalle_receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_receta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idReceta` int NOT NULL,
  `idMateriaPrima` int NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `unidad` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idReceta` (`idReceta`),
  KEY `idMateriaPrima` (`idMateriaPrima`),
  CONSTRAINT `detalle_receta_ibfk_1` FOREIGN KEY (`idReceta`) REFERENCES `receta` (`id`),
  CONSTRAINT `detalle_receta_ibfk_2` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_receta`
--

LOCK TABLES `detalle_receta` WRITE;
/*!40000 ALTER TABLE `detalle_receta` DISABLE KEYS */;
INSERT INTO `detalle_receta` VALUES (1,1,1,2500.00,'ml'),(2,1,2,800.00,'ml'),(3,1,6,600.00,'g'),(4,1,4,120.00,'g'),(5,1,7,80.00,'g'),(6,1,8,12.00,'g'),(7,1,16,150.00,'g'),(8,2,1,2500.00,'ml'),(9,2,2,800.00,'ml'),(10,2,6,600.00,'g'),(11,2,4,120.00,'g'),(12,2,7,80.00,'g'),(13,2,8,12.00,'g'),(14,2,17,80.00,'ml'),(15,3,1,2500.00,'ml'),(16,3,2,800.00,'ml'),(17,3,6,600.00,'g'),(18,3,4,120.00,'g'),(19,3,7,80.00,'g'),(20,3,8,12.00,'g'),(21,3,11,1000.00,'g'),(22,4,1,2500.00,'ml'),(23,4,2,800.00,'ml'),(24,4,6,600.00,'g'),(25,4,4,120.00,'g'),(26,4,7,80.00,'g'),(27,4,8,12.00,'g'),(28,4,18,150.00,'g'),(29,5,1,2500.00,'ml'),(30,5,2,800.00,'ml'),(31,5,6,600.00,'g'),(32,5,4,120.00,'g'),(33,5,7,80.00,'g'),(34,5,8,12.00,'g'),(35,5,19,100.00,'g'),(36,6,1,2500.00,'ml'),(37,6,2,800.00,'ml'),(38,6,6,600.00,'g'),(39,6,4,120.00,'g'),(40,6,7,80.00,'g'),(41,6,8,12.00,'g'),(42,6,14,1000.00,'g'),(43,7,3,1500.00,'ml'),(44,7,1,600.00,'ml'),(45,7,2,400.00,'ml'),(46,7,6,300.00,'g'),(47,7,5,200.00,'g'),(48,7,8,8.00,'g'),(49,7,12,1000.00,'g'),(50,8,3,1500.00,'ml'),(51,8,1,600.00,'ml'),(52,8,2,400.00,'ml'),(53,8,6,300.00,'g'),(54,8,5,200.00,'g'),(55,8,8,8.00,'g'),(56,8,11,1000.00,'g'),(57,9,10,1000.00,'ml'),(58,9,12,700.00,'g'),(59,9,6,280.00,'g'),(60,9,9,30.00,'ml'),(61,9,8,4.00,'g'),(62,9,22,20.00,'pza'),(63,10,10,1000.00,'ml'),(64,10,13,700.00,'g'),(65,10,6,280.00,'g'),(66,10,9,30.00,'ml'),(67,10,8,4.00,'g'),(68,10,22,20.00,'pza'),(69,11,10,1000.00,'ml'),(70,11,14,700.00,'g'),(71,11,6,280.00,'g'),(72,11,9,30.00,'ml'),(73,11,8,4.00,'g'),(74,11,22,20.00,'pza'),(75,12,10,1000.00,'ml'),(76,12,15,1000.00,'g'),(77,12,6,280.00,'g'),(78,12,8,4.00,'g'),(79,12,22,20.00,'pza'),(80,13,1,1000.00,'ml'),(81,13,2,400.00,'ml'),(82,13,5,300.00,'g'),(83,13,6,150.00,'g'),(84,13,16,120.00,'g'),(85,13,8,6.00,'g'),(86,13,22,18.00,'pza'),(87,14,1,1000.00,'ml'),(88,14,2,400.00,'ml'),(89,14,5,300.00,'g'),(90,14,6,150.00,'g'),(91,14,18,120.00,'g'),(92,14,8,6.00,'g'),(93,14,22,18.00,'pza'),(94,15,1,1000.00,'ml'),(95,15,2,400.00,'ml'),(96,15,5,300.00,'g'),(97,15,6,150.00,'g'),(98,15,17,80.00,'ml'),(99,15,8,6.00,'g'),(100,15,22,18.00,'pza');
/*!40000 ALTER TABLE `detalle_receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalleventa`
--

DROP TABLE IF EXISTS `detalleventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleventa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idProducto` int NOT NULL,
  `idVenta` int NOT NULL,
  `idPresentacion` int DEFAULT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `precioUnitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idProducto` (`idProducto`),
  KEY `idVenta` (`idVenta`),
  KEY `idPresentacion` (`idPresentacion`),
  CONSTRAINT `detalleventa_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`),
  CONSTRAINT `detalleventa_ibfk_2` FOREIGN KEY (`idVenta`) REFERENCES `venta` (`id`),
  CONSTRAINT `detalleventa_ibfk_3` FOREIGN KEY (`idPresentacion`) REFERENCES `presentacion_venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleventa`
--

LOCK TABLES `detalleventa` WRITE;
/*!40000 ALTER TABLE `detalleventa` DISABLE KEYS */;
INSERT INTO `detalleventa` VALUES (1,1,1,1,2.00,18.00),(2,9,1,20,2.00,9.00),(3,1,2,1,4.00,18.00),(4,3,2,8,2.00,14.00),(5,7,2,18,1.00,22.00),(6,13,2,24,2.00,13.00),(7,2,3,5,3.00,14.00),(8,10,3,21,2.00,9.00),(9,4,4,10,2.00,16.00),(10,12,4,23,2.00,8.00),(11,1,5,1,3.00,18.00),(12,7,5,18,1.00,22.00),(13,8,5,19,1.00,22.00),(14,9,6,20,2.00,9.00),(15,12,6,23,2.00,8.00),(16,5,7,12,2.00,15.00),(17,12,7,23,1.00,8.00),(18,1,8,1,5.00,18.00),(19,3,9,8,3.00,14.00),(20,2,9,5,2.00,14.00),(21,9,10,20,1.00,9.00),(22,11,10,22,1.00,9.00),(23,12,10,23,1.00,8.00),(24,1,11,1,3.00,18.00),(25,13,11,24,2.00,13.00),(26,7,11,18,1.00,22.00),(27,1,12,14,1.00,150.00),(28,8,13,19,2.00,22.00),(29,1,14,1,5.00,18.00),(30,4,14,10,2.00,16.00),(31,8,14,19,1.00,22.00),(32,3,15,8,3.00,14.00),(33,5,15,12,2.00,15.00),(34,9,16,20,2.00,9.00),(35,14,16,25,2.00,13.00),(36,2,17,5,2.00,14.00),(37,9,17,20,2.00,9.00),(38,13,18,24,3.00,13.00),(39,7,18,18,1.00,22.00),(40,1,19,1,6.00,18.00),(41,3,19,8,4.00,14.00),(42,9,20,20,2.00,9.00),(43,12,20,23,2.00,8.00),(44,6,21,13,3.00,15.00),(45,1,21,1,3.00,18.00),(46,10,22,21,2.00,9.00),(47,11,22,22,2.00,9.00),(48,1,23,14,1.00,150.00),(49,3,23,16,1.00,140.00),(50,9,23,20,5.00,9.00),(51,1,24,1,2.00,18.00),(52,13,24,24,2.00,13.00),(53,1,25,1,4.00,18.00),(54,2,25,5,2.00,14.00),(55,7,25,18,1.00,22.00),(56,3,26,8,3.00,14.00),(57,12,26,23,2.00,8.00),(58,10,26,21,1.00,9.00),(59,1,27,1,6.00,18.00),(60,3,27,8,3.00,14.00),(61,7,27,18,2.00,22.00),(62,9,27,20,2.00,9.00),(63,1,28,1,4.00,18.00),(64,4,28,10,2.00,16.00),(65,2,29,5,6.00,14.00),(66,13,29,24,4.00,13.00),(67,8,29,19,1.00,22.00),(68,12,30,23,2.00,8.00),(69,10,30,21,2.00,9.00),(70,7,47,18,1.00,22.00),(71,9,48,20,3.00,9.00),(72,9,50,20,1.00,9.00),(73,2,51,5,1.00,18.00),(74,1,52,4,2.00,34.00),(75,7,53,18,1.00,22.00),(76,1,54,14,2.00,150.00),(77,1,54,2,1.00,18.00),(78,7,55,18,1.00,22.00),(79,1,56,4,1.00,34.00),(80,1,57,14,1.00,150.00);
/*!40000 ALTER TABLE `detalleventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materia_prima`
--

DROP TABLE IF EXISTS `materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materia_prima` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `unidadBase` varchar(20) NOT NULL,
  `stockActual` decimal(10,2) DEFAULT NULL,
  `stockMinimo` decimal(10,2) DEFAULT NULL,
  `idCategoria` int NOT NULL,
  `estatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idCategoria` (`idCategoria`),
  CONSTRAINT `materia_prima_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materia_prima`
--

LOCK TABLES `materia_prima` WRITE;
/*!40000 ALTER TABLE `materia_prima` DISABLE KEYS */;
INSERT INTO `materia_prima` VALUES (1,'Leche entera','ml',78000.00,10000.00,1,1),(2,'Crema para batir','ml',16400.00,2500.00,1,1),(3,'Yogur natural entero','ml',15000.00,5000.00,1,1),(4,'Leche en polvo descremada','g',5160.00,600.00,1,1),(5,'Leche condensada','g',5000.00,5000.00,1,1),(6,'Azúcar estándar','g',53800.00,5000.00,2,1),(7,'Dextrosa','g',7840.00,1000.00,2,1),(8,'Estabilizante CMC','g',976.00,100.00,3,1),(9,'Jugo de limón natural','ml',4000.00,500.00,3,1),(10,'Agua purificada','ml',80000.00,10000.00,4,1),(11,'Fresas frescas','g',12000.00,2000.00,4,1),(12,'Guayaba fresca','g',10000.00,2000.00,4,1),(13,'Tuna fresca','g',8000.00,1500.00,4,1),(14,'Xoconostle fresco','g',5000.00,4000.00,4,1),(15,'Limón (fruta)','g',6000.00,1000.00,4,1),(16,'Pasta de cajeta','g',3450.00,500.00,5,1),(17,'Extracto de vainilla','ml',1120.00,200.00,5,1),(18,'Pasta de chocolate','g',2700.00,500.00,5,1),(19,'Pasta de elote','g',1500.00,300.00,5,1),(20,'Conos wafer','pza',90.00,80.00,6,1),(21,'Vasos desechables 250 ml','pza',600.00,60.00,6,1),(22,'Palitos de paleta','pza',1200.00,200.00,6,1);
/*!40000 ALTER TABLE `materia_prima` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merma`
--

DROP TABLE IF EXISTS `merma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merma` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idMateriaPrima` int DEFAULT NULL,
  `idProducto` int DEFAULT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `unidad` varchar(20) NOT NULL,
  `justificacion` varchar(200) NOT NULL,
  `fecha` date NOT NULL,
  `estatus` tinyint(1) DEFAULT NULL,
  `fechaEliminacion` datetime DEFAULT NULL,
  `idUsuario` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idMateriaPrima` (`idMateriaPrima`),
  KEY `idProducto` (`idProducto`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `merma_ibfk_1` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`id`),
  CONSTRAINT `merma_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`),
  CONSTRAINT `merma_ibfk_3` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`id`),
  CONSTRAINT `check_merma_origen` CHECK ((((`idMateriaPrima` is not null) and (`idProducto` is null)) or ((`idMateriaPrima` is null) and (`idProducto` is not null))))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merma`
--

LOCK TABLES `merma` WRITE;
/*!40000 ALTER TABLE `merma` DISABLE KEYS */;
INSERT INTO `merma` VALUES (1,11,NULL,500.00,'g','Fresas con hongos al revisar entrada de compra','2026-04-12',1,NULL,2),(2,12,NULL,800.00,'g','Guayaba fermentada, no llegó en condición adecuada','2026-04-12',1,NULL,3),(3,NULL,9,3.00,'pza','Paletas de guayaba rotas al desmoldar lote matutino','2026-04-12',0,'2026-04-15 18:08:25',4),(4,1,NULL,2000.00,'ml','Leche con variación de temperatura por falla eléctrica','2026-04-13',1,NULL,2),(5,NULL,3,4.00,'L','Nieve de fresa con cristalización excesiva, descartada','2026-04-13',1,NULL,3),(6,11,NULL,300.00,'g','Fresas residuales del día anterior no refrigeradas','2026-04-14',1,NULL,4),(7,NULL,7,2.00,'pza','Troles de guayaba con empaque roto en congelador','2026-04-14',1,NULL,2),(8,15,NULL,600.00,'g','Limón reseco, no apto para producción','2026-04-15',1,NULL,3),(9,NULL,12,2.00,'pza','Paletas de limón con palito mal insertado, no vendibles','2026-04-15',1,NULL,4);
/*!40000 ALTER TABLE `merma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `folio` varchar(20) NOT NULL,
  `idCliente` int NOT NULL,
  `fechaPedido` datetime NOT NULL,
  `fechaRecogida` datetime DEFAULT NULL,
  `estatus` varchar(30) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `folio` (`folio`),
  KEY `idCliente` (`idCliente`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `cliente_externo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'PED-AB12CD34',1,'2026-04-12 11:00:00','2026-04-13 17:30:00','Listo para recoger',68.00),(2,'PED-EF56GH78',2,'2026-04-12 12:15:00','2026-04-13 10:00:00','En preparación',150.00),(3,'PED-IJ90KL12',3,'2026-04-12 18:00:00','2026-04-14 11:00:00','Pago en proceso',44.00),(4,'PED-MN34OP56',4,'2026-04-13 09:30:00','2026-04-14 16:00:00','En preparación',280.00),(5,'PED-QR78ST90',5,'2026-04-13 11:00:00','2026-04-15 10:00:00','Pendiente de pago',96.00),(6,'PED-UV12WX34',6,'2026-04-14 10:00:00','2026-04-15 17:00:00','En preparación',130.00),(7,'PED-YZ56AB78',7,'2026-04-14 13:30:00','2026-04-16 10:00:00','Pendiente de pago',44.00),(8,'PED-CD90EF12',8,'2026-04-15 09:00:00','2026-04-16 17:30:00','En preparación',162.00),(9,'PED-GH34IJ56',9,'2026-04-15 14:00:00','2026-04-17 11:00:00','Pendiente de pago',88.00),(10,'PED-KL78MN90',10,'2026-04-15 16:00:00','2026-04-17 16:00:00','Pendiente de pago',150.00),(11,'PED-7A8DD2AE',11,'2026-04-15 17:30:36','2026-04-15 18:45:00','entregado',140.00),(12,'PED-827BDAF3',11,'2026-04-15 17:33:41','2026-04-15 18:45:00','Pagado',333.00),(13,'PED-D799FB8C',11,'2026-04-15 17:34:38','2026-04-16 13:00:00','Pagado',244.00),(14,'PED-ABCDEFGH',1,'2026-04-15 11:00:00','2026-04-15 10:00:00','pagado',68.00),(15,'PED-IJKLMNOP',2,'2026-04-15 12:15:00','2026-04-15 10:00:00','pagado',150.00),(16,'PED-QRSTUVWX',3,'2026-04-15 18:00:00','2026-04-15 10:00:00','listo_entrega',44.00),(17,'PED-ZQBCDEFG',4,'2026-04-15 09:30:00','2026-04-15 10:00:00','listo_entrega',280.00),(18,'PED-HIJKLMNO',5,'2026-04-15 11:00:00','2026-04-15 10:00:00','entregado',96.00),(19,'PED-IPOOFSDIJ',6,'2026-04-15 10:00:00','2026-04-15 10:00:00','entregado',130.00),(20,'PED-95DCD634',12,'2026-04-15 20:34:19','2026-04-16 13:00:00','Pagado',54.00);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presentacion_venta`
--

DROP TABLE IF EXISTS `presentacion_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presentacion_venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `idProductoBase` int NOT NULL,
  `equivalencia` decimal(10,4) NOT NULL,
  `estatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idProductoBase` (`idProductoBase`),
  CONSTRAINT `presentacion_venta_ibfk_1` FOREIGN KEY (`idProductoBase`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presentacion_venta`
--

LOCK TABLES `presentacion_venta` WRITE;
/*!40000 ALTER TABLE `presentacion_venta` DISABLE KEYS */;
INSERT INTO `presentacion_venta` VALUES (1,'Cono sencillo – Cajeta (1 bola)',18.00,1,0.1000,1),(2,'Vaso sencillo – Cajeta (1 bola)',18.00,1,0.1000,1),(3,'Cono doble – Cajeta (2 bolas)',34.00,1,0.2000,1),(4,'Vaso doble – Cajeta (2 bolas)',34.00,1,0.2000,1),(5,'Cono sencillo – Vainilla (1 bola)',18.00,2,0.1000,1),(6,'Vaso sencillo – Vainilla (1 bola)',18.00,2,0.1000,1),(7,'Cono doble – Vainilla (2 bolas)',34.00,2,0.2000,1),(8,'Cono sencillo – Fresa (1 bola)',18.00,3,0.1000,1),(9,'Cono doble – Fresa (2 bolas)',34.00,3,0.2000,1),(10,'Cono sencillo – Chocolate (1 bola)',20.00,4,0.1000,1),(11,'Cono doble – Chocolate (2 bolas)',38.00,4,0.2000,1),(12,'Cono sencillo – Elote (1 bola)',20.00,5,0.1000,1),(13,'Cono sencillo – Xoconostle (1 bola)',20.00,6,0.1000,1),(14,'Litro de Nieve – Cajeta',150.00,1,1.0000,1),(15,'Litro de Nieve – Vainilla',140.00,2,1.0000,1),(16,'Litro de Nieve – Fresa',140.00,3,1.0000,1),(17,'Litro de Nieve – Chocolate',150.00,4,1.0000,1),(18,'Trol de Guayaba',22.00,7,1.0000,1),(19,'Trol de Fresa',22.00,8,1.0000,1),(20,'Paleta de Guayaba',9.00,9,1.0000,1),(21,'Paleta de Tuna',9.00,10,1.0000,1),(22,'Paleta de Xoconostle',9.00,11,1.0000,1),(23,'Paleta de Limón',8.00,12,1.0000,1),(24,'Paleta de Cajeta',13.00,13,1.0000,1),(25,'Paleta de Chocolate',13.00,14,1.0000,1),(26,'Paleta de Vainilla',12.00,15,1.0000,1);
/*!40000 ALTER TABLE `presentacion_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `unidadBase` varchar(20) NOT NULL,
  `stockActual` decimal(10,2) NOT NULL,
  `stockMinimo` decimal(10,2) NOT NULL,
  `costoUnitario` decimal(10,2) NOT NULL,
  `idCategoria` int NOT NULL,
  `estatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `idCategoria` (`idCategoria`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Nieve de Cajeta','L',26.00,5.00,18.00,7,1),(2,'Nieve de Vainilla','L',21.40,5.00,14.00,7,1),(3,'Nieve de Fresa','L',18.00,5.00,14.00,7,1),(4,'Nieve de Chocolate','L',24.00,5.00,16.00,7,1),(5,'Nieve de Elote','L',8.00,5.00,15.00,7,1),(6,'Nieve de Xoconostle','L',10.00,3.50,15.00,7,1),(7,'Trol de Guayaba','pza',3.00,5.00,22.00,9,1),(8,'Trol de Fresa','pza',3.00,5.00,22.00,9,1),(9,'Paleta de Guayaba','pza',19.00,10.00,9.00,8,1),(10,'Paleta de Tuna','pza',18.00,10.00,9.00,8,1),(11,'Paleta de Xoconostle','pza',14.00,10.00,9.00,8,1),(12,'Paleta de Limón','pza',20.00,10.00,8.00,8,1),(13,'Paleta de Cajeta','pza',18.00,8.00,13.00,8,1),(14,'Paleta de Chocolate','pza',4.00,8.00,13.00,8,1),(15,'Paleta de Vainilla','pza',17.00,8.00,12.00,8,1);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `razonSocial` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `estatus` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'Lácteos del Bajío S.A. de C.V.','ventas@lacteosbajio.com.mx','4771234567','Blvd. Insurgentes 450, Guanajuato, Gto.','Activo'),(2,'Distribuidora La Vaquita S.A.','pedidos@lavaquita.mx','4779012345','Carr. León-Silao Km 4, León, Gto.','Activo'),(3,'Distribuidora de Sabores TAFER','pedidos@saborestafer.mx','4779876543','Calz. de los Héroes 118, León, Gto.','Activo'),(4,'Grupo FLEMIR Insumos Alimentarios','ventas@flemir.com.mx','4776543210','Av. Tecnológico 890, León, Gto.','Activo'),(5,'Frutería El Huerto de León','elhuerto@frutasyfrutas.com','4772345678','Mercado Hidalgo Local 45, León, Gto.','Activo'),(6,'Pulpas y Frutas del Bajío','ventas@pulpasbajio.mx','4778901234','Blvd. Juan Alonso de Torres 202, León, Gto.','Activo'),(7,'Frutería San Marcos','frutsanmarcos@hotmail.com','4773456789','Mercado San Marcos Local 12, León, Gto.','Activo'),(8,'Insumos Dulces del Centro S.A.','contacto@insumosdc.com.mx','4774567890','Av. Insurgentes 310, Irapuato, Gto.','Activo'),(9,'Azúcar y Derivados AGMEX','ventas@agmex.com.mx','4775678901','Carr. Silao-Guanajuato Km 2, Silao, Gto.','Activo'),(10,'Insumos Fríos del Centro','compras@insumosfrios.mx','4773456789','Av. Juárez 230, Silao, Gto.','Activo'),(11,'Envases y Empaques León S.A.','ventas@envleon.com.mx','4776789012','Blvd. Aeropuerto 770, León, Gto.','Activo'),(12,'Plastiverde Empaques de México','contacto@plastiverde.mx','4777890123','Zona Industrial Oriente, León, Gto.','Activo'),(13,'Quimicalia Industrial S.A. de C.V.','pedidos@quimicalia.com.mx','4778901234','Av. De La Luz 580, Guadalajara, Jal.','Activo'),(14,'Purificadora El Manantial León','ventas@manantialleon.mx','4774321098','Blvd. Torres Landa 1050, León, Gto.','Activo'),(15,'Distribuidora Integral Loperena','compras@loperena.mx','4779876001','Blvd. Mariano Escobedo 440, León, Gto.','Activo');
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta`
--

DROP TABLE IF EXISTS `receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `idProducto` int DEFAULT NULL,
  `cantidadProducida` decimal(10,2) NOT NULL,
  `estatus` tinyint(1) NOT NULL,
  `costoProduccion` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta`
--

LOCK TABLES `receta` WRITE;
/*!40000 ALTER TABLE `receta` DISABLE KEYS */;
INSERT INTO `receta` VALUES (1,'Base Neutra – Cajeta',1,5.00,1,126.52),(2,'Base Neutra – Vainilla',2,5.00,1,109.72),(3,'Base Neutra – Fresa',3,5.00,1,120.52),(4,'Base Neutra – Chocolate',4,5.00,1,123.52),(5,'Base Neutra – Elote',5,5.00,1,90.52),(6,'Base Neutra – Xoconostle',6,5.00,1,115.52),(7,'Base Trol – Guayaba',7,11.00,1,113.48),(8,'Base Trol – Fresa',8,11.00,1,123.48),(9,'Paleta de Agua – Guayaba',9,19.00,1,22.89),(10,'Paleta de Agua – Tuna',10,19.00,1,22.89),(11,'Paleta de Agua – Xoconostle',11,19.00,1,26.39),(12,'Paleta de Agua – Limón',12,19.00,1,23.44),(13,'Paleta de Leche – Cajeta',13,17.00,1,75.21),(14,'Paleta de Leche – Chocolate',14,17.00,1,72.81),(15,'Paleta de Leche – Vainilla',15,17.00,1,65.61);
/*!40000 ALTER TABLE `receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'Administrador'),(2,'Produccion'),(3,'Mostrador'),(4,'Cliente');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_usuarios`
--

DROP TABLE IF EXISTS `roles_usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_usuarios` (
  `usuario_id` int DEFAULT NULL,
  `rol_id` int DEFAULT NULL,
  KEY `usuario_id` (`usuario_id`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `roles_usuarios_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `roles_usuarios_ibfk_2` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_usuarios`
--

LOCK TABLES `roles_usuarios` WRITE;
/*!40000 ALTER TABLE `roles_usuarios` DISABLE KEYS */;
INSERT INTO `roles_usuarios` VALUES (3,2),(4,2),(5,2),(7,3),(8,3),(2,2),(6,3),(1,1);
/*!40000 ALTER TABLE `roles_usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitud_produccion`
--

DROP TABLE IF EXISTS `solicitud_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitud_produccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idProducto` int NOT NULL,
  `idUsuario` int NOT NULL,
  `fecha_solicitud` datetime DEFAULT NULL,
  `estatus` varchar(50) DEFAULT NULL,
  `idReceta` int NOT NULL,
  `lotes` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idProducto` (`idProducto`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idReceta` (`idReceta`),
  CONSTRAINT `solicitud_produccion_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`id`),
  CONSTRAINT `solicitud_produccion_ibfk_2` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`id`),
  CONSTRAINT `solicitud_produccion_ibfk_3` FOREIGN KEY (`idReceta`) REFERENCES `receta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion`
--

LOCK TABLES `solicitud_produccion` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion` DISABLE KEYS */;
INSERT INTO `solicitud_produccion` VALUES (1,1,2,'2026-04-01 08:00:00','Completada',1,1),(2,9,2,'2026-04-01 08:00:00','Completada',9,1),(3,2,3,'2026-04-02 08:00:00','Completada',2,1),(4,13,3,'2026-04-02 09:00:00','Completada',13,1),(5,3,4,'2026-04-03 08:00:00','Completada',3,1),(6,10,4,'2026-04-03 09:00:00','Completada',10,1),(7,7,2,'2026-04-04 08:00:00','Completada',7,1),(8,4,3,'2026-04-05 08:00:00','Completada',4,1),(9,12,4,'2026-04-05 09:00:00','Completada',12,1),(10,1,2,'2026-04-07 08:00:00','Completada',1,1),(11,14,3,'2026-04-07 09:00:00','Completada',14,1),(12,8,4,'2026-04-08 08:00:00','Completada',8,1),(13,5,2,'2026-04-09 08:00:00','Completada',5,1),(14,11,3,'2026-04-09 09:00:00','Completada',11,1),(15,6,4,'2026-04-10 08:00:00','Completada',6,1),(16,2,2,'2026-04-11 08:00:00','Completada',2,1),(17,15,3,'2026-04-12 08:00:00','Completada',15,1),(18,9,4,'2026-04-12 09:00:00','Completada',9,1),(19,1,2,'2026-04-13 08:00:00','Terminado',1,1),(20,3,3,'2026-04-13 08:30:00','En Proceso',3,1),(21,7,4,'2026-04-13 09:00:00','En Proceso',7,1),(22,4,2,'2026-04-14 08:00:00','Pendiente',4,1),(23,10,3,'2026-04-14 08:00:00','En Proceso',10,1),(24,12,4,'2026-04-14 09:00:00','Pendiente',12,1),(25,2,2,'2026-04-15 08:00:00','Terminado',2,1),(26,8,3,'2026-04-15 08:00:00','Pendiente',8,1),(27,6,6,'2026-04-15 18:35:34','Pendiente',6,2),(28,14,6,'2026-04-15 20:25:44','Pendiente',14,3);
/*!40000 ALTER TABLE `solicitud_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `turno`
--

DROP TABLE IF EXISTS `turno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `turno` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idUsuario` int NOT NULL,
  `apertura` datetime NOT NULL,
  `cierre` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `turno_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turno`
--

LOCK TABLES `turno` WRITE;
/*!40000 ALTER TABLE `turno` DISABLE KEYS */;
INSERT INTO `turno` VALUES (1,6,'2026-04-01 09:00:00','2026-04-01 18:00:00'),(2,7,'2026-04-02 09:00:00','2026-04-02 18:00:00'),(3,8,'2026-04-03 09:00:00','2026-04-03 18:00:00'),(4,6,'2026-04-04 09:00:00','2026-04-04 18:00:00'),(5,7,'2026-04-05 09:00:00','2026-04-05 17:00:00'),(6,8,'2026-04-07 09:00:00','2026-04-07 18:00:00'),(7,6,'2026-04-08 09:00:00','2026-04-08 18:00:00'),(8,7,'2026-04-09 09:00:00','2026-04-09 18:00:00'),(9,8,'2026-04-10 09:00:00','2026-04-10 18:00:00'),(10,6,'2026-04-11 09:00:00','2026-04-11 18:30:00'),(11,7,'2026-04-12 09:00:00','2026-04-12 17:00:00'),(12,8,'2026-04-13 09:00:00','2026-04-13 18:00:00'),(13,6,'2026-04-14 09:00:00','2026-04-14 18:00:00'),(14,7,'2026-04-15 09:00:00','2026-04-15 18:00:00'),(15,8,'2026-04-16 09:00:00','2026-04-16 18:00:00'),(16,6,'2026-04-17 09:00:00','2026-04-17 18:00:00'),(17,7,'2026-04-18 09:00:00','2026-04-18 17:00:00'),(18,8,'2026-04-21 09:00:00','2026-04-21 18:00:00'),(19,6,'2026-04-22 09:00:00','2026-04-22 18:00:00'),(20,7,'2026-04-23 09:00:00','2026-04-23 18:00:00'),(21,8,'2026-04-24 09:00:00','2026-04-24 18:00:00'),(22,6,'2026-04-25 09:00:00','2026-04-25 18:30:00'),(23,7,'2026-04-26 09:00:00','2026-04-26 17:00:00'),(24,8,'2026-04-28 09:00:00','2026-04-28 18:00:00'),(25,6,'2026-04-29 09:00:00','2026-04-29 18:00:00'),(26,7,'2026-04-30 09:00:00','2026-04-30 17:30:00');
/*!40000 ALTER TABLE `turno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombreUsuario` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fechaIngreso` date NOT NULL,
  `estatus` tinyint(1) NOT NULL,
  `fs_uniquifier` varchar(255) NOT NULL,
  `idRol` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fs_uniquifier` (`fs_uniquifier`),
  KEY `idRol` (`idRol`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`idRol`) REFERENCES `rol` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'vcruz','Vanessa','Cruz','scrypt:32768:8:1$fnXwZYqnTDTNledt$ca3fa09d8a03ec72f45f39267bb1dae23d037f01a142f903b2dba10fcec9ef408df80d6cf7409c6714e3b30c66f55e21572d5468db89d6ed591d6834982906bb','2026-01-01',1,'uuid-admin-vcruz-001',1),(2,'mramirez','Miguel','Ramírez','scrypt:32768:8:1$1WvHPcxDKa93CCf4$29eae1472e77570a90a91c262fc993ada7cbba84de2b03a4898ef1b356302e3c21c552bdd56ebde881c531df34f827f6909d4178e84b9f99477446c3ce7037f2','2026-01-10',1,'uuid-prod-mrami-002',2),(3,'jsalinas','Jorge','Salinas','$2b$12$prodHashAquiXXXXXXXXXXX','2026-01-15',1,'uuid-prod-jsali-003',2),(4,'pmorales','Patricia','Morales','$2b$12$prodHashAquiXXXXXXXXXXX','2026-02-01',1,'uuid-prod-pmora-004',2),(5,'rflores','Rodrigo','Flores','$2b$12$prodHashAquiXXXXXXXXXXX','2026-02-10',1,'uuid-prod-rflor-005',2),(6,'lgonzalez','Lucía','González','scrypt:32768:8:1$OUMCoZm5EGZ2Edc5$d33e036f0253d31e9715cc333cc05e953d0aed6dd32abb8ecdbd0963958e3e5524be24f41b62b1ee78ab2204087f9c128f5d3839830465930c8b34771deed575','2026-02-01',1,'uuid-most-lgonz-006',3),(7,'cperez','Carmen','Pérez','$2b$12$mostrHashAquiXXXXXXXXXX','2026-02-15',1,'uuid-most-cperz-007',3),(8,'aorozco','Alejandro','Orozco','$2b$12$mostrHashAquiXXXXXXXXXX','2026-03-01',1,'uuid-most-aoroz-008',3);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `idUsuario` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,'2026-04-01 10:30:00',56.00,6),(2,'2026-04-01 12:45:00',130.00,6),(3,'2026-04-01 15:20:00',68.00,6),(4,'2026-04-01 17:00:00',44.00,6),(5,'2026-04-02 11:00:00',86.00,7),(6,'2026-04-02 13:30:00',52.00,7),(7,'2026-04-02 16:00:00',34.00,7),(8,'2026-04-03 10:00:00',90.00,8),(9,'2026-04-03 13:00:00',62.00,8),(10,'2026-04-03 16:30:00',45.00,8),(11,'2026-04-04 10:20:00',95.00,6),(12,'2026-04-04 12:10:00',150.00,6),(13,'2026-04-04 14:45:00',44.00,6),(14,'2026-04-05 11:00:00',126.00,7),(15,'2026-04-05 13:00:00',88.00,7),(16,'2026-04-05 15:30:00',66.00,7),(17,'2026-04-07 10:30:00',70.00,8),(18,'2026-04-07 13:00:00',54.00,8),(19,'2026-04-08 11:00:00',108.00,6),(20,'2026-04-08 15:00:00',60.00,6),(21,'2026-04-09 10:00:00',80.00,7),(22,'2026-04-09 14:00:00',46.00,7),(23,'2026-04-10 11:30:00',140.00,8),(24,'2026-04-10 16:00:00',56.00,8),(25,'2026-04-11 10:00:00',96.00,6),(26,'2026-04-11 13:30:00',72.00,6),(27,'2026-04-12 10:00:00',162.00,7),(28,'2026-04-12 12:00:00',88.00,7),(29,'2026-04-12 14:00:00',130.00,7),(30,'2026-04-12 16:00:00',44.00,7),(47,'2026-04-15 18:56:52',22.00,6),(48,'2026-04-15 18:57:14',27.00,6),(49,'2026-04-15 18:58:49',9.00,6),(50,'2026-04-15 19:01:42',9.00,6),(51,'2026-04-15 19:01:55',18.00,6),(52,'2026-04-15 19:02:11',68.00,6),(53,'2026-04-15 19:19:53',22.00,6),(54,'2026-04-15 20:29:00',318.00,6),(55,'2026-04-16 16:54:27',22.00,6),(56,'2026-04-16 16:54:44',34.00,6),(57,'2026-04-16 16:54:58',150.00,6);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'casadelhelado'
--

--
-- Dumping routines for database 'casadelhelado'
--
/*!50003 DROP PROCEDURE IF EXISTS `agregar_detalle_pedido` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `agregar_detalle_pedido`( IN p_idPedido INT, IN p_idPresentacion INT, IN p_cantidad INT )
BEGIN DECLARE v_stock DECIMAL(10,2); DECLARE v_equivalencia DECIMAL(10,2); DECLARE v_precio DECIMAL(10,2); DECLARE v_unidades DECIMAL(10,2);
 -- Obtener datos 
 SELECT pb.stockActual, pv.equivalencia, pv.precio INTO v_stock, v_equivalencia, v_precio FROM presentacion_venta pv JOIN producto pb 
 ON pv.idProductoBase = pb.id WHERE pv.id = p_idPresentacion; -- Calcular unidades necesarias 
 
 SET v_unidades = p_cantidad * v_equivalencia; -- Validar stock 
 IF v_unidades > v_stock THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuficiente'; END IF; 
 -- Insertar detalle
 INSERT INTO detalle_pedido ( idPedido, idPresentacion, cantidad, precioUnitario )
 VALUES ( p_idPedido, p_idPresentacion, p_cantidad, v_precio ); -- Descontar stock 
 UPDATE producto pb JOIN presentacion_venta pv ON pv.idProductoBase = pb.id 
 SET pb.stockActual = pb.stockActual - v_unidades WHERE pv.id = p_idPresentacion; 
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `agregar_detalle_receta` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `agregar_detalle_receta`(
	in p_idReceta int, 
    in p_idMateriaPrima int, 
    in p_cantidad decimal(10,2), 
    in p_unidad varchar(20)
)
begin
	declare v_mp int;
    declare exit handler for sqlexception
    begin 
		rollback;
        select 'Error en la transaccion. Rollback' as mensaje;
    end;
    
    start transaction;
    
    select count(*) into v_mp
    from materia_prima where id = p_idMateriaPrima;
    
    if v_mp = 0 then 
		signal sqlstate '45000'
		set message_text = 'Error, materia prima no existe';
    end if;
    
    insert into detalle_receta(idReceta, idMateriaPrima,cantidad,unidad)
    values(p_idReceta, p_idMateriaPrima, p_cantidad, p_unidad);
    
    commit;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `agregar_detalle_venta` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `agregar_detalle_venta`(
    IN p_idVenta INT,
    IN p_idProductoBase INT,
    IN p_idPresentacion INT,
    IN p_cantidad INT,
    IN p_precio DECIMAL(10,2)
)
BEGIN
    DECLARE v_equivalencia DECIMAL(10,4);
    DECLARE v_stock_actual DECIMAL(10,2);

    START TRANSACTION;

    -- 1. Obtener equivalencia de la presentación
    SELECT equivalencia
    INTO v_equivalencia
    FROM presentacion_venta
    WHERE id = p_idPresentacion;

    -- 2. Validar stock actual del producto base
    SELECT stockActual
    INTO v_stock_actual
    FROM producto
    WHERE id = p_idProductoBase
    FOR UPDATE;

    -- 3. Validación de seguridad
    IF v_stock_actual < (v_equivalencia * p_cantidad) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock insuficiente';
    END IF;

    -- 4. Insertar detalle de venta
    INSERT INTO detalleventa (
        idVenta,
        idProducto,
        idPresentacion,
        cantidad,
        precioUnitario
    )
    VALUES (
        p_idVenta,
        p_idProductoBase,
        p_idPresentacion,
        p_cantidad,
        p_precio
    );

    -- 5. Descontar stock del producto base
    UPDATE producto
    SET stockActual = stockActual - (v_equivalencia * p_cantidad)
    WHERE id = p_idProductoBase;

    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `calcular_costo_receta` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `calcular_costo_receta`(IN p_idReceta INT)
BEGIN
    DECLARE v_costo DECIMAL(10,2);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error en la transaccion. Rollback' AS mensaje;
    END;

    START TRANSACTION;

    SELECT SUM(
        (
            SELECT 
                AVG(dc.precio / (dc.cantidad * c.factor))
            FROM detalle_compra dc
            INNER JOIN compra cp ON cp.id = dc.idCompra
            INNER JOIN conversiones c 
                ON c.unidadBase = (
                    SELECT unidadBase 
                    FROM materia_prima 
                    WHERE id = dr.idMateriaPrima
                )
                AND c.presentacion = 
                    REPLACE(REPLACE(dc.contenidoNeto, '1 ', ''), ' ', '')
            WHERE dc.idMateriaPrima = dr.idMateriaPrima
            AND cp.fechaCompra >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        ) * dr.cantidad
    ) INTO v_costo
    FROM detalle_receta dr
    WHERE dr.idReceta = p_idReceta;

    UPDATE receta 
    SET costoProduccion = v_costo 
    WHERE id = p_idReceta;

    COMMIT;

    SELECT v_costo AS costo_calculado;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `cancelar_pedido` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `cancelar_pedido`( IN p_folio VARCHAR(20) )
BEGIN DECLARE v_idPedido INT; DECLARE v_estatus VARCHAR(50); DECLARE done INT DEFAULT 0; 
 DECLARE v_idPresentacion INT; DECLARE v_cantidad INT; DECLARE v_equivalencia DECIMAL(10,2); 
 DECLARE cur CURSOR FOR SELECT dp.idPresentacion, dp.cantidad, pv.equivalencia FROM detalle_pedido dp 
 JOIN presentacion_venta pv ON dp.idPresentacion = pv.id WHERE dp.idPedido = v_idPedido; 
 DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1; -- Obtener pedido 
 SELECT id, estatus INTO v_idPedido, v_estatus FROM pedido WHERE folio = p_folio; 
 IF v_idPedido IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Pedido no encontrado'; 
 END IF; IF v_estatus <> 'Pago en proceso' THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede cancelar'; 
 END IF; -- Recorrer detalles 
 OPEN cur; read_loop: LOOP FETCH cur INTO v_idPresentacion, v_cantidad, v_equivalencia; IF done 
 THEN LEAVE read_loop; END IF; UPDATE producto pb JOIN presentacion_venta pv ON pv.idProductoBase = pb.id 
 SET pb.stockActual = pb.stockActual + (v_cantidad * v_equivalencia) WHERE pv.id = v_idPresentacion; END LOOP; CLOSE cur; -- Actualizar estado 
 UPDATE pedido SET estatus = 'Cancelado' WHERE id = v_idPedido; 
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `completar_produccion` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `completar_produccion`(
    IN p_idSolicitud INT
)
BEGIN
    DECLARE v_idReceta         INT;
    DECLARE v_lotes            INT;
    DECLARE v_cantidadProducida DECIMAL(10,2);
    DECLARE v_idProducto       INT;
    DECLARE v_estatus          VARCHAR(50);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT sp.idReceta, sp.lotes, sp.estatus, sp.idProducto
    INTO v_idReceta, v_lotes, v_estatus, v_idProducto
    FROM solicitud_produccion sp
    WHERE sp.id = p_idSolicitud
    FOR UPDATE;

    IF v_estatus != 'En Proceso' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La solicitud no está En Proceso';
    END IF;

    SELECT cantidadProducida INTO v_cantidadProducida
    FROM receta WHERE id = v_idReceta;

    -- Sumar al stock del producto terminado
    UPDATE producto
    SET stockActual = stockActual + (v_cantidadProducida * v_lotes)
    WHERE id = v_idProducto;

    UPDATE solicitud_produccion
    SET estatus = 'Completada'
    WHERE id = p_idSolicitud;

    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `crear_pedido` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `crear_pedido`( 
IN p_folio VARCHAR(20), IN p_idCliente INT, IN p_fecha_recogida DATETIME, IN p_total DECIMAL(10,2) )
BEGIN INSERT INTO pedido ( folio, idCliente, fechaPedido, fechaRecogida, estatus, total ) 

VALUES ( p_folio, p_idCliente, NOW(), p_fecha_recogida, 'Pago en proceso', p_total ); END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `crear_receta` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `crear_receta`(
	IN p_nombre varchar(100),
    IN p_idProducto int,
    IN p_cantidadProducida DECIMAL(10,2),
    out p_idReceta int
)
begin
	declare v_producto int;
    
    declare exit handler for sqlexception 
    begin 
		rollback;
        select 'Error en la transaccion. Rollaback' as mensaje;
	end;
    
    start transaction;
    
    select count(*) into v_producto
    from producto where id = p_idProducto;
    
    if v_producto = 0 then 
		signal sqlstate '45000'
        set message_text = 'Error, producto no existe';
	end if;
    
    insert into receta(nombre, idProducto, cantidadProducida, estatus)
    values(p_nombre, p_idProducto, p_cantidadProducida, TRUE);
    
    set p_idReceta = last_insert_id();
    commit;
    select 'Transaccion exitosa' as mensaje;

end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `crear_solicitud_produccion` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `crear_solicitud_produccion`(
    IN  p_idProducto  INT,
    IN  p_idReceta    INT,
    IN  p_lotes       INT,
    IN  p_idUsuario   INT,
    OUT p_resultado   VARCHAR(200)
)
BEGIN
    DECLARE v_producto INT DEFAULT 0;
    DECLARE v_receta   INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT COUNT(*) INTO v_producto FROM producto WHERE id = p_idProducto;
    IF v_producto = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El producto no existe';
    END IF;

    SELECT COUNT(*) INTO v_receta
    FROM receta WHERE id = p_idReceta AND idProducto = p_idProducto AND estatus = TRUE;
    IF v_receta = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La receta no existe o no pertenece al producto';
    END IF;

    INSERT INTO solicitud_produccion(idProducto, idReceta, lotes, idUsuario, fecha_solicitud, estatus)
    VALUES(p_idProducto, p_idReceta, p_lotes, p_idUsuario, NOW(), 'Pendiente');

    SET p_resultado = 'OK';
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `finalizar_venta` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `finalizar_venta`(
    IN p_idUsuario INT,
    IN p_total DECIMAL(10,2),
    OUT p_idVenta INT)
BEGIN
    INSERT INTO venta (
        idUsuario,
        fecha,
        total
        )
    VALUES (
        p_idUsuario,
        NOW(),
        p_total
        );
    SET p_idVenta = LAST_INSERT_ID();
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `iniciar_produccion` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `iniciar_produccion`(
    IN p_idSolicitud INT
)
BEGIN
    DECLARE v_idReceta  INT;
    DECLARE v_lotes     INT;
    DECLARE v_estatus   VARCHAR(50);
    DECLARE v_faltantes INT DEFAULT 0;

    -- Variables del cursor
    DECLARE v_idMP            INT;
    DECLARE v_cantidadDetalle DECIMAL(10,2);
    DECLARE done              INT DEFAULT FALSE;

    DECLARE cur CURSOR FOR
        SELECT idMateriaPrima, cantidad
        FROM detalle_receta
        WHERE idReceta = v_idReceta;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Obtener y bloquear la solicitud
    SELECT idReceta, lotes, estatus
    INTO v_idReceta, v_lotes, v_estatus
    FROM solicitud_produccion
    WHERE id = p_idSolicitud
    FOR UPDATE;

    IF v_estatus != 'Pendiente' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La solicitud no está en estado Pendiente';
    END IF;

    -- Validar stock de MATERIA PRIMA antes de tocar nada
    SELECT COUNT(*) INTO v_faltantes
    FROM detalle_receta dr
    JOIN materia_prima mp ON mp.id = dr.idMateriaPrima
    WHERE dr.idReceta = v_idReceta
      AND mp.stockActual < (dr.cantidad * v_lotes);

    IF v_faltantes > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock insuficiente de materia prima';
    END IF;

    -- Descontar materia prima
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_idMP, v_cantidadDetalle;
        IF done THEN LEAVE read_loop; END IF;

        UPDATE materia_prima
        SET stockActual = stockActual - (v_cantidadDetalle * v_lotes)
        WHERE id = v_idMP;
    END LOOP;
    CLOSE cur;

    -- Cambiar estatus
    UPDATE solicitud_produccion
    SET estatus = 'En Proceso'
    WHERE id = p_idSolicitud;

    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `pagar_pedido` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `pagar_pedido`( IN p_folio VARCHAR(20) )
BEGIN DECLARE v_estatus VARCHAR(50); 
 SELECT estatus INTO v_estatus FROM pedido WHERE folio = p_folio; 
 IF v_estatus IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Pedido no encontrado'; END IF; 
 IF v_estatus <> 'Pago en proceso' THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Pedido no válido para pago'; END IF; 
 UPDATE pedido SET estatus = 'Pagado' WHERE folio = p_folio; 
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `registrar_compra` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `registrar_compra`(
    IN p_factura VARCHAR(50),
    IN p_idProveedor INT,
    IN p_idUsuario INT,
    IN p_detalles JSON
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE n INT;
    DECLARE v_idMateria INT;
    DECLARE v_cantidad DOUBLE;
    DECLARE v_precio DOUBLE;
    DECLARE v_contenidoNeto VARCHAR(20);
    DECLARE v_unidadBase VARCHAR(10);
    DECLARE v_idCompra INT;
    DECLARE v_factor DOUBLE DEFAULT 1;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Error en la transaccion. Rollback' AS mensaje;
    END;

    START TRANSACTION;

    INSERT INTO compra (factura, fechaCompra, idProveedor, idUsuario, estatus)
    VALUES (p_factura, NOW(), p_idProveedor, p_idUsuario, 1);

    SET v_idCompra = LAST_INSERT_ID();
    SET n = JSON_LENGTH(p_detalles);

    WHILE i < n DO
        SET v_idMateria     = JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[', i, '].idMateriaPrima')));
        SET v_cantidad      = JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[', i, '].cantidad')));
        SET v_contenidoNeto = JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[', i, '].contenidoNeto')));
        SET v_precio        = JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[', i, '].precio')));        
		SET v_factor = 1;

		SELECT unidadBase INTO v_unidadBase
		FROM materia_prima
		WHERE id = v_idMateria;

		SELECT factor INTO v_factor
		FROM conversiones
		WHERE presentacion = v_contenidoNeto
		AND unidadBase = v_unidadBase
		LIMIT 1;

		IF v_factor IS NULL THEN
			SET v_factor = 1;
		END IF;

        INSERT INTO detalle_compra (idCompra, idMateriaPrima, cantidad, contenidoNeto, precio)
        VALUES (v_idCompra, v_idMateria, v_cantidad, v_contenidoNeto, v_precio);

        UPDATE materia_prima SET stockActual = stockActual + (v_cantidad * v_factor) WHERE id = v_idMateria;

        SET i = i + 1;
    END WHILE;

    COMMIT;
    SELECT 'Transaccion exitosa' AS mensaje;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `registrar_merma` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `registrar_merma`(
    IN p_idMateriaPrima INT,
    IN p_idProducto INT,
    IN p_cantidad INT,
    IN p_justificacion VARCHAR(200),
    IN p_idUsuario INT
)
BEGIN
    DECLARE v_stock DECIMAL(10,2);
    DECLARE v_unidad VARCHAR(20);

    -- Validación: solo uno debe venir
    IF (p_idMateriaPrima IS NULL AND p_idProducto IS NULL) OR 
       (p_idMateriaPrima IS NOT NULL AND p_idProducto IS NOT NULL) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Debes enviar materia prima o producto, no ambos';
    END IF;

    -- MATERIA PRIMA
    IF p_idMateriaPrima IS NOT NULL THEN
        SELECT stockActual, unidadBase 
        INTO v_stock, v_unidad
        FROM materia_prima
        WHERE id = p_idMateriaPrima;

        IF v_stock < p_cantidad THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Stock insuficiente en materia prima';
        END IF;

        UPDATE materia_prima
        SET stockActual = stockActual - p_cantidad
        WHERE id = p_idMateriaPrima;

        INSERT INTO merma (
            idMateriaPrima, cantidad, unidad, justificacion, fecha, idUsuario, estatus
        )
        VALUES (
            p_idMateriaPrima, p_cantidad, v_unidad, p_justificacion, NOW(), p_idUsuario, true
        );

    END IF;

    -- PRODUCTO
    IF p_idProducto IS NOT NULL THEN

        SELECT stockActual, unidadBase 
        INTO v_stock, v_unidad
        FROM producto
        WHERE id = p_idProducto;

        IF v_stock < p_cantidad THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Stock insuficiente en producto';
        END IF;

        UPDATE producto
        SET stockActual = stockActual - p_cantidad
        WHERE id = p_idProducto;

        INSERT INTO merma (
            idProducto, cantidad, unidad, justificacion, fecha, idUsuario, estatus
        )
        VALUES (
            p_idProducto, p_cantidad, v_unidad, p_justificacion, NOW(), p_idUsuario, true
        );

    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-16 17:15:54
