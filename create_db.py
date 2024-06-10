from tinydb import TinyDB, Query
import json

db = TinyDB("data/person_db.json")
person_table = db.table("persons")
ekg_table = db.table("ekg_tests")

person_table.insert_multiple([
    {
        "id": 2,
	    "date_of_birth": 1967,
	    "firstname": "Yannic",
	    "lastname": "Heyer",
        "picture_path" : "data/pictures/js.jpg"
    }, {
	    "id": 3,
	    "date_of_birth": 1973,
	    "firstname": "Yunus",
	    "lastname": "Schmirander",
        "picture_path" : "data/pictures/bl.jpg"
    },	{
	    "id": 4,
	    "date_of_birth": 2000,
	    "firstname": "Max",
	    "lastname": "Leer",
        "picture_path" : "data/pictures/empty.png"
    }, {
        "id": 1,
	    "date_of_birth": 1989,
	    "firstname": "Julian",
	    "lastname": "Huber",
        "picture_path" : "data/pictures/tb.jpg"
    }
])

ekg_table.insert_multiple([
    {
        "id": 3,
        "person_id": 3,
        "date": "13.3.2023",
        "result_link": "data/ekg_data/03_Belastung.txt"
    }, {
        "id": 1,
        "person_id": 1,
        "date": "2022-01-01",
        "result_link": "data/ekg_data/01_ruhe.txt"
    }, {		
        "id": 4,
        "person_id": 1,
		"date": "11.3.2023",
		"result_link": "data/ekg_data/04_Belastung.txt"
	}, {
        "id": 2,
        "person_id": 2,
        "date": "12.3.2023",
        "result_link": "data/ekg_data/02_Ruhe.txt"
    }
])

print(person_table.all())