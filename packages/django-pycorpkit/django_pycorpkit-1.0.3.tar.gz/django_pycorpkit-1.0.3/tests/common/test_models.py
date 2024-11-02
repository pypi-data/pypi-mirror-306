from pycorpkit.common.models.organisation import Organisation
from pycorpkit.common.models.person import Person


def test_person_full_names_all_names():
    from model_bakery import baker
    person = baker.make(Person, first_name="Josh", last_name="Doe", surname="Surname")
    assert person.full_name == "Josh Doe Surname"
    assert person.__str__() == "Josh Doe Surname"


def test_person_full_names_only_two_names():
    from model_bakery import baker
    person = baker.make(Person, first_name="Josh", last_name="Doe")
    assert person.full_name == "Josh Doe"
    assert person.__str__() == "Josh Doe"


def test_organisation_str_():
    from model_bakery import baker
    organisation = baker.make(Organisation, name="Tech Inc")
    assert organisation.__str__() == "Tech Inc"
