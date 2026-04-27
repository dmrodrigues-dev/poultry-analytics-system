-- =============================================
-- SCHEMA: banco granja
-- Sistema de Gerenciamento de Granja de Galinhas Poedeiras Caipiras
-- Charset: utf8 / utf8_general_ci
-- =============================================

CREATE DATABASE IF NOT EXISTS `granja`
  DEFAULT CHARACTER SET utf8
  COLLATE utf8_general_ci;

USE `granja`;

-- ---------------------------------------------
-- Tabela: galpoes
-- Armazena os galpões da granja e suas áreas
-- ---------------------------------------------
CREATE TABLE `galpoes` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `area` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ---------------------------------------------
-- Tabela: lotes
-- Armazena os lotes de aves vinculados a galpões
-- ---------------------------------------------
CREATE TABLE `lotes` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `galpao` tinyint(3) unsigned NOT NULL,
  `nascimento` date NOT NULL,
  `inicio_producao` date NOT NULL,
  `descarte` date NOT NULL,
  `qtd_inicial` smallint(5) unsigned NOT NULL,
  `qtd_atual` smallint(5) unsigned NOT NULL,
  `fornecedor` varchar(30) NOT NULL,
  `racao` enum('R.Pre-Ini','R.Crescim','R.Inicial','R.Postura') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `galpao` (`galpao`),
  CONSTRAINT `lotes_ibfk_1` FOREIGN KEY (`galpao`) REFERENCES `galpoes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ---------------------------------------------
-- Tabela: preproducao
-- Registro diário de lotes em fase de crescimento
-- ---------------------------------------------
CREATE TABLE `preproducao` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `id_lote` tinyint(3) unsigned NOT NULL,
  `dia` date NOT NULL,
  `mortalidade` smallint(5) unsigned DEFAULT 0,
  `consumo_racao` decimal(6,2) DEFAULT 0.00,
  `consumo_agua` decimal(6,2) DEFAULT 0.00,
  `peso` decimal(4,3) DEFAULT 0.000,
  `categoria` enum('R.Pre-Ini','R.Inicial','R.Crescim') NOT NULL,
  `obs` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_lote` (`id_lote`),
  CONSTRAINT `preproducao_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lotes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ---------------------------------------------
-- Tabela: producao
-- Registro diário de produção por lote
-- ---------------------------------------------
CREATE TABLE `producao` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `id_lote` tinyint(3) unsigned NOT NULL,
  `dia` date NOT NULL,
  `ovos_inteiros` smallint(5) unsigned DEFAULT 0,
  `ovos_defeituosos` smallint(5) unsigned DEFAULT 0,
  `mortalidade` smallint(5) unsigned DEFAULT 0,
  `consumo_racao` decimal(6,2) DEFAULT 0.00,
  `consumo_agua` decimal(6,2) DEFAULT 0.00,
  `obs` text DEFAULT NULL,
  `taxa` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_lote` (`id_lote`),
  CONSTRAINT `producao_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lotes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ---------------------------------------------
-- Tabela: financeiro
-- Registro de movimentações financeiras
-- ---------------------------------------------
CREATE TABLE `financeiro` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `dia` date NOT NULL,
  `categoria` enum('Ovos','R.Pre-Ini','R.Crescim','R.Inicial','R.Postura') NOT NULL,
  `qtd` decimal(6,2) NOT NULL,
  `valor` decimal(8,2) NOT NULL,
  `forn_comp` varchar(40) DEFAULT NULL,
  `obs` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
