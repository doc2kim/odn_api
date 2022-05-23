import environ

env = environ.Env()

environ.Env.read_env()

print(env('RDS_HOST'))