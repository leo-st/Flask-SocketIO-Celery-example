from datetime import date, timedelta
from email.utils import parseaddr
from typing import Any

from werkzeug.security import generate_password_hash


def get_default_month_date(weeks_timedelta: int = 26):
    default_date = date.today() + timedelta(weeks=weeks_timedelta)
    default_date = date(year=default_date.year, month=default_date.month, day=1)
    return default_date


def parse_date(date_str: str, default_date: date = get_default_month_date()) -> date:
    try:
        parsed_date = date.fromisoformat(date_str)
        return parsed_date
    except:
        return default_date


def parse_int(input_int: Any, default_int: int = None, min_value: int = None, max_value: int = None) -> int | None:
    if input_int is None:
        return default_int
    
    try:
        return_value = int(input_int)
    except ValueError:
        return_value = default_int
    
    return_value = return_value if min_value is None else max(return_value, min_value)
    return_value = return_value if max_value is None else min(return_value, max_value)

    return return_value


def parse_float(input_float: Any, default_float: float = None) -> float | None:
    if input_float is None:
        return default_float
    
    try:
        return_value = float(input_float)
    except ValueError:
        return_value = default_float
    
    return return_value


def parse_int_list(input_ints: Any) -> list[int]:
    if input_ints is None:
        return []
    try:
        input_ints = iter(input_ints)
    except TypeError as te:
        input_ints = [input_ints]
    
    sanitized_ints = []
    for i in input_ints:
        try:
            i_int = int(i)
            sanitized_ints.append(i_int)
        except ValueError:
            continue
    
    return sanitized_ints

def parse_str_list(input_strs: Any) -> list[str]:
    if input_strs is None:
        return []
    try:
        input_strs = iter(input_strs)
    except TypeError as te:
        input_strs = [input_strs]
    
    sanitized_strs = []
    
    for i in input_strs:
        try:
            i_str = str(i)
            sanitized_strs.append(i_str.strip())
        except ValueError:
            continue
    
    return sanitized_strs


def parse_email(input_email: str, default_email: str = None) -> str | None:
    if input_email is None or not isinstance(input_email, str) or input_email.strip() == '':
        return default_email
    sanitized_email_str = input_email.strip().lower()
    if parseaddr(sanitized_email_str)[1] == '':
        return default_email
    return sanitized_email_str


def parse_non_empty_str(input_str: str, default_str: str = None) -> str | None:
    if input_str is None or not isinstance(input_str, str) or input_str.strip() == '':
        return default_str
    sanitized_input_str = input_str.strip()
    return sanitized_input_str


def parse_bool(input_bool: Any, default_bool: bool = True) -> bool:
    if isinstance(input_bool, bool):
        return input_bool
    if isinstance(input_bool, str):
        return input_bool.lower() in ('true', '1', 't')
    return default_bool
    

def parse_language(input_lang: str, default_lang: str = 'DE') -> str:
    valid_langs = ['DE', 'FR', 'IT', 'EN']

    if input_lang is None or not isinstance(input_lang, str) or input_lang.strip() == '':
        return default_lang
    
    sanitized_input_lang = input_lang.strip().upper()

    if sanitized_input_lang in valid_langs:
        return sanitized_input_lang
    else:
        return default_lang


def parse_hash_pw(input_pw: str, default_pw_hash: str = None) -> str:
    if input_pw is None or not isinstance(input_pw, str) or input_pw.strip() == '':
        return default_pw_hash
    
    # removes all white space (tabs, spaces, newlines etc.)
    sanitized_input_pw = ''.join(input_pw.strip().split())
    return generate_password_hash(sanitized_input_pw)
