import json
import datetime
from tinydb import TinyDB

class Person:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where the person Database is and returns a TinyDB-Table with the Persons"""
        return TinyDB("data/person_db.json").table("persons")

    @staticmethod
    def load_by_id(id):
        """A Function that loads a person by id"""
        try:
            person = Person.load_person_data().get(doc_id=id)
            return person
        except:
            raise ValueError("Person with ID {} not found".format(id))                            

    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []
        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""

        person_data = Person.load_person_data()
        #print(suchstring)
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            print(eintrag)
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                print()

                return eintrag
        else:
            return {}

    @staticmethod
    def calc_age(date_of_birth):
            '''Alter berechnen mit dem Geburtsdatum als Eingabe'''
            today = datetime.date.today()
            age = today.year - date_of_birth
            return age

    @staticmethod
    def calc_max_hr(age : int) -> int:
        '''Max HR anhand des Alters berechnen'''    
        max_hr_bpm =  223 - 0.9 * age
        return int(max_hr_bpm)
    
    @staticmethod 
    def get_ekg_list(person_data): # Mögliche Funktion für die Anzeige aller EKGs evtl löschen
        """A Function that takes the persons-dictionary and returns a list of all person names"""
        list_of_ekgs = []
        for eintrag in person_data:
            ekg_tests = eintrag.get("ekg_tests", [])  # Get the list of ekg_tests or an empty list if it doesn't exist
            for ekg_test in ekg_tests:
                ekg_id = ekg_test.get("id")
                ekg_date = ekg_test.get("date")
                list_of_ekgs.append((ekg_id, ekg_date))
        return list_of_ekgs



#move to ekgdata.py? 
    @staticmethod
    def ekgs_of_person(ekg_table, person_id): 
        """A Function that takes the EKG-Table and an id, and returns the IDs of for that id"""
        list_of_ekg_ids = []
        for document in ekg_table:
            if document["person_id"] == person_id:
                list_of_ekg_ids.append(document.doc_id)
        if len(list_of_ekg_ids) == 0:
            return ["Keine EKGs vorhanden. Andere Person wählen!"]
        return list_of_ekg_ids


    def __init__(self, person_dict) -> None:
        self.year_of_birth = person_dict["year_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.age = self.calc_age(self.year_of_birth)
        self.max_hr_bpm = self.calc_max_hr(self.age)
        


if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    #print(person_names)
    #print(Person.find_person_data_by_name("Huber, Julian"))
    #print(Person.calc_age())
    #print(Person.calc_max_hr())
    #print(Person.load_by_id().age)
    #print(Person.load_by_id(2).max_hr_bpm)
    #print(Person.load_by_id(2).age)
    #print(Person.get_ekg_list(persons))
    #print(Person.ekgs_of_person(persons, 1))
    print(Person.ekgs_of_person(persons.table('ekg_tests'), 1))
    