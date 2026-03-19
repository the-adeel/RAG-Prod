from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJzVlFFr2zAUhf+K0FMH2Ui8ZC1+SwOlK10K3RiDMYwi3ziisuRK11tL5v9erpxEjtOUDv"
    "awPfrcI+mcD1lrXtoctH83BafkiqdszY0ogaesNxkwLqoq6iSgWOhgFdGz8OiERJ6ypdAe"
    "Bozn4KVTFSpreMpMrTWJVnp0yhRRqo26ryFDWwCuwPGUff8xYFyZHB7Abz+ru2ypQOd7UV"
    "VOZwc9w8cqaB8NXgQjnbbIpNV1aaK5esSVNTu3MkhqAQacQKDt0dUUn9Jtem4btUmjpY3Y"
    "WZPDUtQaO3VfyUBaQ/yUQSq85gWd8jYZjU/HZ+8/jM8GjIckO+W0aevF7u3CQGD+hTdhLl"
    "C0joAxcvsJzlOkA3izlXDP0+ss6SH06PoIt8BeYrgVIsR4cf4SxVI8ZBpMgXTBk8nkBWZf"
    "p7ezy+ntSTKZvKE21gnZ3vH5ZpS0MwIbQdKv8QcQN/b/E+BoOHwFwNFweBRgmO0DlNYgtP"
    "/gPsSrzzfz5yF2lvRA5koi+8208vhvAm2O86O+FLr0/l53sZ18mn7rE51d35yH/tZj4cIu"
    "YYNz3jT0WC43j+Xu9VwIefdLuDw7mNjEHvMejsqk7CvCiCKwosZN8wS6eQTQ"
)
