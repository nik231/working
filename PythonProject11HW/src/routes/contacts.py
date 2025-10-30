from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas.contact import ContactSchema, ContactUpdateSchema, ContactResponseSchema

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=list[ContactResponseSchema])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts

@router.get('/{contact_id}', response_model=ContactResponseSchema)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id {contact_id} not found")
    return contact

@router.get('/search/contact_name', response_model=list[ContactResponseSchema])
async def get_contact_by_name(contact_name: str, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_name(contact_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with name {contact_name} not found")
    return contact

@router.get('/search/contact_surname', response_model=list[ContactResponseSchema])
async def get_contact_by_surname(contact_surname: str, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_surname(contact_surname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with surname {contact_surname} not found")
    return contact

@router.get('/search/contact_email', response_model=list[ContactResponseSchema])
async def get_contact_by_email(contact_email: str, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with email {contact_email} not found")
    return contact

@router.get('/search/next_week_birthdays', response_model=list[ContactResponseSchema])
async def get_next_week_contacts(db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_next_week_bd_contacts(db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact not found")
    return contact

@router.post('/', response_model=ContactResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact

@router.put('/{contact_id}', response_model=ContactUpdateSchema)
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id {contact_id} not found")
    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    return contact
