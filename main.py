from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import OperationalError, ProgrammingError

app = FastAPI()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="My_password1"
        )
        return conn
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/categories")
def get_categories():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT "Name" FROM "Production"."ProductCategory";')
            categories = cur.fetchall()

            if not categories:
                raise HTTPException(status_code=404, detail="Nenhuma categoria encontrada.")

            return [{"category_name": category[0]} for category in categories]
    finally:
        conn.close()        

from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import OperationalError, ProgrammingError


@app.get("/sales/top-products/category/{category}")
def get_top_products_by_category(category: str):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p."Name", SUM(sod."OrderQty") as total_quantity
                FROM "Sales"."SalesOrderDetail" sod
                JOIN "Production"."Product" p ON sod."ProductID" = p."ProductID"
                JOIN "Production"."ProductCategory" pc ON p."ProductCategoryID" = pc."ProductCategoryID"
                WHERE pc."Name" = %s
                GROUP BY p."Name"
                ORDER BY total_quantity DESC
                LIMIT 10;
            """, (category,))
            results = cur.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="Categoria não encontrada ou sem vendas registradas.")

            return [{"product_name": row[0], "total_quantity": row[1]} for row in results]
    except ProgrammingError as e:
        raise HTTPException(status_code=500, detail=f"SQL error: {str(e)}")
    finally:
        if conn:
            conn.close()



def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="My_password1"
        )
        return conn
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@app.get("/sales/best-customer")
def get_best_customer():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c."CustomerID", c."CompanyName", COUNT(o."OrderID") AS total_orders
                FROM "Sales"."SalesOrderHeader" o
                JOIN "Sales"."Customer" c ON o."CustomerID" = c."CustomerID"
                GROUP BY c."CustomerID", c."CompanyName"
                ORDER BY total_orders DESC
                LIMIT 1;
            """)
            result = cur.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")

            customer = {
                "customer_id": result[0],
                "company_name": result[1],
                "total_orders": result[2]
            }
            return customer
    except ProgrammingError as e:
        raise HTTPException(status_code=500, detail=f"SQL error: {str(e)}")
    finally:
        if conn:
            conn.close()


@app.get("/sales/top-sellers")
def get_top_sellers():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                WITH average_sales AS (
                    SELECT AVG(s."salesytd") AS avg_sales
                    FROM "Sales"."SalesPerson" s
                    WHERE EXTRACT(YEAR FROM s."modifieddate") = EXTRACT(YEAR FROM CURRENT_DATE) - 1
                )
                SELECT s."businessentityid", s."salesytd", s."saleslastyear"
                FROM "Sales"."SalesPerson" s
                JOIN average_sales a ON s."salesytd" > a.avg_sales
                WHERE EXTRACT(YEAR FROM s."modifieddate") = EXTRACT(YEAR FROM CURRENT_DATE) - 1
                ORDER BY s."salesytd" DESC;
            """)
            results = cur.fetchall()

            if not results:
                raise HTTPException(status_code=404, detail="Nenhum vendedor com vendas acima da média encontrado.")

            sellers = [
                {
                    "business_entity_id": row[0],
                    "sales_ytd": row[1],
                    "sales_last_year": row[2]
                }
                for row in results
            ]
            return sellers
    except ProgrammingError as e:
        raise HTTPException(status_code=500, detail=f"SQL error: {str(e)}")
    finally:
        if conn:
            conn.close()


@app.get("/sales/busiest-month")
def get_busiest_month():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT TO_CHAR(o."OrderDate", 'YYYY-MM') AS month, SUM(o."TotalDue") AS total_sales
                FROM "Sales"."SalesOrderHeader" o
                GROUP BY TO_CHAR(o."OrderDate", 'YYYY-MM')
                ORDER BY total_sales DESC
                LIMIT 1;
            """)
            result = cur.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Nenhum dado de vendas encontrado.")

            month, total_sales = result
            return {
                "month": month,
                "total_sales": total_sales
            }
    except ProgrammingError as e:
        raise HTTPException(status_code=500, detail=f"SQL error: {str(e)}")
    finally:
        if conn:
            conn.close()            
