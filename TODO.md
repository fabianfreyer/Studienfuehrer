# Things to do

## Authentification

### Implement roles and permissions
We basically need at least the following roles with their associated permissions:

* Superuser (already implemented)
  - can do anything

* Editor
  - can add / edit fields on their associated uni / subject
  - can add fields

### Add a registration form
Why have user accounts?
* Save queries

### Token login
For editors to be sent out by email

## Implement query factory
Implement some query factory to filter by fields. Some useful links may be:

* [SQLAlchemy - Building Query-Enabled Properties](http://docs.sqlalchemy.org/en/rel_1_0/orm/join_conditions.html#building-query-enabled-properties)

## Implement views
* Container comparison
* Filter query view
* Better field add view (directly on detail view)
* Better schema add view (directly on schema admin view)

## Pre-Seed database
* Use YAML for schema?

## Fix Bugs
* Check for item existance everywhere where an ID is given via GET parameter
