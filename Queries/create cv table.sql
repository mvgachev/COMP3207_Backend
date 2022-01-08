CREATE TABLE Cvs (
    cvId int NOT NULL IDENTITY(1,1) PRIMARY KEY,
    userId int NOT NULL,
	jobTitle varchar(255) NOT NULL,
	jobOffers varchar(255) NOT NULL,
	pdfFile varbinary(MAX) NOT NULL,
    CONSTRAINT FK_UserCV FOREIGN KEY (userId)
    REFERENCES Users(id)
);