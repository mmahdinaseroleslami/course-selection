class CourseSelectionException(Exception):
    def __init__(self, message: str = "خطای سیستم انتخاب واحد"):
        self.message = message
        super().__init__(self.message)


class StudentNotFoundException(CourseSelectionException):
    pass


class DuplicateStudentException(CourseSelectionException):
    pass


class ProfessorNotFoundException(CourseSelectionException):
    pass


class DuplicateProfessorException(CourseSelectionException):
    pass


class CourseNotFoundException(CourseSelectionException):
    pass


class DuplicateCourseException(CourseSelectionException):
    pass


class CapacityFullException(CourseSelectionException):
    pass


class InvalidCapacityException(CourseSelectionException):
    pass


class DuplicateCourseSelectionException(CourseSelectionException):
    pass


class CourseNotSelectedException(CourseSelectionException):
    pass


class AlreadyAssignedToSameProfessorException(CourseSelectionException):
    pass


class CourseAlreadyHasProfessorException(CourseSelectionException):
    pass


class CourseHasNoProfessorException(CourseSelectionException):
    pass


class RequiredFieldException(CourseSelectionException):
    pass