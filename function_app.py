import azure.functions as func
import logging
import psycopg2
import os
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="reports_portal_backend")
def reports_portal_backend(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        conn = psycopg2.connect(
            host=os.getenv("PGHOST"),
            database=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            port="5432"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mg_austinflat.los_revenue_expenses_data LIMIT 10")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        keys = ['well_name', 'metric', 'metric_value', 'metric_month', 'row_insert_date', 'row_insert_timestamp']
        json_result = [dict(zip(keys, r)) for r in rows]

        return func.HttpResponse(
            json.dumps(json_result, default=str),  # convert datetime to string
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*"
            }
        )

    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)