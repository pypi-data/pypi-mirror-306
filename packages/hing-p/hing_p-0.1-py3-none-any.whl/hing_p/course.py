class Course:
    def __init__(self, course_name, max_students):
        self.course_name = course_name
        self.max_students = max_students
        self.students = []

    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student)
            return True
        return False

    def get_student_list(self):
        # 각 학생의 정보를 튜플 형태로 반환
        return [(student.name, student.age, student.student_id) for student in self.students]
