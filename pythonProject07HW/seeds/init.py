import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Student, Group, Grade, Subject

fake = Faker('en-GB')

def insert_students():
    groups = session.query(Group).all()
    for _ in range(50):
        student = Student(
            fullname=fake.name(),
            group_id=random.choice(groups).id
        )
        session.add(student)
def insert_teachers():
    for _ in range(5):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)
def insert_groups():
    for _ in range(3):
        group = Group(
            name=fake.name()
        )
        session.add(group)

def insert_subjects():
    teachers = session.query(Teacher).all()
    for _ in range(8):
        subject = Subject(
            name=fake.word(),
            teacher_id=random.choice(teachers).id
        )
        session.add(subject)
def insert_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(1,3)):
                grade = Grade(
                    student_id=student.id,
                    grade=random.randint(1,100),
                    subject_id=subject.id,
                    grade_date=fake.date_this_year()
                )
                session.add(grade)


if __name__ == '__main__':
    try:
        insert_groups()
        insert_students()
        insert_teachers()
        insert_subjects()
        insert_grades()
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()