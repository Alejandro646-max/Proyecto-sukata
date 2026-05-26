from app.core.database import db

class ProductService:
    
    def create(self, name, category, defect, status, notes, image_url):
        query = """
            INSERT INTO products (name, category, defect, status, notes, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (name, category, defect, status, notes, image_url)
        return db.execute_query(query, params)
    
    def get_all(self):
        rows = db.fetch_all("SELECT * FROM products ORDER BY created_at DESC")
        return rows
    
    def get_by_id(self, product_id):
        row = db.fetch_one("SELECT * FROM products WHERE id = %s", (product_id,))
        return row
    
    def update_status(self, product_id, status):
        query = "UPDATE products SET status = %s WHERE id = %s"
        return db.execute_query(query, (status, product_id))
    
    def delete(self, product_id):
        query = "DELETE FROM products WHERE id = %s"
        return db.execute_query(query, (product_id,))
    
    def get_statistics(self):
        total = db.fetch_one("SELECT COUNT(*) as total FROM products")['total']
        
        by_status = {}
        rows = db.fetch_all("SELECT status, COUNT(*) as count FROM products GROUP BY status")
        for row in rows:
            by_status[row['status']] = row['count']
        
        by_category = {}
        rows = db.fetch_all("SELECT category, COUNT(*) as count FROM products GROUP BY category")
        for row in rows:
            by_category[row['category']] = row['count']
        
        return {'total': total, 'by_status': by_status, 'by_category': by_category}