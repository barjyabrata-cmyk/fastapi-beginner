from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname : str
    database_port: str
    database_password: str
    database_name :str
    database_username :str
    secret_key: str
    algorithm: str
    access_token_expire_minutes:int

    
    model_config = SettingsConfigDict(env_file=".env")


settings=Settings()


# THIS FILE and .env file is made for save the credentials informatio ;ike databasae port url secret key passwor
# not directly in file...rather than save them in enviornmental varaibale and import them using basesetting
