from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest

from utils import eleva_quadrado, requires_role


@pytest.mark.parametrize("test_input, expected", [(2, 4), (3, 9), (4, 16), (5, 25)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected


@pytest.mark.parametrize(
    "test_input,exc_class, msg", [
        ("a", TypeError, "unsupported operand type(s) for ** or pow(): \'str\' and \'int\'"),
        (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'"),
    ]
)
def test_eleva_quadrado_typeerror(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)

    assert str(exc.value) == msg


def test_require_role_success(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = 'admin'

    mocker.patch('utils.get_jwt_identity')
    mocker.patch('utils.db.get_or_404', return_value=mock_user)

    decorated_function = requires_role('admin')(lambda: "success")
    result = decorated_function()

    assert result == 'success'


def test_require_role_fail(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = 'normal'

    mocker.patch('utils.get_jwt_identity')
    mocker.patch('utils.db.get_or_404', return_value=mock_user)

    decorated_function = requires_role('admin')(lambda: "success")
    result = decorated_function()

    assert result == ({'message': 'User does not have access.'}, HTTPStatus.FORBIDDEN)
