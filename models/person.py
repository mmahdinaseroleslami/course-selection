from exceptions.custom_exceptions import RequiredFieldException


class Person:
    def __init__(self, ID: int, first_name: str, last_name: str):
        if ID is None or not first_name or not last_name:
            raise RequiredFieldException("تمامی فیلدهای کلاس Person الزامی می‌باشند.")
        self.ID = int(ID)
        self.first_name = str(first_name)
        self.last_name = str(last_name)

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict:
        return {
            "ID": self.ID,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name()
        }
