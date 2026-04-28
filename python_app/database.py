import mysql.connector


def create_connection():
        """Create database connection"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='climbing_app',
                user='app_user',
                password='1234'
            )
            if connection.is_connected():
                return connection
        except Exception as e:
            print(f"Error: {e}")
            return None

def validate_user(uname):
        """
        Validates if the user exists that the person is trying to login as
        Parameter: uname - the username
        Returns: the user id found for that username
        """
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()

        try:
            c.execute("SELECT (id) FROM users WHERE user_name=%s",(uname,))
            u_idl = c.fetchone()
            if u_idl:
                u_id = u_idl[0]
                conn.close()
                return u_id
            else:
                conn.close()
                return None
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError

def create_user(uname, max_grade, description):
    conn = create_connection()
    if not conn:
        return LookupError
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (user_name, max_grade, description) VALUES (%s,%s,%s)",(uname,max_grade,description))
    except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError



class db_mngr:
    def __init__(self,uid):
        self.uid = uid
        
    def pull_wishlist(self):
        """
        Returns a tuple of tuples: the wishlist for a specific user in form ((name,grade,description),...,(name,grade,description))
        """
        conn = self.create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        try:
            c.execute("""SELECT (r.name,r.grade,r.description) FROM routes r
                    JOIN wishlists w ON w.route_id=r.route_id
                    WHERE w.user_id=%s""",(self.uid))
            wishlist=c.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError
        conn.close()
        return wishlist
    
    def pull_ascents(self):
        """
        Returns a tuple of tuples: the wishlist for a specific user in form ((name,grade,description,user_rating),...,(name,grade,description,user_rating))
        """
        conn = self.create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        try:
            c.execute("""SELECT (r.name,r.grade,r.description,a.rating) FROM routes r
                    JOIN ascents a ON a.route_id=r.route_id
                    WHERE a.user_id=%s""",(self.uid))
            ascents=c.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError
        conn.close()
        return ascents