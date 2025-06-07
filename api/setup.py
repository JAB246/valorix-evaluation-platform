from setuptools import setup, find_packages

setup(
    name='valorix-backend',
    version='1.0.0',
    description='Valorix backend API - FastAPI, 23 agents, modular architecture',
    author='JAB246',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.110.0',
        'uvicorn[standard]>=0.29.0',
        'SQLAlchemy==1.4.50',
        'pydantic>=2.7.1',
        'pandas==2.2.3',
        'numpy==2.2.6',
        'python-dotenv',
        'python-jose',
        'passlib[bcrypt]',
        'asyncpg',
        'alembic',
        'httpx',
        'redis',
        'aioredis',
        'loguru',
    ],
)
