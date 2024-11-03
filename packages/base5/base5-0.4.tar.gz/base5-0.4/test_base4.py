from hamcrest import assert_that, equal_to, calling, raises
from base5 import (d5encode, d5decode, d5encode_check, d5decode_check)

base4_ALPHABET = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"


def test_simple_encode():
    data = d5encode(b'hello world', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b'K3*J+EGLBVAYYB36'))


def test_leadingz_encode():
    data = d5encode(b'\0\0hello world', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b'00K3*J+EGLBVAYYB36'))


def test_encode_empty():
    data = d5encode(b'', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b''))


def test_simple_decode():
    data = d5decode('K3*J+EGLBVAYYB36', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b'hello world'))


def test_simple_decode_bytes():
    data = d5decode(b'K3*J+EGLBVAYYB36', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b'hello world'))


def test_autofix_decode_bytes():
    data = d5decode(
        b'K3*J+EGLBVAYYB36', alphabet=base4_ALPHABET, autofix=True)
    assert_that(data, equal_to(b'hello world'))


def test_leadingz_decode():
    data = d5decode('00K3*J+EGLBVAYYB36', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b'\0\0hello world'))


def test_leadingz_decode_bytes():
    data = d5decode(b'00K3*J+EGLBVAYYB36', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b'\0\0hello world'))


def test_empty_decode():
    data = d5decode('1', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b'\x01'))


def test_empty_decode_bytes():
    data = d5decode(b'1', alphabet=base4_ALPHABET)
    assert_that(data, equal_to(b'\x01'))


def test_check_str():
    data = 'hello world'
    out = d5encode_check(data, alphabet=base4_ALPHABET)
    assert_that(out, equal_to(b'AHN49RN6G8B%AWUALA8K2D'))
    back = d5decode_check(out, alphabet=base4_ALPHABET)
    assert_that(back, equal_to(b'hello world'))


def test_autofix_check_str():
    data = 'AHN49RN6G8B%AWUALA8K2D'
    back = d5decode_check(data, alphabet=base4_ALPHABET, autofix=True)
    assert_that(back, equal_to(b'hello world'))


def test_autofix_not_applicable_check_str():
    charset = base4_ALPHABET.replace(b'x', b'l')
    msg = b'hello world'
    enc = d5encode_check(msg, alphabet=base4_ALPHABET)
    modified = enc.replace(b'x', b'l').replace(b'o', b'0')
    back = d5decode_check(modified, alphabet=charset, autofix=True)
    assert_that(back, equal_to(msg))


def test_check_failure():
    data = '3vQB7B6MrGQZaxCuFg4oH'
    assert_that(calling(d5decode_check).with_args(data), raises(ValueError))


def test_invalid_input():
    data = 'xyz0'
    assert_that(
        calling(d5decode).with_args(data),
        raises(ValueError, "Invalid character '0'"))
