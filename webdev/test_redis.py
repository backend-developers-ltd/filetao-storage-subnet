import os

 import pytest
 from passlib.context import CryptContext
 from database import get_database, startup, UserInDB, create_user, get_user

 pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

 UNUSED_DB = 15  # WARNING: This will clear the entire Redis database. Use with caution.
 PORT = 6379
 HOST = "localhost"

 os.environ["REDIS_HOST"] = HOST
 os.environ["REDIS_PORT"] = str(PORT)
 os.environ["REDIS_DB"] = str(UNUSED_DB)


 @pytest.fixture(scope="session", autouse=True)
 def redis_db():
     startup()
     redis_db = get_database()
     redis_db.flushdb()
     yield redis_db
     redis_db.flushdb()


 def test_user_creation_and_retrieval():
     fake_user = UserInDB(
         username="janedoe",
         hashed_password=pwd_context.hash("password123"),
         seed="b6825ec6168f72e90b1244b1d2307433ad8394ad65b7ef4af10966bc103a39bf",
         wallet_name="janedoe",
         wallet_hotkey="default",
         wallet_mnemonic="ocean bean until sauce near place labor admit dismiss long asthma tunnel",
     )
     create_user(fake_user)

     # Retrieve the user
     retrieved_user = get_user("janedoe")

     # Assert equality
     assert retrieved_user.dict() == {
         "username": "janedoe",
         "hashed_password": fake_user.hashed_password,
         "seed": fake_user.seed,
         "wallet_name": fake_user.wallet_name,
         "wallet_hotkey": fake_user.wallet_hotkey,
         "wallet_mnemonic": fake_user.wallet_mnemonic,
     }