from faker.providers.ssn.uk_UA import select_gender
from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Student, Teacher, Group, Subject
from conf.db import session


def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grade g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subject_id == 2).group_by(Student.id).order_by(
        desc('average_grade')).first()
    return result


def select_03():
    result = session.query(Student.group_id, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subject_id == 3).group_by(Student.group_id).order_by(
        desc('average_grade')).all()
    return result


def select_04():
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).all()
    return result


def select_05():
    result = session.query(Subject.teacher_id, Subject.name) \
        .select_from(Subject).filter(Subject.teacher_id == 3).all()
    return result


def select_06():
    result = session.query(Student.group_id, Student.fullname) \
        .select_from(Student).filter(Student.group_id == 7).order_by(Student.fullname).all()
    student_list = []
    for r in result:
        if r[1] not in student_list:
            student_list.append(r[1])
        groupid = r[0]
    return groupid, student_list


def select_07():
    result = session.query(Student.group_id, Grade.subject_id, Student.fullname, Grade.grade) \
        .select_from(Grade).join(Student).filter(and_(Student.group_id == 8, Grade.subject_id == 1)).order_by(
        desc(Grade.grade)).all()
    return result


def select_08():
    result = session.query(Subject.name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Subject).filter(Subject.teacher_id == 3).group_by(Subject.name).order_by(
        desc('average_grade')).all()
    return result


def select_09():
    result = session.query(Student.fullname, Grade.subject_id) \
        .select_from(Grade).join(Student).filter(Grade.student_id == 6).order_by(Grade.subject_id).all()
    subject_list = []
    for r in result:
        if r[1] not in subject_list:
            subject_list.append(r[1])
            student_name = r[0]
    return (student_name, subject_list)


def select_10():
    result = session.query(Grade.student_id, Student.fullname, Subject.name) \
        .select_from(Grade).join(Subject).join(Student).filter(
        and_(Grade.student_id == 6, Subject.teacher_id == 3)).order_by(Grade.subject_id).all()
    subject_list = []
    for r in result:
        if r[2] not in subject_list:
            subject_list.append(r[2])
            student_name = r[1]
    return (student_name, subject_list)


def select_11():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).join(Subject).filter(
        and_(Grade.student_id == 1, Subject.teacher_id == 5)).group_by(Student.fullname).all()
    return result

def select_12():
    result = session.query(Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade).join(Student).filter(and_(Student.group_id == 8, Grade.subject_id == 1)).order_by(desc(Grade.grade_date)).all()
    student_list = []
    output_list = []
    for r in result:
        if r[0] not in student_list:
            student_list.append(r[0])
            output_list.append(r)

    return output_list


if __name__ == '__main__':
    # print(select_01())
    # print(select_02())
    # print(select_03())
    # print(select_04())
    # print(select_05())
    print(select_06())
    # print(select_07())
    # print(select_08())
    # print(select_09())
    print(select_10())
    print(select_12())
