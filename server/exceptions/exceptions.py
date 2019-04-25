"""Execptions.py holds all of the exceptions for the program."""


class Error(Exception):
    """Base class for other exceptions"""
    pass


class BadEmailError(Error):
    """Raised when email is malformed"""
    pass


class ShortPasswordError(Error):
    """Raised when password is too short"""
    pass


class UsernameInUseError(Error):
    """Raised when username is already in use"""
    pass


class EmailInUseError(Error):
    """Raised when email is already in use"""
    pass


class BadLoginError(Error):
    """Raised when login credentials are bad"""
    pass


class BadTokenError(Error):
    """Raised when a login token is bad"""
    pass


class NoFileUploadedError(Error):
    """Raised when no file exists"""
    pass


class EmptyFileError(Error):
    """Raised when file is empty"""
    pass


class FileTooLargeError(Error):
    """Raised when file is too large"""
    pass


class BadFileExtError(Error):
    """Raised when file is a bad file"""
    pass


class SQLExecutionError(Error):
    """Raised when query does not execute correctly"""
    pass
