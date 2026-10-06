-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: resilio_db
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
-- Table structure for table `departamentos`
--

DROP TABLE IF EXISTS `departamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departamentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `empresa_id` int NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `empresa_id` (`empresa_id`),
  CONSTRAINT `departamentos_ibfk_1` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamentos`
--

LOCK TABLES `departamentos` WRITE;
/*!40000 ALTER TABLE `departamentos` DISABLE KEYS */;
INSERT INTO `departamentos` VALUES (1,1,'Tecnología de la Información (IT)'),(2,1,'Ventas y Marketing'),(3,1,'Recursos Humanos'),(4,2,'Recursos Humanos (HR)'),(5,2,'Operaciones'),(6,2,'Ventas');
/*!40000 ALTER TABLE `departamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dimensiones`
--

DROP TABLE IF EXISTS `dimensiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dimensiones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dimensiones`
--

LOCK TABLES `dimensiones` WRITE;
/*!40000 ALTER TABLE `dimensiones` DISABLE KEYS */;
INSERT INTO `dimensiones` VALUES (1,'Agotamiento','Fatiga física y mental severa.'),(2,'Distanciamiento Mental','Cinismo y evitación del trabajo.'),(3,'Deterioro Cognitivo','Problemas de concentración, memoria y atención.'),(4,'Deterioro Emocional','Falta de control sobre las emociones en el trabajo.');
/*!40000 ALTER TABLE `dimensiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresas`
--

DROP TABLE IF EXISTS `empresas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sector` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `codigo_registro` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_registro` (`codigo_registro`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresas`
--

LOCK TABLES `empresas` WRITE;
/*!40000 ALTER TABLE `empresas` DISABLE KEYS */;
INSERT INTO `empresas` VALUES (1,'TechCorp Innovations','Tecnología','TECH-2026-VIP'),(2,'Acme Corporation','Manufactura y Logística','ACME-HR-2026'),(3,'aaaa','Tecnología','NOVA-6500-X');
/*!40000 ALTER TABLE `empresas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluaciones`
--

DROP TABLE IF EXISTS `evaluaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `puntuacion_total` decimal(4,2) NOT NULL,
  `dim_agotamiento` decimal(4,2) NOT NULL,
  `dim_distanciamiento` decimal(4,2) NOT NULL,
  `dim_cognitivo` decimal(4,2) NOT NULL,
  `dim_emocional` decimal(4,2) NOT NULL,
  `consejos` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `evaluaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluaciones`
--

LOCK TABLES `evaluaciones` WRITE;
/*!40000 ALTER TABLE `evaluaciones` DISABLE KEYS */;
INSERT INTO `evaluaciones` VALUES (1,5,'2026-03-09 10:41:54',3.00,3.00,3.00,3.00,3.00,'No se han generado consejos. Configura la API de Gemini para obtener recomendaciones personalizadas.'),(2,5,'2026-03-11 12:35:56',2.92,2.00,3.33,3.00,3.33,'No se han generado consejos. Configura la API de Gemini para obtener recomendaciones personalizadas.'),(3,5,'2026-03-11 12:36:29',1.00,1.00,1.00,1.00,1.00,'No se han generado consejos. Configura la API de Gemini para obtener recomendaciones personalizadas.'),(4,5,'2026-03-11 12:36:58',3.33,3.67,2.33,5.00,2.33,'No se han generado consejos. Configura la API de Gemini para obtener recomendaciones personalizadas.'),(5,5,'2026-03-11 12:37:21',5.00,5.00,5.00,5.00,5.00,'No se han generado consejos. Configura la API de Gemini para obtener recomendaciones personalizadas.'),(7,5,'2026-03-12 10:42:36',3.58,3.67,3.67,3.33,3.67,''),(8,4,'2026-03-12 10:44:03',3.00,3.00,3.00,3.00,3.00,'Error al generar consejos. Por favor, intenta más tarde.'),(9,5,'2026-03-12 10:55:26',3.83,3.00,3.33,4.00,5.00,'No se han generado consejos. Configura la API de Gemini para obtener recomendaciones personalizadas.'),(10,5,'2026-03-12 10:58:09',3.92,4.00,4.00,4.00,3.67,'No se han generado consejos. Configura la API de Gemini para obtener recomendaciones personalizadas.'),(11,5,'2026-03-12 11:00:36',4.08,4.00,4.33,3.67,4.33,'Error al generar consejos. Por favor, intenta más tarde.'),(12,5,'2026-03-12 11:28:42',3.58,3.00,3.67,4.00,3.67,'Cuota de la API agotada. Intenta de nuevo en unas horas o configura una API key con facturación.'),(13,5,'2026-03-12 11:33:55',3.25,4.00,3.00,3.00,3.00,'Cuota de la API agotada. Intenta de nuevo en unas horas o configura una API key con facturación.'),(14,5,'2026-03-12 11:42:59',3.50,3.00,3.33,4.00,3.67,'Cuota de la API agotada. Intenta de nuevo en unas horas o configura una API key con facturación.'),(15,5,'2026-03-13 12:21:36',3.75,3.00,3.67,3.33,5.00,'Modo de prueba: Si puedes leer esto en tu dashboard, significa que el test y la base de datos funcionan perfecto. El problema era la conexión con Gemini.'),(16,5,'2026-03-13 12:41:26',4.17,3.67,4.67,4.33,4.00,'Tus resultados se guardaron. (Los consejos de la IA no cargaron, verifica la terminal para ver el error).'),(17,5,'2026-03-13 12:49:44',3.17,3.00,3.67,2.67,3.33,'Tus resultados se guardaron. (Los consejos de la IA no cargaron, verifica la terminal para ver el error).'),(18,5,'2026-03-13 13:06:31',3.42,3.00,3.33,3.67,3.67,'Entiendo perfectamente cómo te sientes. Una puntuación de 3.42/5 indica que estás atravesando una etapa de desgaste considerable, y que el área **cognitiva** sea la más afectada significa que probablemente sientas \"niebla mental\", dificultad para concentrarte o pequeños olvidos que antes no tenías.\n\nEn Resilio queremos ayudarte a liberar esa carga mental. Aquí tienes 3 consejos accionables para aplicar hoy mismo:\n\n1.  **Haz un \"Vaciado Mental\" de 5 minutos:**\n    La saturación cognitiva ocurre cuando intentamos retener demasiada información. Toma papel y lápiz (evita el móvil) y escribe absolutamente todo lo que tienes pendiente o te preocupa, sin orden. Al pasarlo al papel, tu cerebro deja de gastar energía intentando \"no olvidarlo\", liberando de inmediato capacidad de procesamiento.\n\n2.  **Aplica la regla de \"Una Sola Tarea\" (Monotasking):**\n    Cuando la dimensión cognitiva está agotada, el *multitasking* es tu peor enemigo. Elige una sola actividad, cierra todas las pestañas de tu navegador que no uses y pon el móvil en silencio por 25 minutos. Al reducir los estímulos externos, permites que tu atención se estabilice sin agotarse.\n\n3.  **Realiza Micro-pausas de \"Contraste Sensorial\":**\n    Cada hora, aléjate de la pantalla durante 2 minutos. Cierra los ojos y busca identificar 3 sonidos lejanos y 3 sensaciones físicas (el roce de la ropa, el contacto de los pies con el suelo). Esto ayuda a desconectar el \"piloto automático\" cognitivo y devuelve tu atención al momento presente, reduciendo la fatiga mental.\n\nRecuerda que estos hábitos son herramientas para gestionar tu bienestar diario; escuchar a tu cuerpo es el primer paso para recuperar tu claridad mental.'),(19,5,'2026-03-13 13:48:55',4.17,4.00,3.67,5.00,4.00,'<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Pausas mentales</h4>\n        <p>Realiza descansos de cinco minutos sin pantallas cada hora para liberar carga mental.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Foco único</h4>\n        <p>Evita la multitarea; prioriza una sola actividad para reducir el agotamiento cognitivo.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Desconexión total</h4>\n        <p>Dedica diez minutos al finalizar tu jornada a una actividad manual o física relajante.</p>\n    </div>\n</div>'),(20,5,'2026-03-13 14:01:46',1.00,1.00,1.00,1.00,1.00,'<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Prioriza el descanso</h4>\n        <p>Duerme al menos siete horas diarias para que tu cuerpo y mente se recuperen adecuadamente.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Desconexión total</h4>\n        <p>Apaga toda notificación laboral al terminar tu jornada para reducir la fatiga mental acumulada.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Pausas conscientes</h4>\n        <p>Realiza tres respiraciones profundas cada hora para liberar tensiones y oxigenar tu sistema nervioso.</p>\n    </div>\n</div>'),(21,5,'2026-03-13 14:11:10',3.50,4.00,4.67,4.00,1.33,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Lamentamos que estés pasando por un momento de carga emocional elevada; tu puntuación de 3.5 refleja un agotamiento que merece atención. Es fundamental que valides lo que sientes y te permitas priorizar tu recuperación para reducir ese distanciamiento.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Humaniza tus vínculos</h4>\n        <p>Busca momentos de charla informal con compañeros para reducir la sensación de distanciamiento emocional.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Micro-pausas activas</h4>\n        <p>Tómate cinco minutos cada hora para estirar y alejar la vista de las pantallas.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Ritual de cierre</h4>\n        <p>Define una hora límite de conexión digital para separar totalmente tu vida personal del trabajo.</p>\n    </div>\n</div>'),(22,5,'2026-03-18 14:48:44',2.75,3.00,3.00,2.33,2.67,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Tu puntuación de 2.75 indica que estás experimentando un agotamiento que requiere atención y autocuidado. Es un momento importante para validar tu cansancio y empezar a priorizar tu recuperación personal.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Límites Claros</h4>\n        <p>Establece una hora fija de desconexión digital para separar tu vida laboral de la personal.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Micro-descansos</h4>\n        <p>Realiza pausas de cinco minutos cada hora para estirarte y alejar la vista del monitor.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Calma Inmediata</h4>\n        <p>Practica la respiración abdominal durante dos minutos cuando sientas que el agotamiento te sobrepasa.</p>\n    </div>\n</div>'),(23,5,'2026-03-19 17:31:22',3.75,3.00,4.00,4.00,4.00,'\n        <div class=\"consejos-grid\">\n            <div class=\"consejo-card\" style=\"border-top-color: #ff4757;\">\n                <h4>⚠️ Aviso del Sistema</h4>\n                <p>Tus resultados se guardaron con éxito, pero los consejos de la IA no pudieron cargar en este momento.</p>\n            </div>\n        </div>\n        '),(24,5,'2026-03-20 21:23:30',3.00,3.33,3.00,3.33,2.33,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Tu puntuación de 3.0 indica que el estrés está afectando tu bienestar, especialmente mediante el agotamiento. Es el momento de ser amable contigo mismo y priorizar tu recuperación física y mental.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Micro-pausas activas</h4>\n        <p>Aplica descansos de cinco minutos cada hora para liberar tensión y oxigenar tu cerebro eficazmente.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Desconexión digital</h4>\n        <p>Define una hora de cierre total para separar tu vida personal del entorno laboral diario.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Respiración consciente</h4>\n        <p>Realiza respiraciones profundas antes de cada reunión para calmar tu sistema nervioso y reducir fatiga.</p>\n    </div>\n</div>'),(25,5,'2026-03-25 12:54:34',3.17,2.00,3.67,3.33,3.67,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Tu puntuación de 3.17 indica que estás enfrentando un nivel de estrés que merece atención. Es comprensible que sientas distanciamiento; estamos aquí para apoyarte a recuperar tu bienestar.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Vínculos de apoyo</h4>\n        <p>Busca interacciones breves y significativas con otros para reducir el sentimiento de desconexión emocional.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Desconexión digital</h4>\n        <p>Establece un horario estricto de cierre tecnológico para separar tu vida personal del trabajo.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Pausas conscientes</h4>\n        <p>Practica la respiración controlada durante tres minutos al iniciar y finalizar tu jornada laboral.</p>\n    </div>\n</div>'),(26,5,'2026-03-25 13:39:46',3.00,3.00,2.67,3.33,3.00,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Tu puntuación de 3.0 indica que estás atravesando un periodo de estrés considerable que afecta tu concentración. Es comprensible que sientas fatiga mental; estamos aquí para apoyarte a recuperar tu equilibrio.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Monotarea consciente</h4>\n        <p>Enfócate en una sola actividad a la vez para reducir la carga cognitiva acumulada diariamente.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Microdescansos mentales</h4>\n        <p>Realiza pausas de cinco minutos cada hora para liberar tensión y oxigenar tu cerebro efectivamente.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Desconexión total</h4>\n        <p>Establece un horario límite para pantallas, permitiendo que tu mente descanse profundamente antes de dormir.</p>\n    </div>\n</div>'),(27,6,'2026-03-25 13:42:23',3.42,2.67,3.00,3.67,4.33,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Tu puntuación de 3.42 indica que estás atravesando un periodo de agotamiento emocional considerable. Reconocer esta carga es el primer paso para permitirte el descanso y la recuperación que tanto necesitas ahora.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Gestión emocional</h4>\n        <p>Identifica y nombra tus emociones diariamente para reducir su impacto y recuperar la calma interna.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Pausas breves</h4>\n        <p>Realiza respiraciones profundas durante cinco minutos para relajar tu sistema nervioso y liberar tensiones acumuladas.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Desconexión total</h4>\n        <p>Establece un horario firme para apagar notificaciones de trabajo y priorizar actividades que te reconforten.</p>\n    </div>\n</div>'),(28,5,'2026-03-26 00:08:04',3.67,3.00,3.67,3.33,4.67,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Entendemos que te sientas agotado emocionalmente en este momento. Tu puntuación de 3.67 indica una carga de estrés considerable, pero estamos aquí para acompañarte a recuperar tu bienestar paso a paso.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Validación emocional</h4>\n        <p>Permítete sentir sin juzgarte; reconocer tus emociones es el primer paso para sanar.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Desconexión total</h4>\n        <p>Establece un horario estricto de fin de jornada y silencia toda notificación de trabajo.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Respiración 4-7-8</h4>\n        <p>Inhala 4 segundos, retén 7 y exhala 8 para calmar tu sistema nervioso inmediatamente.</p>\n    </div>\n</div>'),(29,5,'2026-03-26 12:19:13',3.17,2.67,3.00,3.67,3.33,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Tu puntuación de 3.17 indica que estás atravesando un periodo de estrés significativo. Es comprensible que sientas fatiga cognitiva; estamos aquí para apoyarte en tu recuperación y bienestar.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Enfoque Único</h4>\n        <p>Evita la multitarea; realiza una sola actividad a la vez para reducir el agotamiento mental.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Pausas Visuales</h4>\n        <p>Aplica la regla 20-20-20: cada veinte minutos, mira algo a seis metros durante veinte segundos.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Desconexión Total</h4>\n        <p>Establece una hora límite para revisar dispositivos y permite que tu mente descanse profundamente.</p>\n    </div>\n</div>'),(30,5,'2026-03-26 12:51:52',3.75,2.33,4.67,3.67,4.33,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Entiendo que estés pasando por un momento difícil; tu puntuación de 3.75 indica un agotamiento considerable. Es comprensible sentir ese distanciamiento como defensa ante el estrés; estamos aquí para apoyarte.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Reconecta con sentido</h4>\n        <p>Identifica una tarea que aporte valor real para recuperar el sentido de tu labor diaria.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Desconexión digital</h4>\n        <p>Define una hora de cierre total para permitir que tu mente descanse realmente sin distracciones.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Respiración 4-7-8</h4>\n        <p>Inhala en cuatro segundos y exhala en ocho para calmar tu sistema nervioso inmediatamente.</p>\n    </div>\n</div>'),(31,5,'2026-03-26 13:06:32',3.42,3.00,3.00,3.67,4.00,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Tu puntuación de 3.42 indica que estás atravesando un periodo de agotamiento emocional significativo. Entendemos tu cansancio y estamos aquí para apoyarte a recuperar tu equilibrio y bienestar.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Expresión emocional</h4>\n        <p>Dedica diez minutos diarios a escribir tus sentimientos para liberar la carga mental acumulada.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Límites claros</h4>\n        <p>Establece una hora fija para desconectar notificaciones y proteger tu tiempo de descanso personal.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Pausa consciente</h4>\n        <p>Practica la respiración 4-7-8 tres veces al día para calmar tu sistema nervioso rápidamente.</p>\n    </div>\n</div>'),(32,5,'2026-05-04 10:42:32',3.08,3.00,3.00,2.67,3.67,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Comprendemos que te sientas agotado emocionalmente; tu resultado de 3.08 indica que estás asumiendo una carga pesada. No estás solo en esto y es el momento ideal para priorizar tu descanso y bienestar.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Límites claros</h4>\n        <p>Identifica qué situaciones agotan tu energía y establece límites para proteger tu espacio personal.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Pausas conscientes</h4>\n        <p>Realiza descansos breves cada hora para desconectar la mente y reducir la tensión acumulada.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Respiración profunda</h4>\n        <p>Dedica tres minutos a respirar profundamente para centrarte y calmar el agobio emocional actual.</p>\n    </div>\n</div>'),(33,9,'2026-05-28 23:29:26',3.33,3.33,3.00,2.67,4.33,'\n        <div class=\"consejos-grid\">\n            <div class=\"consejo-card\" style=\"border-top-color: #ff4757;\">\n                <h4>⚠️ Aviso del Sistema</h4>\n                <p>Tus resultados se guardaron con éxito, pero los consejos de la IA no pudieron cargar en este momento.</p>\n            </div>\n        </div>\n        '),(34,10,'2026-05-29 00:03:22',3.42,3.33,2.67,4.00,3.67,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Tu puntuación de 3.42 indica que estás atravesando una etapa de agotamiento considerable que requiere tu atención y autocuidado. Comprendemos que te sientas mentalmente sobrepasado; es vital priorizar espacios de desconexión real para proteger tu bienestar.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Micro-pausas mentales</h4>\n        <p>Realiza descansos de cinco minutos sin pantallas cada hora para reducir la fatiga cognitiva.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Priorización radical</h4>\n        <p>Selecciona solo tres tareas clave diarias para evitar la saturación y el agobio mental.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Ritual de cierre</h4>\n        <p>Practica respiración consciente al terminar la jornada para facilitar una desconexión mental profunda y real.</p>\n    </div>\n</div>'),(35,11,'2026-05-29 10:50:19',1.00,1.00,1.00,1.00,1.00,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>¡Muchas felicidades por tu excelente puntuación de 1.0/5! Gozas de un bienestar óptimo y un gran equilibrio emocional; sigue cultivando tus hábitos actuales para mantener esta energía positiva a largo plazo.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Blindaje del descanso</h4>\n        <p>Mantén tus horarios de desconexión digital para asegurar que tu mente repose cada día.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Pausas preventivas</h4>\n        <p>Continúa con tus breves descansos activos para oxigenar tu cuerpo y evitar fatiga futura.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Autocuidado constante</h4>\n        <p>Sigue priorizando tus hobbies y actividad física como pilares fundamentales de tu bienestar actual.</p>\n    </div>\n</div>'),(36,11,'2026-05-29 10:53:02',4.75,5.00,4.67,4.67,4.67,'\n        <div class=\"consejos-grid\">\n            <div class=\"consejo-card\" style=\"border-top-color: #ff4757;\">\n                <h4>⚠️ Aviso del Sistema</h4>\n                <p>Tus resultados se guardaron con éxito, pero los consejos de la IA no pudieron cargar en este momento.</p>\n            </div>\n        </div>\n        '),(37,12,'2026-05-29 12:43:21',4.17,3.67,4.67,4.00,4.33,'<div class=\"consejo-intro\" style=\"margin-bottom: 25px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;\">\n    <p>Sentimos que estés atravesando este nivel de agotamiento; tu puntuación de 4.17 refleja una carga de estrés muy pesada. Es fundamental que valides tu cansancio y te permitas momentos de desconexión profunda para recuperarte.</p>\n</div>\n<div class=\"consejos-grid\">\n    <div class=\"consejo-card\">\n        <h4>💡 Reconexión humana</h4>\n        <p>Conversa con un colega sobre temas no laborales para disminuir el sentimiento de distanciamiento.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>⚡ Límites claros</h4>\n        <p>Define una hora de desconexión total y silencia las notificaciones del trabajo al finalizar.</p>\n    </div>\n    <div class=\"consejo-card\">\n        <h4>🧘 Pausa consciente</h4>\n        <p>Dedica cinco minutos diarios a respirar profundamente para anclarte en el momento presente.</p>\n    </div>\n</div>');
/*!40000 ALTER TABLE `evaluaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preguntas`
--

DROP TABLE IF EXISTS `preguntas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preguntas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dimension_id` int NOT NULL,
  `texto` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `es_activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `dimension_id` (`dimension_id`),
  CONSTRAINT `preguntas_ibfk_1` FOREIGN KEY (`dimension_id`) REFERENCES `dimensiones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preguntas`
--

LOCK TABLES `preguntas` WRITE;
/*!40000 ALTER TABLE `preguntas` DISABLE KEYS */;
INSERT INTO `preguntas` VALUES (1,1,'En el trabajo, me siento mentalmente agotado/a.',1),(2,1,'Después de un día de trabajo, me resulta difícil recuperar mi energía.',1),(3,1,'Me siento físicamente agotado/a en el trabajo.',1),(4,2,'Me cuesta encontrar entusiasmo por mi trabajo.',1),(5,2,'Siento una fuerte aversión hacia mi trabajo.',1),(6,2,'Soy cínico/a sobre lo que significa mi trabajo para los demás.',1),(7,3,'En el trabajo, me cuesta mantener la concentración.',1),(8,3,'Cuando estoy trabajando, cometo errores porque estoy distraído/a.',1),(9,3,'En el trabajo, me cuesta pensar con claridad.',1),(10,4,'En el trabajo, me siento incapaz de controlar mis emociones.',1),(11,4,'No reconozco mi propia forma de reaccionar emocionalmente en el trabajo.',1),(12,4,'En mi trabajo me irrito con facilidad sin saber por qué.',1);
/*!40000 ALTER TABLE `preguntas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `respuestas_evaluacion`
--

DROP TABLE IF EXISTS `respuestas_evaluacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `respuestas_evaluacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `evaluacion_id` int NOT NULL,
  `pregunta_id` int NOT NULL,
  `valor` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `evaluacion_id` (`evaluacion_id`),
  KEY `pregunta_id` (`pregunta_id`),
  CONSTRAINT `respuestas_evaluacion_ibfk_1` FOREIGN KEY (`evaluacion_id`) REFERENCES `evaluaciones` (`id`) ON DELETE CASCADE,
  CONSTRAINT `respuestas_evaluacion_ibfk_2` FOREIGN KEY (`pregunta_id`) REFERENCES `preguntas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=433 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respuestas_evaluacion`
--

LOCK TABLES `respuestas_evaluacion` WRITE;
/*!40000 ALTER TABLE `respuestas_evaluacion` DISABLE KEYS */;
INSERT INTO `respuestas_evaluacion` VALUES (1,1,1,3),(2,1,2,3),(3,1,3,3),(4,1,4,3),(5,1,5,3),(6,1,6,3),(7,1,7,3),(8,1,8,3),(9,1,9,3),(10,1,10,3),(11,1,11,3),(12,1,12,3),(13,2,1,2),(14,2,2,2),(15,2,3,2),(16,2,4,4),(17,2,5,4),(18,2,6,2),(19,2,7,4),(20,2,8,4),(21,2,9,1),(22,2,10,5),(23,2,11,4),(24,2,12,1),(25,3,1,1),(26,3,2,1),(27,3,3,1),(28,3,4,1),(29,3,5,1),(30,3,6,1),(31,3,7,1),(32,3,8,1),(33,3,9,1),(34,3,10,1),(35,3,11,1),(36,3,12,1),(37,4,1,5),(38,4,2,1),(39,4,3,5),(40,4,4,1),(41,4,5,5),(42,4,6,1),(43,4,7,5),(44,4,8,5),(45,4,9,5),(46,4,10,5),(47,4,11,1),(48,4,12,1),(49,5,1,5),(50,5,2,5),(51,5,3,5),(52,5,4,5),(53,5,5,5),(54,5,6,5),(55,5,7,5),(56,5,8,5),(57,5,9,5),(58,5,10,5),(59,5,11,5),(60,5,12,5),(61,7,1,2),(62,7,2,4),(63,7,3,5),(64,7,4,1),(65,7,5,5),(66,7,6,5),(67,7,7,4),(68,7,8,3),(69,7,9,3),(70,7,10,4),(71,7,11,5),(72,7,12,2),(73,8,1,3),(74,8,2,3),(75,8,3,3),(76,8,4,3),(77,8,5,3),(78,8,6,3),(79,8,7,3),(80,8,8,3),(81,8,9,3),(82,8,10,3),(83,8,11,3),(84,8,12,3),(85,9,1,3),(86,9,2,3),(87,9,3,3),(88,9,4,3),(89,9,5,3),(90,9,6,4),(91,9,7,5),(92,9,8,5),(93,9,9,2),(94,9,10,5),(95,9,11,5),(96,9,12,5),(97,10,1,5),(98,10,2,4),(99,10,3,3),(100,10,4,5),(101,10,5,5),(102,10,6,2),(103,10,7,2),(104,10,8,5),(105,10,9,5),(106,10,10,4),(107,10,11,2),(108,10,12,5),(109,11,1,4),(110,11,2,5),(111,11,3,3),(112,11,4,5),(113,11,5,3),(114,11,6,5),(115,11,7,5),(116,11,8,4),(117,11,9,2),(118,11,10,4),(119,11,11,4),(120,11,12,5),(121,12,1,2),(122,12,2,3),(123,12,3,4),(124,12,4,4),(125,12,5,3),(126,12,6,4),(127,12,7,4),(128,12,8,4),(129,12,9,4),(130,12,10,4),(131,12,11,2),(132,12,12,5),(133,13,1,3),(134,13,2,4),(135,13,3,5),(136,13,4,1),(137,13,5,3),(138,13,6,5),(139,13,7,2),(140,13,8,5),(141,13,9,2),(142,13,10,3),(143,13,11,4),(144,13,12,2),(145,14,1,2),(146,14,2,5),(147,14,3,2),(148,14,4,5),(149,14,5,3),(150,14,6,2),(151,14,7,5),(152,14,8,3),(153,14,9,4),(154,14,10,5),(155,14,11,2),(156,14,12,4),(157,15,1,4),(158,15,2,2),(159,15,3,3),(160,15,4,4),(161,15,5,5),(162,15,6,2),(163,15,7,3),(164,15,8,5),(165,15,9,2),(166,15,10,5),(167,15,11,5),(168,15,12,5),(169,16,1,3),(170,16,2,5),(171,16,3,3),(172,16,4,5),(173,16,5,5),(174,16,6,4),(175,16,7,5),(176,16,8,5),(177,16,9,3),(178,16,10,2),(179,16,11,5),(180,16,12,5),(181,17,1,3),(182,17,2,2),(183,17,3,4),(184,17,4,5),(185,17,5,1),(186,17,6,5),(187,17,7,5),(188,17,8,2),(189,17,9,1),(190,17,10,3),(191,17,11,5),(192,17,12,2),(193,18,1,3),(194,18,2,2),(195,18,3,4),(196,18,4,2),(197,18,5,4),(198,18,6,4),(199,18,7,4),(200,18,8,2),(201,18,9,5),(202,18,10,5),(203,18,11,2),(204,18,12,4),(205,19,1,3),(206,19,2,4),(207,19,3,5),(208,19,4,5),(209,19,5,3),(210,19,6,3),(211,19,7,5),(212,19,8,5),(213,19,9,5),(214,19,10,5),(215,19,11,3),(216,19,12,4),(217,20,1,1),(218,20,2,1),(219,20,3,1),(220,20,4,1),(221,20,5,1),(222,20,6,1),(223,20,7,1),(224,20,8,1),(225,20,9,1),(226,20,10,1),(227,20,11,1),(228,20,12,1),(229,21,1,5),(230,21,2,3),(231,21,3,4),(232,21,4,5),(233,21,5,4),(234,21,6,5),(235,21,7,4),(236,21,8,5),(237,21,9,3),(238,21,10,1),(239,21,11,2),(240,21,12,1),(241,22,1,4),(242,22,2,3),(243,22,3,2),(244,22,4,3),(245,22,5,3),(246,22,6,3),(247,22,7,2),(248,22,8,3),(249,22,9,2),(250,22,10,2),(251,22,11,3),(252,22,12,3),(253,23,1,4),(254,23,2,2),(255,23,3,3),(256,23,4,5),(257,23,5,3),(258,23,6,4),(259,23,7,5),(260,23,8,3),(261,23,9,4),(262,23,10,4),(263,23,11,3),(264,23,12,5),(265,24,1,3),(266,24,2,4),(267,24,3,3),(268,24,4,3),(269,24,5,3),(270,24,6,3),(271,24,7,2),(272,24,8,4),(273,24,9,4),(274,24,10,2),(275,24,11,3),(276,24,12,2),(277,25,1,3),(278,25,2,2),(279,25,3,1),(280,25,4,4),(281,25,5,5),(282,25,6,2),(283,25,7,2),(284,25,8,4),(285,25,9,4),(286,25,10,4),(287,25,11,4),(288,25,12,3),(289,26,1,3),(290,26,2,4),(291,26,3,2),(292,26,4,3),(293,26,5,4),(294,26,6,1),(295,26,7,4),(296,26,8,2),(297,26,9,4),(298,26,10,4),(299,26,11,2),(300,26,12,3),(301,27,1,2),(302,27,2,4),(303,27,3,2),(304,27,4,3),(305,27,5,4),(306,27,6,2),(307,27,7,4),(308,27,8,5),(309,27,9,2),(310,27,10,4),(311,27,11,4),(312,27,12,5),(313,28,1,4),(314,28,2,2),(315,28,3,3),(316,28,4,5),(317,28,5,2),(318,28,6,4),(319,28,7,3),(320,28,8,5),(321,28,9,2),(322,28,10,4),(323,28,11,5),(324,28,12,5),(325,29,1,2),(326,29,2,4),(327,29,3,2),(328,29,4,3),(329,29,5,4),(330,29,6,2),(331,29,7,3),(332,29,8,4),(333,29,9,4),(334,29,10,5),(335,29,11,2),(336,29,12,3),(337,30,1,2),(338,30,2,4),(339,30,3,1),(340,30,4,5),(341,30,5,4),(342,30,6,5),(343,30,7,2),(344,30,8,5),(345,30,9,4),(346,30,10,5),(347,30,11,3),(348,30,12,5),(349,31,1,3),(350,31,2,2),(351,31,3,4),(352,31,4,3),(353,31,5,4),(354,31,6,2),(355,31,7,4),(356,31,8,5),(357,31,9,2),(358,31,10,4),(359,31,11,5),(360,31,12,3),(361,32,1,3),(362,32,2,2),(363,32,3,4),(364,32,4,2),(365,32,5,3),(366,32,6,4),(367,32,7,2),(368,32,8,4),(369,32,9,2),(370,32,10,4),(371,32,11,3),(372,32,12,4),(373,33,1,3),(374,33,2,4),(375,33,3,3),(376,33,4,4),(377,33,5,3),(378,33,6,2),(379,33,7,2),(380,33,8,3),(381,33,9,3),(382,33,10,4),(383,33,11,5),(384,33,12,4),(385,34,1,3),(386,34,2,2),(387,34,3,5),(388,34,4,2),(389,34,5,1),(390,34,6,5),(391,34,7,4),(392,34,8,5),(393,34,9,3),(394,34,10,4),(395,34,11,3),(396,34,12,4),(397,35,1,1),(398,35,2,1),(399,35,3,1),(400,35,4,1),(401,35,5,1),(402,35,6,1),(403,35,7,1),(404,35,8,1),(405,35,9,1),(406,35,10,1),(407,35,11,1),(408,35,12,1),(409,36,1,5),(410,36,2,5),(411,36,3,5),(412,36,4,5),(413,36,5,5),(414,36,6,4),(415,36,7,5),(416,36,8,5),(417,36,9,4),(418,36,10,5),(419,36,11,4),(420,36,12,5),(421,37,1,4),(422,37,2,3),(423,37,3,4),(424,37,4,5),(425,37,5,4),(426,37,6,5),(427,37,7,3),(428,37,8,4),(429,37,9,5),(430,37,10,4),(431,37,11,5),(432,37,12,4);
/*!40000 ALTER TABLE `respuestas_evaluacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin'),(2,'hr'),(3,'user_personal'),(4,'user_empresa');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
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
  `empresa_id` int DEFAULT NULL,
  `departamento_id` int DEFAULT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellidos` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `rol_id` (`rol_id`),
  KEY `empresa_id` (`empresa_id`),
  KEY `departamento_id` (`departamento_id`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`) ON DELETE SET NULL,
  CONSTRAINT `usuarios_ibfk_3` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (3,2,2,NULL,'Piero','Funes','piero@hr.com','scrypt:32768:8:1$KqlOzQ6AdPNoeWpT$4cf1bbecd5cdd456b6b83d9272b857287f73a414054f21b3ef4545db2bffea955f9bbbc247fa7c2219f3177faff8df02354b45279a631a2d73284fdb45603ca5','2026-02-26 14:13:37'),(4,3,NULL,NULL,'123','123','123@123.com','scrypt:32768:8:1$NDh2HndS1V1q072j$4e70609cfd393776d25cb539b20d2eb01e4c9cbdeaf328283ea8866fafa1d4e8aabd29c2d6333d634db5cb2c3a112993b7e7ba50546b86a86f6d7b04013d0c2c','2026-03-04 13:52:25'),(5,3,NULL,NULL,'admin','admin','admin@admin.com','scrypt:32768:8:1$dml4I8oon51F1j9j$ba52d2d7b5390fba0dfecb61a25b7f823a85e7bf33d8852808d2780bd09052dbbd0ba26677076a38fa5ce2cb621ff49907038e0ae56780d343e6306df0dafa1a','2026-03-09 10:10:08'),(6,3,NULL,NULL,'Juan','aaaa','juan@juan.com','scrypt:32768:8:1$gqkxMI4nwpqTDemS$49de18ce529124ba3f21223201799d5a2e8550d1a8972a9e7ba8ae963d95767d47861d0ad82949c6735adfd26600032b7fe6f96b1c7fde4da7bd1515277fdb1f','2026-03-25 13:41:41'),(7,1,NULL,NULL,'admin111','admin111','admin111@admin.com','admin123','2026-03-26 12:30:04'),(8,1,NULL,NULL,'admin','admin','admin@resilio.com','scrypt:32768:8:1$di2IuLrXX2svASXN$d006393a3cca6dfcfdf90d5a0613a58ef8f1f034b771508ff1c04f0027683838bfc9e3541b2dd6944bcf3509abcb33d7c49160068a6fccda2c0ae73b02c79f15','2026-05-28 21:02:52'),(9,4,2,NULL,'Luis','Lopez','Luis@Acme.com','scrypt:32768:8:1$Gh5NApL4L6x1j2r3$c1b01df1b3d23c0bdc8313dbd37bc3ced9038eaf6ff3db9c6d7d420ca8bb9e7628a46bf141e3050572b4d19bebbb88925bd5995526f98106cdfc1c11baf8adb8','2026-05-28 23:27:42'),(10,4,2,NULL,'maria','Garcia','maria@acme.com','scrypt:32768:8:1$VAAV1piyORkRwQXD$30bf2e4166ce26a9f5a61dd8eb59a900e1e76ed4abd8b9f35b3d6344cca8d7280e72cebb0b112f9c0a5b6fe927d11e4a29264d90a7aebd34980c09ac9d024393','2026-05-29 00:02:46'),(11,4,2,NULL,'pepe','alvarez','pepe@acme.com','scrypt:32768:8:1$UBKyGyBBvv355uhw$7d490e790adfa7893e596cb1e475d3848594474ae49b85860ff76b5a75318656e71bbea9b77904a5078fc8e5b24474cf5716f5d403bad62fe70ce883b8d14f46','2026-05-29 00:16:59'),(12,4,2,NULL,'Piero','Funes Larios','piero@acme.com','scrypt:32768:8:1$KWBQht4m53fxwArV$eaa8019c3a6ee560ddd3c1fb0217d8bddcc6ea4ebe5eeafbb661559a7d6db4033a5442480074af0c9145a2c2053f1cae6949ef85e04bbe1a1fec618e8381cf04','2026-05-29 12:41:57');
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

-- Dump completed on 2026-06-08  1:32:03
