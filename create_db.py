from tinydb import TinyDB, Query
from tinydb.table import Document
import json

db = TinyDB("data/person_db.json")
person_table = db.table("persons")
ekg_table = db.table("ekg_tests")

person_table.insert_multiple([
    Document({
        "id": 2,
	    "date_of_birth": 1967,
	    "firstname": "Yannic",
	    "lastname": "Heyer",
        "picture_path" : "data/pictures/js.jpg"
    }, doc_id=2),
    Document({
	    "id": 3,
	    "date_of_birth": 1973,
	    "firstname": "Yunus",
	    "lastname": "Schmirander",
        "picture_path" : "data/pictures/bl.jpg"
    }, doc_id=3),
    Document({
	    "id": 4,
	    "date_of_birth": 2000,
	    "firstname": "Max",
	    "lastname": "Leer",
        "picture_path" : "data/pictures/empty.png"
    }, doc_id=4),
    Document({
        "id": 1,
	    "date_of_birth": 1989,
	    "firstname": "Julian",
	    "lastname": "Huber",
        "picture_path" : "data/pictures/tb.jpg"
    },doc_id=1)
])

ekg_table.insert_multiple([
    Document({
        "id": 3,
        "person_id": 3,
        "date": "13.3.2023",
        "result_link": "data/ekg_data/03_Belastung.txt"
    },doc_id=3),
    Document({
        "id": 1,
        "person_id": 1,
        "date": "2022-01-01",
        "result_link": "data/ekg_data/01_ruhe.txt"
        },
        doc_id=1
    ),
    Document({		
        "id": 4,
        "person_id": 1,
		"date": "11.3.2023",
		"result_link": "data/ekg_data/04_Belastung.txt"
	},doc_id=4),
    Document({
        "id": 2,
        "person_id": 2,
        "date": "12.3.2023",
        "result_link": "data/ekg_data/02_Ruhe.txt"
    },doc_id=2)
])

print(person_table.all())