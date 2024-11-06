class Course:
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} - [{self.duration} horas] ({self.link})"

courses = [
    Course("Personalización Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-linux/"),
    Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Python ofensivo", 35, "https://hack4u.io/cursos/python-ofensivo/"),
    Course("Introducción al hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course

    return None
