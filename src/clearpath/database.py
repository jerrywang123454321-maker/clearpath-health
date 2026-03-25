# ====================================================================
# database.py — Database Connection and Setup
#
# WHAT IS THIS FILE?
# This file handles everything related to CONNECTING to the database
# and SETTING IT UP for the first time. Think of it as the "key to
# the filing cabinet" — it opens the database so other parts of the
# code can read from and write to it.
#
# WHAT IS SQLite?
# SQLite is a lightweight database that stores everything in a single
# file on your computer (like clearpath.db). Unlike big databases
# like PostgreSQL or MySQL, you don't need to install or run a
# separate server. It "just works."
#
# For ClearPath Health's current scale (hundreds of payers, not
# millions of rows), SQLite is more than powerful enough. If the
# project grows huge, we can migrate to PostgreSQL later.
# ====================================================================

# ====================================================================
# IMPORTS
#
# sqlite3 — Built-in Python module for working with SQLite databases.
#           No need to install anything — it comes with Python.
#
# config  — Our own config.py file (from this same project).
#           We import the database path and schema path from there
#           so we don't have to hardcode file locations in this file.
#
# "from .config import ..." — the dot (.) before "config" means
# "look in the SAME FOLDER as this file." It's called a
# "relative import." Without the dot, Python would look for a
# config module installed globally, which isn't what we want.
# ====================================================================
import sqlite3

from .config import DATABASE_PATH, SCHEMA_PATH


def get_connection():
    """
    Open a connection to the database and return it.

    WHAT IS A "CONNECTION"?
    A connection is like picking up the phone to call the database.
    You need an open connection to send commands (queries) to the
    database. When you're done, you should close the connection
    (hang up the phone).

    WHAT IS "def"?
    "def" defines a FUNCTION — a reusable block of code with a name.
    Instead of writing the same 5 lines every time you want to
    connect to the database, you write them once inside a function,
    and then just call the function by name: get_connection()

    WHAT IS "return"?
    "return" sends a value BACK to whoever called the function.
    When some other code calls get_connection(), it gets back
    a connection object that it can use to talk to the database.
    """

    # sqlite3.connect() opens (or creates) a database file.
    # str(DATABASE_PATH) converts our Path object to a plain string
    # because sqlite3 expects a string, not a Path object.
    connection = sqlite3.connect(str(DATABASE_PATH))

    # By default, SQLite returns data as plain tuples (ordered lists).
    # This line tells it to return data as Row objects instead, which
    # let you access columns by NAME (like row["name"]) instead of
    # by position number (like row[0]). Much more readable.
    connection.row_factory = sqlite3.Row

    # Turn on "foreign key enforcement."
    # Remember in schema.sql where we said a metrics_report must
    # reference a real payer_id? SQLite doesn't enforce that by
    # default (weird, right?). This line turns on that enforcement.
    # "PRAGMA" is a SQLite-specific command for changing settings.
    connection.execute("PRAGMA foreign_keys = ON")

    # Send the connection back to whoever asked for it.
    return connection


def initialize_database():
    """
    Create all the database tables from our schema.sql file.

    This function reads the SQL commands from db/schema.sql and
    runs them against the database. It's safe to run multiple times
    because the schema uses "CREATE TABLE IF NOT EXISTS" — if the
    tables already exist, it just skips them.

    You typically only need to run this ONCE when setting up the
    project for the first time. After that, the tables exist and
    you just add data to them.
    """

    # --- Step 1: Read the schema file ---
    # open() opens a file for reading. The "r" means "read mode"
    # (as opposed to "w" for write). "encoding='utf-8'" tells Python
    # how to interpret the characters in the file (utf-8 is the
    # universal standard that handles all languages and symbols).
    #
    # "with" is a special Python keyword that automatically CLOSES
    # the file when you're done, even if an error happens. Without
    # "with", you'd have to remember to call f.close() yourself.
    # Always use "with" when opening files.
    #
    # "as f" gives the opened file a short name "f" that we use
    # inside the indented block below.
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        # f.read() reads the ENTIRE file contents as one big string.
        schema_sql = f.read()

    # --- Step 2: Connect to the database and run the schema ---
    # We use "with" here too — it ensures the connection is properly
    # closed when we're done, and it automatically SAVES (commits)
    # our changes if everything succeeds.
    with get_connection() as connection:
        # executescript() runs multiple SQL commands at once.
        # Our schema.sql has multiple CREATE TABLE commands separated
        # by semicolons, so we need executescript (not execute).
        connection.executescript(schema_sql)

    # If we get here without an error, the database was created
    # successfully! (Python functions return None by default if
    # there's no explicit return statement — that's fine here
    # because we don't need to send anything back.)
