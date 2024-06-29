import datetime
from tinydb import TinyDB, Query
from tinydb.table import Table, Document

class Person:
    
    @staticmethod
    def load_person_data() -> Table:
        '''
        A `staticmethod` that knows where the person Database is and returns a TinyDB-Table with the Persons
        ### Parameters
        - Args:
        - Returns:
            - (`TinyDB.Table`): A table with all Persondata
        '''
        return TinyDB("data/person_db.json").table("persons")


    @staticmethod
    def load_by_id(id) -> dict:
        '''
        A `staticmethod` that loads a person by id
        ### Parameters
        - Args:
        - Returns:
            - person (``): 
        '''
        try:
            person = Person.load_person_data().get(doc_id=id)
            return person
        except:
            raise ValueError("Person with ID {} not found".format(id))                            


    @staticmethod
    def get_persons_list(persons_table) -> list[str]:
        '''
        A `staticmethod` that takes the persons-table and returns a list of strings auf all person names
        ### Parameters
        - Args:
            - persons_table (`TinyDB.table_class`):
        - Returns:
            - list_of_names (`list`): 
        '''
    
        list_of_names = []
        for eintrag in persons_table:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    

    @staticmethod
    def find_person_data_by_name(suchstring:str) -> (Document | None):
        '''
        A `staticmethod` that takes the lastname, firstname as a string and returns the person as a TinyDB-Document
        ### Parameters
        - Args:
            - suchstring (`str`): String in the format "lastname, firstname"
        - Returns:
            - person (`TinyDB.Document`):
        '''

        if suchstring == "None":
            return None

        lastname_firstname = suchstring.split(", ")

        query = Query()
        found_list = Person.load_person_data().search((query.lastname == lastname_firstname[0]) and (query.firstname == lastname_firstname[1]))
        if found_list == []:
            return None
        else:
            return found_list[0]


    def find_person_id_by_name(suchstring:str) -> (int | None):
        '''
        A `staticmethod` that takes the lastname, firstname as a string and returns the person as a TinyDB-Document
        ### Parameters
        - Args:
            - suchstring (`str`): String in the format "lastname, firstname"
        - Returns:
            - person_id (`int`):
        '''

        if suchstring == "None":
            return None

        lastname_firstname = suchstring.split(", ")

        query = Query()
        found_list = Person.load_person_data().search((query.lastname == lastname_firstname[0]) and (query.firstname == lastname_firstname[1]))
        if found_list == []:
            return None
        else:
            return found_list[0].doc_id
        

    @staticmethod
    def calc_age(date_of_birth:int) -> int:
        '''
        A `staticmethod` that calculates the age
        ### Parameters
        - Args:
            - date_of_birth (`int`): the year of birth          #may be changed later
        - Returns:
            - age (`int`)
        '''
        today = datetime.date.today()
        age = today.year - date_of_birth
        return age


    @staticmethod
    def calc_max_hr(age : int) -> int:
        '''
        A `staticmethod` that calculates the maximum heartrate in bpm from the age
        ### Parameters
        - Args:
            - age (`int`)
        - Returns:
            - max_hr_bpm (`int`)
        '''    
        max_hr_bpm =  223 - 0.9 * age
        return int(max_hr_bpm)
    
    """
    # not functional or used
    @staticmethod 
    def get_ekg_list(persons_table:Table): # Mögliche Funktion für die Anzeige aller EKGs evtl löschen
        '''
        A `staticmethod` that takes the persons-table and returns a list of all person names
        ### Parameters
        - Args:
            - persons_table (`tinydb.Table`)
        - Returns:
            - list_of_ekgs (`list[]`)
        '''
        list_of_ekgs = []
        for eintrag in person_data:
            ekg_tests = eintrag.get("ekg_tests", [])  # Get the list of ekg_tests or an empty list if it doesn't exist
            for ekg_test in ekg_tests:
                ekg_id = ekg_test.get("id")
                ekg_date = ekg_test.get("date")
                list_of_ekgs.append((ekg_id, ekg_date))
        return list_of_ekgs
    """
 

    def __init__(self, person_id:int):
        person_table = Person.load_person_data().get(doc_id=person_id)
        self.year_of_birth = person_table["year_of_birth"]
        self.firstname = person_table["firstname"]
        self.lastname = person_table["lastname"]
        self.picture_path = person_table["picture_path"]
        self.id = person_table.doc_id
        self.age = self.calc_age(self.year_of_birth)
        self.max_hr_bpm = self.calc_max_hr(self.age)
        


if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    print(type(persons))
    print(type(persons.get(doc_id=1)))
    person_names = Person.get_persons_list(persons)
    print(person_names)
    print(Person.find_person_data_by_name("Huber, Julian"))




    #print(person_names)
    #print(Person.find_person_data_by_name("Huber, Julian"))
    #print(Person.calc_age())
    #print(Person.calc_max_hr())
    #print(Person.load_by_id().age)
    #print(Person.load_by_id(2).max_hr_bpm)
    #print(Person.load_by_id(2).age)
    #print(Person.get_ekg_list(persons))
    #print(Person.ekgs_of_person(persons, 1))
    ##print(Person.ekgs_of_person(persons.table('ekg_tests'), 1))
    