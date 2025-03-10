"""A collection of tools made available to the system."""

from faker import Faker
from faker_education import SchoolProvider

fake = Faker()
fake.add_provider(SchoolProvider)

def get_school_information(school_name="", zip_code=""):
    """Return only what the agent needs about a school."""
    school = fake.school_object()
    to_return = {
        "zip_code": fake.postalcode_in_state(school["state"]),
        "school_name": school["school"],
        "school_district": school["district"]
    }
    return to_return
