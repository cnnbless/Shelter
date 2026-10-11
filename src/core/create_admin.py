import asyncio
from sqlalchemy.future import select

from src.db.session import AsyncSessionLocal
from src.models.entities import User, Role
from src.core.security import get_password_hash


async def create_superuser(email: str, password: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.email == email))
        if result.scalars().first():
            print(f"User {email} already exists.")
            return

        hashed_password = get_password_hash(password)
        admin = User(email=email, hashed_password=hashed_password, role=Role.ADMIN)
        db.add(admin)
        await db.commit()
        print(f"Administrator {email} created successfully.")


if __name__ == "__main__":
    asyncio.run(create_superuser("admin@shelter.local", "admin12345"))
