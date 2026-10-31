
"""Recruitment Tracker application using an SQLite database."""

import csv
import sqlite3


DATABASE_CONNECTION = sqlite3.connect(":memory:")

DATABASE_CONNECTION.execute(
    """
    CREATE TABLE applicants (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        expected_salary INTEGER,
        status TEXT
    )
    """
)


def add_applicant(name, role, expected_salary, status="applied"):
    """Add a new applicant to the database."""
    DATABASE_CONNECTION.execute(
        """
        INSERT INTO applicants
        (name, role, expected_salary, status)
        VALUES (?, ?, ?, ?)
        """,
        (name, role, expected_salary, status),
    )
    DATABASE_CONNECTION.commit()


def shortlist(role, salary_limit):
    """Return applicants matching a role and salary limit."""
    rows = DATABASE_CONNECTION.execute(
        """
        SELECT name, expected_salary
        FROM applicants
        WHERE role = ?
        """,
        (role,),
    ).fetchall()

    return [
        name for name, salary in rows
        if salary <= salary_limit
    ]


def update_status(applicant_id, status):
    """Update the hiring status of an applicant."""
    DATABASE_CONNECTION.execute(
        "UPDATE applicants SET status = ? WHERE id = ?",
        (status, applicant_id),
    )
    DATABASE_CONNECTION.commit()


def export_report(path):
    """Export applicant names, roles and statuses to a CSV file."""
    rows = DATABASE_CONNECTION.execute(
        "SELECT name, role, status FROM applicants"
    )

    with open(path, "w", newline="", encoding="utf-8") as report_file:
        writer = csv.writer(report_file)
        writer.writerows(rows)


def count_by_status(status):
    """Return the number of applicants with a given status."""
    result = DATABASE_CONNECTION.execute(
        "SELECT COUNT(*) FROM applicants WHERE status = ?",
        (status,),
    ).fetchone()

    return result[0]


def main():
    """Run the Recruitment Tracker demonstration."""
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)

    update_status(1, "interview")

    print(shortlist("analyst", 650000))
    export_report("applicants_report.csv")
    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    main()
