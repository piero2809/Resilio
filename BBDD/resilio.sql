-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: resilio
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `preguntas`
--

DROP TABLE IF EXISTS `preguntas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preguntas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dimension` enum('agotamiento','cinismo','eficacia') NOT NULL,
  `enunciado` text NOT NULL,
  `orden` int DEFAULT '0',
  `es_activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preguntas`
--

LOCK TABLES `preguntas` WRITE;
/*!40000 ALTER TABLE `preguntas` DISABLE KEYS */;
INSERT INTO `preguntas` VALUES (1,'agotamiento','Me siento emocionalmente agotado por mi trabajo.',1,1),(2,'agotamiento','Me siento acabado al final de la jornada de trabajo.',2,1),(3,'agotamiento','Me siento fatigado cuando me levanto por la mañana.',3,1),(4,'agotamiento','Trabajar todo el día representa un gran esfuerzo para mí.',4,1),(5,'agotamiento','Me siento quemado por el trabajo.',5,1),(6,'cinismo','He perdido entusiasmo por mi trabajo.',6,1),(7,'cinismo','Me he vuelto más cínico respecto a la utilidad de mi trabajo.',7,1),(8,'cinismo','Solo quiero hacer mi trabajo y que no me molesten.',8,1),(9,'cinismo','Dudo del valor y la utilidad de mi trabajo.',9,1),(10,'cinismo','Me he vuelto más distante de mi trabajo.',10,1),(11,'eficacia','Puedo resolver eficazmente los problemas en mi trabajo.',11,1),(12,'eficacia','Siento que hago una contribución efectiva a mi empresa.',12,1),(13,'eficacia','En mi opinión, soy bueno en lo que hago.',13,1),(14,'eficacia','Me siento estimulado cuando realizo algo importante.',14,1),(15,'eficacia','He conseguido muchas cosas valiosas en este puesto.',15,1);
/*!40000 ALTER TABLE `preguntas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `respuestas_detalle`
--

DROP TABLE IF EXISTS `respuestas_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `respuestas_detalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `intento_id` int NOT NULL,
  `pregunta_id` int NOT NULL,
  `puntuacion` tinyint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `intento_id` (`intento_id`),
  KEY `pregunta_id` (`pregunta_id`),
  CONSTRAINT `respuestas_detalle_ibfk_1` FOREIGN KEY (`intento_id`) REFERENCES `test_intentos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `respuestas_detalle_ibfk_2` FOREIGN KEY (`pregunta_id`) REFERENCES `preguntas` (`id`),
  CONSTRAINT `respuestas_detalle_chk_1` CHECK ((`puntuacion` between 0 and 6))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respuestas_detalle`
--

LOCK TABLES `respuestas_detalle` WRITE;
/*!40000 ALTER TABLE `respuestas_detalle` DISABLE KEYS */;
/*!40000 ALTER TABLE `respuestas_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),   
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin'),(3,'gestor_rrhh'),(2,'usuario_personal');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_intentos`
--

DROP TABLE IF EXISTS `test_intentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_intentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `fecha_realizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `puntuacion_agotamiento` decimal(4,2) DEFAULT NULL,
  `puntuacion_cinismo` decimal(4,2) DEFAULT NULL,
  `puntuacion_eficacia` decimal(4,2) DEFAULT NULL,
  `resultado_final` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `test_intentos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_intentos`
--

LOCK TABLES `test_intentos` WRITE;
/*!40000 ALTER TABLE `test_intentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `test_intentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_resultados`
--

DROP TABLE IF EXISTS `test_resultados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_resultados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `agotamiento_puntos` int DEFAULT NULL,
  `despersonalizacion_puntos` int DEFAULT NULL,
  `realizacion_puntos` int DEFAULT NULL,
  `resultado_final` varchar(50) DEFAULT NULL,
  `fecha_realizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `test_resultados_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_resultados`
--

LOCK TABLES `test_resultados` WRITE;
/*!40000 ALTER TABLE `test_resultados` DISABLE KEYS */;
/*!40000 ALTER TABLE `test_resultados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rol_id` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-10  1:24:12


-- Create user 

CREATE USER 
'resilio'@'localhost' 
IDENTIFIED  BY 'Resilio123$';

GRANT USAGE ON *.* TO 'resilio'@'localhost';

ALTER USER 'resilio'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON resilio.* 
TO 'resilio'@'localhost';

FLUSH PRIVILEGES;

-- Modificacion en la tabla usuarios para que sea compatible con personas dentro y fuera de la empresa

-- 1. Agregamos la columna empresa (puede ser NULL para usuarios libres)
ALTER TABLE usuarios 
ADD COLUMN empresa VARCHAR(100) DEFAULT NULL;

-- 2. Agregamos la columna departamento (puede ser NULL para usuarios libres)
ALTER TABLE usuarios 
ADD COLUMN departamento VARCHAR(100) DEFAULT NULL;
