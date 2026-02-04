# Sample code related to the library API for HR purposes

## Rationale

This is a sample project to provide example of how I am developing apps. This is very minimalistic example, for the purpose of evaluation of simple code creation. There is no doubts that the solution could be extended with more documentation and more complex data models, never as minimalistic one even that one table solution might fit clients needs. For further development there would be probably a need to split the table with books into three. One related to books itself, second related to customers, third to keep transactions and its history.

## Run instructions

After setting up environment use command: `docker compose up`

## How to run tests

Use command: `pytest test_app.py`

## Api documentation

Documentation is available at http://localhost:8000/docs

## Database schema

The database schema can be found in the file [schema.py](schema.py)

## License

[CC BY NC 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0)
