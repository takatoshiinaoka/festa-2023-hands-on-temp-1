import boto3
import pytest


@pytest.fixture(scope="session")
def dynamodb_resource():
    return boto3.resource("dynamodb", endpoint_url="http://localhost:4566")


@pytest.fixture(scope="session")
def dynamodb_client():
    return boto3.client("dynamodb", endpoint_url="http://localhost:4566")


@pytest.fixture(scope="function")
def single_key_dynamodb_table(request, dynamodb_client, dynamodb_resource):
    items = request.param

    name = "single-key-table"
    dynamodb_client.create_table(
        TableName=name,
        AttributeDefinitions=[
            {
                "AttributeName": "hash",
                "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "hash",
                "KeyType": "HASH"
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    if items:
        table = dynamodb_resource.Table(name)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    yield name

    dynamodb_client.delete_table(
        TableName=name
    )


@pytest.fixture(scope="function")
def double_keys_dynamodb_table(request, dynamodb_client, dynamodb_resource):
    items = request.param

    name = "double-keys-table"
    dynamodb_client.create_table(
        TableName=name,
        AttributeDefinitions=[
            {
                "AttributeName": "hash",
                "AttributeType": "S"
            },
            {
                "AttributeName": "range",
                "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "hash",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "range",
                "KeyType": "RANGE"
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    if items:
        table = dynamodb_resource.Table(name)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    yield name

    dynamodb_client.delete_table(
        TableName=name
    )


class TestGetItem:
    @pytest.mark.parametrize(
        "single_key_dynamodb_table, key, expected", [
            (
                [],
                {
                    "hash": "test"
                },
                None
            ),
            (
                [
                    {
                        "hash": "test",
                        "name": "テストデータ",
                        "size": 9
                    },
                    {
                        "hash": "test_02",
                        "name": "テストデータ 02",
                        "size": 11
                    }
                ],
                {
                    "hash": "test"
                },
                {
                    "hash": "test",
                    "name": "テストデータ",
                    "size": 9
                }
            ),
        ], indirect=["single_key_dynamodb_table"]
    )
    def test_single_key(self, dynamodb_resource, single_key_dynamodb_table, key, expected):
        table = dynamodb_resource.Table(single_key_dynamodb_table)
        resp = table.get_item(Key=key)
        assert resp.get("Item") == expected

    @pytest.mark.parametrize(
        "double_keys_dynamodb_table, key, expected", [
            (
                [],
                {
                    "hash": "test",
                    "range": "first"
                },
                None
            ),
            (
                [
                    {
                        "hash": "test",
                        "range": "first",
                        "name": "テストデータ01",
                    }
                ],
                {
                    "hash": "test",
                    "range": "first"
                },
                {
                    "hash": "test",
                    "range": "first",
                    "name": "テストデータ01",
                }
            ),
        ], indirect=["double_keys_dynamodb_table"]
    )
    def test_double_keys(self, dynamodb_resource, double_keys_dynamodb_table, key, expected):
        table = dynamodb_resource.Table(double_keys_dynamodb_table)
        resp = table.get_item(Key=key)
        assert resp.get("Item") == expected