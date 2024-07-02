from tinydb import TinyDB, Query
from tinydb.table import Document

db = TinyDB("data/person_db.json")
person_table = db.table("persons")
ekg_table = db.table("ekg_tests")

person_table.insert_multiple([
    Document({
	        "year_of_birth": 1967,
	        "firstname": "Yannic",
	        "lastname": "Heyer",
            "picture_path" : "data/pictures/js.jpg"
        },
        doc_id=2
    ),
    Document({
	        "year_of_birth": 1973,
	        "firstname": "Yunus",
	        "lastname": "Schmirander",
            "picture_path" : "data/pictures/bl.jpg"
        },
        doc_id=3
    ),
    Document({
	        "year_of_birth": 2000,
	        "firstname": "Max",
	        "lastname": "Leer",
            "picture_path" : "data/pictures/empty.png"
        },
        doc_id=4
    ),
    Document({
	        "year_of_birth": 1989,
	        "firstname": "Julian",
	        "lastname": "Huber",
            "picture_path" : "data/pictures/tb.jpg"
        },
        doc_id=1)
])

ekg_table.insert_multiple([
    Document({
            "person_id": 3,
            "date": "2023-03-13",
            "result_link": "data/ekg_data/03_Ruhe.txt"
        },
        doc_id=3
    ),
    Document({
            "person_id": 1,
            "date": "2022-01-01",
            "result_link": "data/ekg_data/01_Ruhe.txt"
        },
        doc_id=1
    ),
    Document({		
            "person_id": 1,
		    "date": "2023-03-11",
		    "result_link": "data/ekg_data/04_Belastung.txt"
	    },
        doc_id=4
    ),
    Document({
            "person_id": 2,
            "date": "2023-03-12",
            "result_link": "data/ekg_data/02_Ruhe.txt"
        },
        doc_id=2
    ),
    Document({
            "person_id": None,
            "date": "2022-01-01",
            "result_link": "data/ekg_data/05_Belastung.txt"
        },
        doc_id=5
    ),
])

print(person_table.all())