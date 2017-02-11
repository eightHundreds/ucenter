# -*- coding: utf-8 -*-
from enum import Enum

class UcEnum(Enum):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return super().__eq__(other)
        else:
            return str(self.value) == str(other)

class UserRegisterEnum(UcEnum):
    SUCCESS = 0
    USER_NAME_ILLEGAL = -1
    CONTAINS_INVALID_WORDS = -2
    USER_NAME_EXISTS = -3
    INCORRECT_EMAIL_FORMAT = -4
    EMAIL_NOT_ALLOWED = -5
    EMAIL_HAS_BEEN_REGISTERED = -6

class UserLoginResult(UcEnum):
    Success = 0
    NotExist = -1
    PassWordError = -2
    QuestionError = -3

class UserEmailCheckResult(UcEnum):
    Success = 1
    IncorrectEmailFormat = -4
    EmailNotAllowed = -5
    EmailHasBeenRegistered = -6

class UserNameCheckResult(UcEnum):
    Success = 1
    UserNameIllegal = -1
    ContainsInvalidWords = -2
    UserNameExists = -3