import duckdb
import csv
import git
import json
import pytest
from click.testing import CliRunner
from git_logger.cli import cli

@pytest.fixture
def git_repo(tmpdir):
    repo = git.Repo.init(tmpdir)
    yield repo

def test_cli_json(tmpdir, git_repo):
    # Create a JSON file and commit it
    json_file = (tmpdir / "data.json")
    data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 40}]
    with open(json_file, "w") as f:
        json.dump(data, f)

    git_repo.git.checkout('-b', 'main')  # Create and checkout the 'main' branch
    git_repo.index.add([json_file])
    git_repo.index.commit("First commit")

    # Test the cli command with the JSON file
    db_name = str(tmpdir / "test.db")
    table_name = "my_table"
    repo_path = str(tmpdir)

    runner = CliRunner()
    result = runner.invoke(cli, [str(json_file), db_name, "--table_name", table_name, "--repo_path", repo_path])
    assert result.exit_code == 0
    assert f"Git history has been logged to {db_name}.{table_name}" in result.output

    # Check that the data was inserted correctly
    with duckdb.connect(db_name) as con:
        result = con.sql(f"SELECT * FROM {table_name}").fetchall()
        assert len(result) == 2
        assert set(row[2] for row in result) == {"Alice", "Bob"}

def test_cli_csv(tmpdir, git_repo):
    # Create a CSV file and commit it
    csv_file = (tmpdir / "data.csv")
    data = [["name", "age"], ["Alice", "30"], ["Bob", "40"]]
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    git_repo.git.checkout('-b', 'main')  # Create and checkout the 'main' branch
    git_repo.index.add([csv_file])
    git_repo.index.commit("First commit")

    # Test the cli command with the CSV file
    db_name = str(tmpdir / "test.db")
    table_name = "my_table"
    repo_path = str(tmpdir)

    runner = CliRunner()
    result = runner.invoke(cli, [str(csv_file), db_name, "--table_name", table_name, "--repo_path", repo_path])
    assert result.exit_code == 0
    assert f"Git history has been logged to {db_name}.{table_name}" in result.output

    # Check that the data was inserted correctly
    with duckdb.connect(db_name) as con:
        result = con.sql(f"SELECT * FROM {table_name}").fetchall()
        assert len(result) == 2
        assert set(row[2] for row in result) == {"Alice", "Bob"}