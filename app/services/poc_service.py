import sqlite3
from typing import Optional
import requests
from fastapi import HTTPException
# todo: improve this
from dto.pocs.alerts_dto import PocDTO


class PocService:
    BASE_URL = "https://poc-in-github.motikan2010.net/api/v1/"
    DB_FILE = "alerts.db"

    @staticmethod
    def ensure_table_exists():
        """
        Check if the `pocs` table exists and create it if it doesn't.
        """
        conn = sqlite3.connect(PocService.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pocs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cve_id TEXT,
                name TEXT,
                owner TEXT,
                full_name TEXT,
                html_url TEXT,
                description TEXT,
                stargazers_count INTEGER,
                nvd_description TEXT,
                created_at TEXT,
                updated_at TEXT,
                pushed_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def get_pocs(limit: int = 50, cve_id: Optional[str] = None):
        """
        Fetch POCs from the database or fetch from an external API if not present.
        Ensures the `pocs` table exists before proceeding.
        """
        # Ensure the table exists
        PocService.ensure_table_exists()

        # Connect to the SQLite database
        conn = sqlite3.connect(PocService.DB_FILE)
        cursor = conn.cursor()

        # Build the SQL query
        query = "SELECT * FROM pocs"
        params = []
        if cve_id:
            query += " WHERE cve_id = ?"
            params.append(cve_id)
        query += " LIMIT ?"
        params.append(limit)

        # Ensure params are passed as a tuple
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            # If no rows are found, fetch from external API
            external_params = {"limit": limit}
            if cve_id:
                external_params["cve_id"] = cve_id

            response = requests.get(PocService.BASE_URL, params=external_params)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch POCs")

            pocs_data = response.json().get("pocs", [])

            # Insert new data into the database
            for poc_data in pocs_data:
                cursor.execute("""
                    INSERT INTO pocs (
                        cve_id, name, owner, full_name, html_url, description, 
                        stargazers_count, nvd_description, created_at, updated_at, pushed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(poc_data.get("cve_id", "")),
                    str(poc_data.get("name", "")),
                    str(poc_data.get("owner", "")),
                    str(poc_data.get("full_name", "")),
                    str(poc_data.get("html_url", "")),
                    poc_data.get("description", None),
                    int(poc_data.get("stargazers_count", 0)),
                    poc_data.get("nvd_description", None),
                    poc_data.get("created_at", None),
                    poc_data.get("updated_at", None),
                    poc_data.get("pushed_at", None),
                ))
            conn.commit()

            # Re-run the query to fetch the newly added rows
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

        conn.close()

        # Convert rows to DTOs
        return [PocDTO.from_sqlite_row(row) for row in rows]

