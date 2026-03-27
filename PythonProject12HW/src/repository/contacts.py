from sqlalchemy import select, func, or_, and_, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, date

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def get_contact_by_name(contact_name: str, db: AsyncSession, user: User):
    stmt = select(Contact).filter(func.lower(Contact.first_name) == contact_name.lower()).filter_by(user=user)
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def get_contact_by_surname(contact_surname: str, db: AsyncSession, user: User):
    stmt = select(Contact).filter(func.lower(Contact.last_name) == contact_surname.lower()).filter_by(user=user)
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def get_contact_by_email(contact_email: str, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(email=contact_email, user=user)
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def get_next_week_bd_contacts(db: AsyncSession, user: User):
    today = datetime.today().date()

    result = await db.execute(
        select(Contact).filter_by(user=user)
    )
    contacts = result.scalars().all()

    upcoming_contacts = []

    for contact in contacts:
        bd_str = contact.birthday
        try:
            bd_day = int(bd_str[:2])
            bd_month = int(bd_str[2:4])
        except:
            continue

        birthday_this_year = date(today.year, bd_month, bd_day)
        delta = (birthday_this_year - today).days

        if delta < 0:
            try:
                birthday_next_year = date(today.year + 1, bd_month, bd_day)
                delta = (birthday_next_year - today).days
            except:
                continue

        if 0 <= delta <= 7:
            upcoming_contacts.append(contact)

    return upcoming_contacts


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
