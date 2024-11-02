"""
The root module of the library provides a unified API for accessing the main 
components of the library. It includes functionalities for loading data from 
various sources, managing documents (such as invoices), and delivering 
files or documents through email, SFTP, or S3.

Classes:
    CSVDataSource: Loads data from CSV files.
    DataFrameDataSource: Loads data from polars DataFrames.
    PostgreSQLDataSource: Loads data from PostgreSQL databases.
    XLSXDataSource: Loads data from XLSX files.
    Template: Manages HTML templates with associated CSS and assets.
    EmailMessageBuilder: Helps in constructing email messages.
    EmailSender: Sends emails via an SMTP server.
    S3Delivery: Uploads files to Amazon S3.
    SFTPDelivery: Transfers files via SFTP.
    SMTPConfig: Configures the SMTP server for sending emails.
    TemplateManager: Manages document templates and integrates them with data sources.
"""

from .data_sources import (
    CSVDataSource,
    DataFrameDataSource,
    PostgreSQLDataSource,
    XLSXDataSource,
)
from .models import Template
from .services import (
    EmailMessageBuilder,
    EmailSender,
    AWSConfig,
    S3Delivery,
    SFTPDelivery,
    SMTPConfig,
    TemplateManager,
)

__all__ = [
    "CSVDataSource",
    "DataFrameDataSource",
    "PostgreSQLDataSource",
    "XLSXDataSource",
    "Template",
    "EmailMessageBuilder",
    "EmailSender",
    "AWSConfig",
    "S3Delivery",
    "SFTPDelivery",
    "SMTPConfig",
    "TemplateManager",
]
