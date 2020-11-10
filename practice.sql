-- create schema dbo

DROP TABLE IF EXISTS Contracts
DROP TABLE IF EXISTS Complects
DROP TABLE IF EXISTS Products
DROP TABLE IF EXISTS Units

DROP FUNCTION IF EXISTS GuarCalc

DROP TRIGGER IF EXISTS inserttrg
DROP TRIGGER IF EXISTS insertcmp
DROP TRIGGER IF EXISTS updatetrg
DROP TRIGGER IF EXISTS updateunt
DROP TRIGGER IF EXISTS deleteprd
DROP TRIGGER IF EXISTS deleteunt

CREATE TABLE Units (
    UnitCode varchar(256) PRIMARY KEY,
    UnitName varchar(256),
    IsProvided bit,
    ProviderName varchar(256),
)

CREATE TABLE Products (
    ProductID varchar(256) PRIMARY KEY,
    ProductName varchar(256),
)

CREATE TABLE Complects (
    LineNum int PRIMARY KEY IDENTITY,
    ProductId varchar(256),
    ProductName varchar(256),
    UnitCode varchar(256),
    UnitName varchar(256),
    UnitAmt int,
    CONSTRAINT FK_Products_ProductId FOREIGN KEY (ProductId) REFERENCES Products(ProductId),
    CONSTRAINT FK_Products_UnitCode FOREIGN KEY (UnitCode) REFERENCES Units(UnitCode),
)

CREATE TABLE Contracts (
    Id int PRIMARY KEY IDENTITY (10000000, 1),
    Customer varchar(256),
    ConclDate date,
    ProductKey varchar(256),
    ProductName varchar(256),
    MakingDate date,
    GuaranteePeriod int,
    SaleDate date,
    GuarEndDate date,
    Cost money,
    CONSTRAINT FK_Contracts_ProductID FOREIGN KEY (ProductKey) REFERENCES Products(ProductId),
);
GO

CREATE FUNCTION GuarCalc(@GPer int, @SDate date)
    RETURNS date
        BEGIN
            DECLARE @y INT, @m INT, @d INT, @counter INT, @s varchar(10)
--             SET @counter = GPer;
            SET @counter = @GPer;
            SET @y = YEAR(@SDate);
            SET @m = MONTH(@SDate);
            SET @d = DAY(@SDate);
            WHILE @y <= 9999
                BEGIN
                    WHILE @m <= 12
                        BEGIN
                            WHILE (@m = 2 and @y % 4 = 0 and @d <= 29) or (@m = 2 and @y % 4 != 0 and @d <= 28) or ((@m = 1 or @m = 3 or @m = 5 or @m = 7 or @m = 8 or @m = 10 or @m = 12) and @d <= 31) or ((@m = 4 or @m = 6 or @m = 9 or @m = 11) and @d <= 30)
                                BEGIN
                                    IF @counter = 0 BREAK
                                    SET @d = @d + 1
                                    SET @counter = @counter - 1
                                end
                            IF @counter = 0 BREAK
                            SET @m = @m + 1
                            SET @d = 1
                        end
                    IF @counter = 0 BREAK
                    SET @y = @y + 1
                    SET @m = 1
                end
            SET @s = CAST(@y as varchar(4)) + '.' + CAST(@m as varchar(2)) + '.' + CAST(@d as varchar(2))
            RETURN CAST(@s as DATE)
        end
GO

CREATE TRIGGER insertcmp ON Complects AFTER INSERT AS
BEGIN
    UPDATE Complects SET ProductName = (SELECT ProductName from Products WHERE Products.ProductID in (SELECT ProductId from inserted)) WHERE ProductId in (SELECT ProductId from inserted)
    UPDATE Complects SET UnitName = (SELECT UnitName from Units WHERE Units.UnitCode in (SELECT UnitCode from inserted)) WHERE UnitCode in (SELECT UnitCode from inserted)
end
GO

CREATE TRIGGER inserttrg ON Contracts AFTER INSERT AS
Begin
    UPDATE Contracts SET ProductName = (SELECT ProductName from Products WHERE ProductID = (SELECT ProductKey from inserted)) WHERE Contracts.ProductKey = (SELECT ProductKey from inserted)
end
GO

CREATE TRIGGER updatetrg ON Contracts AFTER UPDATE AS
BEGIN
    UPDATE Contracts SET GuarEndDate = dbo.GuarCalc(GuaranteePeriod, SaleDate)
    WHERE Id in (SELECT Id FROM inserted) AND SaleDate is not NULL AND GuaranteePeriod is not NULL
END
GO

CREATE TRIGGER updateunt ON Units AFTER UPDATE AS
BEGIN
    UPDATE Units SET IsProvided = 1 WHERE UnitCode in (SELECT UnitCode FROM inserted) AND ProviderName != '-'
    UPDATE Units SET IsProvided = 0 WHERE UnitCode in (SELECT UnitCode FROM inserted) AND ProviderName = '-'
end
GO
CREATE TRIGGER deleteunt ON Units INSTEAD OF DELETE AS
BEGIN
    DELETE FROM Complects WHERE UnitCode in (SELECT UnitCode FROM deleted)
    DELETE FROM Units WHERE UnitCode in (SELECT UnitCode FROM deleted)
end
GO
CREATE TRIGGER deleteprd ON Products INSTEAD OF DELETE AS
BEGIN
    DELETE FROM Complects WHERE ProductID in (SELECT ProductId FROM deleted)
    DELETE FROM Complects WHERE ProductId in (SELECT ProductID FROM deleted)
end
GO
-- Заполнение Таблиц
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES ('2646.03.03.000', N'Реверс-редуктор', 0, '-')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES ('2703.03.04.000', N'Колесная пара', 0,  '-')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES ('DIWA5E', N'Гидропередача', 1, 'DIWA')
-- МГМ4ОС.00.00.000
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'7029803792', N'Датчик сигнализатора температуры', 1, N'г.Калуга КЗАМЭ')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'4573827162', N'Датчик скорости', 1, N'г.Владимир Автоприбор')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'4573827163', N'Датчик аварийного давления масла', 1, N'г.Владимир Автоприбор')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'8156497126', N'Модуль электронной системы управления', 1, N'г.С-Петербург"АБИТ"')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'7521212914', N'Компрессор', 1, N'г.Первомайск ОАО"Транспневматика"')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'3169748299', N'Гидромотор', 1, N'г.Люберцы "ГидроСнабХолдинг"')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'4289527887', N'Вал карданный', 1, N'г.Гродно завод карданных валов')
-- 2646ГП.00.00.000
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'6678471221', N'Батарея аккумуляторная', 1, N'г.Подольск Аккумуляторный з-д')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'4830048390', N'Тахометр электронный', 1, N'г.Владимир Автоприбор')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'3968969689', N'Выпрямитель сварочный', 1, N'г.Санкт-Петербург АО "Северная электротехническая компания"')
INSERT INTO Units(UnitCode, UnitName, IsProvided, ProviderName) VALUES (N'2206452298', N'Цилиндр тормозной', 1, N'г.Первомайск ОАО"Транспневматика"')
GO
--
INSERT INTO Products(ProductID, ProductName) VALUES ('МГМ4ОС.00.00.000', 'МГМ-4')
INSERT INTO Products(ProductID, ProductName) VALUES ('2646ГП.00.00.000', 'АГД-1А')
INSERT INTO Products(ProductID, ProductName) VALUES ('МГМ5.00.00.000', 'МГМ-5')
INSERT INTO Products(ProductID, ProductName) VALUES ('2703.00.00.000', N'АГС-1')
--
INSERT INTO Complects(ProductId, ProductName, UnitCode, UnitName, UnitAmt) VALUES ('2646ГП.00.00.000','АГД-1А', '2646.03.03.000', N'Реверс-редуктор', 1)
INSERT INTO Complects(ProductId, ProductName, UnitCode, UnitName, UnitAmt) VALUES ('2646ГП.00.00.000','АГД-1А', '2703.03.04.000', N'Колесная пара', 2)
INSERT INTO Complects(ProductId, ProductName, UnitCode, UnitName, UnitAmt) VALUES ('2646ГП.00.00.000','АГД-1А', 'DIWA5E', N'Гидропередача', 1)
INSERT INTO Complects(ProductId, ProductName, UnitCode, UnitName, UnitAmt) VALUES ('МГМ4ОС.00.00.000', 'МГМ-4', N'7029803792', N'Датчик сигнализатора температуры', 1)
INSERT INTO Complects(ProductId, ProductName, UnitCode, UnitName, UnitAmt) VALUES ('МГМ4ОС.00.00.000', 'МГМ-4', N'4573827162', N'Датчик скорости', 1)
--
INSERT INTO Contracts(Customer, ConclDate, ProductKey, ProductName, MakingDate, GuaranteePeriod, SaleDate, Cost)
VALUES (N'Горнодобывающий комбинат', CAST('2016-11-21' as date), N'2703.00.00.000', N'АГС-1', CAST('2017-05-21' as date), 730, CAST('2017-06-20' as date), CAST(12000000 as money))



