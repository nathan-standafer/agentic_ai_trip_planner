"""SQLite helpers for the manual_save_to_db package.

Creates a SQLite database named "VacationPlanner.db" by default and an
`activities` table capable of storing instances of the `Activity` model.

PYTHONPATH=src python -c "from manual_save_to_db.tools.db import retrieve_activities; import json; acts=retrieve_activities(); print(json.dumps([a.dict() for a in acts], indent=2))"
"""
from typing import Optional, List
import sqlite3
from .entities import Activity, ScheduledActivity

DB_FILENAME = "VacationPlanner.db"


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Return a sqlite3 connection to `db_path` or the default DB filename.

    The default file is `VacationPlanner.db` in the current working directory.
    """
    path = db_path or DB_FILENAME
    return sqlite3.connect(path)


def create_tables(db_path: Optional[str] = None) -> None:
    """Create the `activities` and `daily_schedule` tables if they do not exist."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            suggested_duration TEXT,
            location TEXT,
            sublocation TEXT,
            http_link TEXT,
            type TEXT,
            estimated_duration TEXT,
            cost TEXT,
            suitability TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            activity_name TEXT NOT NULL,
            activity_description TEXT,
            location TEXT,
            duration TEXT,
            transportation TEXT,
            notes TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def init_db(db_path: Optional[str] = None) -> None:
    """Initialize the database (create file and tables)."""
    create_tables(db_path)


def save_activity(activity: Activity, db_path: Optional[str] = None) -> int:
    """Save an `Activity` instance to the `activities` table.

    Returns the inserted row id.
    """
    # Ensure tables exist
    create_tables(db_path)

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO activities
            (name, 
            description, 
            suggested_duration, 
            location, 
            sublocation, 
            http_link, 
            type, 
            estimated_duration, 
            cost, 
            suitability)
        VALUES (
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?, 
            ?)
        """,
        (
            activity.name,
            activity.description,
            activity.suggested_duration,
            activity.location,
            activity.sublocation,
            activity.http_link,
            activity.type,
            activity.estimated_duration,
            activity.cost,
            activity.suitability,
        ),
    )
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid


def _show_tables(db_path: Optional[str] = None) -> list:
    """Return a list of table names in the database."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


def retrieve_activities(db_path: Optional[str] = None, location: Optional[str] = None) -> List[Activity]:
    """Return activities from the `activities` table as a list of `Activity` models.

    If location is provided, only returns activities matching that location (case-insensitive partial match).
    """
    # Ensure tables exist
    create_tables(db_path)

    conn = get_connection(db_path)
    cur = conn.cursor()

    if location:
        # Use LIKE for partial matching (e.g., "Tokyo" matches "Tokyo, Japan")
        cur.execute(
            """SELECT name, description, suggested_duration, location, sublocation, http_link,
                      type, estimated_duration, cost, suitability
               FROM activities
               WHERE location LIKE ? OR location LIKE ? OR location LIKE ?""",
            (f"%{location}%", f"%{location.lower()}%", f"%{location.upper()}%")
        )
    else:
        cur.execute(
            "SELECT name, description, suggested_duration, location, sublocation, http_link, type, estimated_duration, cost, suitability FROM activities"
        )
    rows = cur.fetchall()
    conn.close()

    activities: List[Activity] = []
    for row in rows:
        activities.append(
            Activity(
                name=row[0] or "",
                description=row[1] or "",
                suggested_duration=row[2] or "",
                location=row[3] or "",
                sublocation=row[4] or "",
                http_link=row[5] or "",
                type=row[6] if len(row) > 6 else None,
                estimated_duration=row[7] if len(row) > 7 else None,
                cost=row[8] if len(row) > 8 else None,
                suitability=row[9] if len(row) > 9 else None,
            )
        )

    return activities


def activity_exists(name: str, location: str, db_path: Optional[str] = None) -> bool:
    """Check if an activity with the given name and location already exists in the database.

    Uses case-insensitive matching for the name and partial matching for location.
    """
    # Ensure tables exist
    create_tables(db_path)

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        """SELECT COUNT(*) FROM activities
           WHERE LOWER(name) = LOWER(?)
           AND (location LIKE ? OR location LIKE ? OR location LIKE ?)""",
        (name, f"%{location}%", f"%{location.lower()}%", f"%{location.upper()}%")
    )
    count = cur.fetchone()[0]
    conn.close()

    return count > 0


def clear_schedule(db_path: Optional[str] = None) -> int:
    """Clear all scheduled activities from the daily_schedule table.

    Returns the number of rows deleted.
    """
    # Ensure tables exist
    create_tables(db_path)

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM daily_schedule")
    deleted_count = cur.rowcount
    conn.commit()
    conn.close()

    return deleted_count


def save_scheduled_activity(scheduled: ScheduledActivity, db_path: Optional[str] = None) -> int:
    """Save a `ScheduledActivity` instance to the `daily_schedule` table.

    Returns the inserted row id.
    """
    # Ensure tables exist
    create_tables(db_path)

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO daily_schedule
            (date, time_slot, activity_name, activity_description, location, duration, transportation, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            scheduled.date,
            scheduled.time_slot,
            scheduled.activity_name,
            scheduled.activity_description,
            scheduled.location,
            scheduled.duration,
            scheduled.transportation,
            scheduled.notes,
        ),
    )
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid


def retrieve_schedule(db_path: Optional[str] = None) -> List[ScheduledActivity]:
    """Return all scheduled activities from the `daily_schedule` table ordered by date and time."""
    # Ensure tables exist
    create_tables(db_path)

    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT date, time_slot, activity_name, activity_description, location, duration, transportation, notes FROM daily_schedule ORDER BY date, time_slot"
    )
    rows = cur.fetchall()
    conn.close()

    scheduled_activities: List[ScheduledActivity] = []
    for row in rows:
        scheduled_activities.append(
            ScheduledActivity(
                date=row[0] or "",
                time_slot=row[1] or "",
                activity_name=row[2] or "",
                activity_description=row[3] or "",
                location=row[4] or "",
                duration=row[5] or "",
                transportation=row[6],
                notes=row[7],
            )
        )

    return scheduled_activities


def _make_sample_activity(args) -> Activity:
    return Activity(
        name=args.name,
        description=args.description,
        suggested_duration=args.suggested_duration,
        location=args.location,
        sublocation=args.sublocation,
        http_link=args.http_link,
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manage the VacationPlanner SQLite database (create table, insert sample, show tables)"
    )
    parser.add_argument("--db-path", help="Path to SQLite DB file (defaults to VacationPlanner.db)")
    subparsers = parser.add_subparsers(dest="cmd")

    subparsers.add_parser("init", help="Create the database and tables")

    sp_save = subparsers.add_parser("save-sample", help="Save a sample Activity to the DB")
    sp_save.add_argument("--name", default="Sample Activity")
    sp_save.add_argument("--description", default="A sample activity created from the CLI")
    sp_save.add_argument("--suggested-duration", dest="suggested_duration", default="2 hours")
    sp_save.add_argument("--location", default="Unknown")
    sp_save.add_argument("--sublocation", default="")
    sp_save.add_argument("--http-link", dest="http_link", default="")

    subparsers.add_parser("show-tables", help="List tables in the SQLite database")

    args = parser.parse_args()
    db_path = args.db_path if getattr(args, "db_path", None) else None

    if args.cmd == "init":
        init_db(db_path)
        print("Initialized database and ensured tables exist.")
    elif args.cmd == "save-sample":
        act = _make_sample_activity(args)
        rowid = save_activity(act, db_path)
        print(f"Inserted sample Activity with row id {rowid}")
    elif args.cmd == "show-tables":
        tables = _show_tables(db_path)
        for t in tables:
            print(t)
    else:
        parser.print_help()
