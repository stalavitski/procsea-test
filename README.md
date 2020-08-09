Test
====

Introduction
------------


This is a backend test, the choice of the Python framework is up to you (it can 
be django, flask, aiohttp, fastapi, sqlachemy, ...).

The aim of this test is to assert your development skills, so try to make it as 
professional as possible (tests, comments when you feel it's required,
ready to run in prodution, 12factor, linters, ready to be picked up by one of your colleagues, ...).

We know that you may not have as much time as required to do everything, in this case,
focus on the quality and don't try to do everything.

At the end, fill a README with:

- The time spent
- What you didn't have time to do
- What is buggy
- What could be improved with more time
- ...

If any question, feel free to ask us :)

The time spent
----------
Approx 4 hours

What you didn't have time to do
----------
I finished all 6 tasks

What is buggy
----------
- External API won't return data for ["MIDI-PYRENEES"](https://nominatim.openstreetmap.org/search?country=France&state=MIDI-PYRENEES&format=json) so it has nulls in the lat, lon columns

What could be improved with more time
----------
- Analyze CSV data better to set proper validations
- Discuss postal code field. It may be split in the separate table 
- Cache for totalArea and totalPopulation. Their calculation is very resourceful 
- Cache for lat, lon fields. External API calls are not fast
- Proper error handling for parser 
- Possibility to set CSV name as param for command
- Tests (proper mocking etc)

Info
----------
- Use `./manage.py importregions` to run CSV parser. It will parse CSV file in the project root with the name `correspondance-code-insee-code-postal.csv`;
- Api endpoint `/api/regions/`. List of region is under `results` list.

What to do
----------

1. The project should be versionned with git

2. Create a database with this data model:

        +--------+       +--------+       +-------------+
        | Region |-1---*-| County |-1---*-| City        |
        +--------+       +--------+       +-------------+
        | code   |       | code   |       | code_insee  |
        | name   |       | name   |       | code_postal |
        +--------+       +--------+       | name        |
                                          | population  |
                                          | area        |
                                          +-------------+

    From the CSV available here:

    [INSEE & postal codes](./correspondance-code-insee-code-postal.csv)

    Region model:
    - code: "Code Région" column in the CSV
    - name: "Région" column in the CSV

    County model:
    - code: "Code Département" column in the CSV
    - name: "Département" column in the CSV

    City model:
    - code_insee: "Code INSEE" columun in the CSV
    - code_postal: "Code Postal" column in the CSV
    - name: "Commune" column in the CSV
    - population: "Population" column in the CSV
    - area: "Superficie" column in the CSV

3. Create a script to import the CSV

4. Create an API endpoint which returns a list of the region containing the
   name of the region and its code:

        GET /api/regions/

        [
            {
            	"code": 11,
            	"name": "ILE-DE-FRANCE"
            },
		    ...
        ]

   optional: Paginate the answer to have 10 items per page

5. Improve this endpoint and add the `totalPopulation` and the `totalArea` which
   are the sum of the fields `population` and `area` in the City model (the data
   model should not be changed):

        GET /api/regions/

        [
            {
            	"code": 11,
            	"name": "ILE-DE-FRANCE",
            	"totalPopulation": 99999,
                "totalArea": 99999
            },
		    ...
        ]

6. Improve this endpoint by adding the coordinates of the regions by calling the nominatim API:
   https://nominatim.org/release-docs/develop/api/Search/

   Call exemple: https://nominatim.openstreetmap.org/search?country=France&state=Bretagne&format=json

        GET /api/regions/

        [
            {
            	"code": 11,
            	"name": "ILE-DE-FRANCE",
            	"lat": "48.6443057",
                "lon": "2.7537863"
            },
		    ...
        ]

