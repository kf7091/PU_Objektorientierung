import json
import datetime
import numpy as np


class Person:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data

    @staticmethod
    def load_by_id(id):
        """A Function that loads a person by id"""
        person_data = Person.load_person_data()
        for eintrag in person_data:
            if eintrag["id"] == id:
                return Person(eintrag)     
        raise ValueError("Person with {} not found".format(id))                             

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
    

    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.age = self.calc_age(self.date_of_birth)
        self.max_hr_bpm = self.calc_max_hr(self.age)


if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    #print(person_names)
    #print(Person.find_person_data_by_name("Huber, Julian"))
    #print(Person.calc_max_hr())
    #print(Person.estimate_max_hr(21))
    print(Person.load_by_id(5).age)