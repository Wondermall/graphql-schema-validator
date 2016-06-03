import pytest
from click.testing import CliRunner
from graphql_schema_validator import cli
import os.path

SCHEMA = os.path.join(os.path.dirname(__file__), 'starwars.schema')
VALID_QUERY = os.path.join(os.path.dirname(__file__), 'valid.query')
INVALID_QUERY = os.path.join(os.path.dirname(__file__), 'invalid.query')

@pytest.fixture
def runner():
    return CliRunner()

def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code != 0
    assert result.exception

def test_cli_with_valid_query(runner):
    result = runner.invoke(cli.main, ['-s', SCHEMA, '-q', VALID_QUERY])
    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == 'Valid query'


def test_cli_with_invalid_query(runner):
    expected = 'Cannot query field "invalidProperty" on type "Faction".'

    result = runner.invoke(cli.main, ['-s', SCHEMA, '-q', INVALID_QUERY])
    assert result.exit_code != 0
    assert result.exception
    assert expected in result.output.strip()
