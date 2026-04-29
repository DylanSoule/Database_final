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

def create_user(uname, max_grade, description=None):
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
    conn.commit()
    conn.close()
    return None



class db_mngr:
    def __init__(self,uid):
        self.uid = uid
        
    def pull_wishlist(self):
        """
        Returns a list of tuples: the wishlist for a specific user in form [(name,grade,description),...,(name,grade,description)]
        """
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        try:
            print(self.uid)
            c.execute("""SELECT r.name,r.grade,r.description FROM routes r
                    JOIN wishlists w ON w.route_id=r.id
                    WHERE w.user_id=%s""",(self.uid,))
            wishlist=c.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError
        conn.close()
        return wishlist
    

    def pull_ascents(self):
        """
        Returns a list of tuples: the wishlist for a specific user in form [(name,grade,description,user_rating),...,(name,grade,description,user_rating)]
        """
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        try:
            c.execute("""SELECT r.name,r.grade,r.description,a.user_rating FROM routes r
                    JOIN ascents a ON a.route_id=r.id
                    WHERE a.user_id=%s""",(self.uid,))
            ascents=c.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError
        conn.close()
        return ascents
    
    def search(self, table, search):
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        print(table)
        try:
            if table == "wishlists":
                c.execute("""SELECT l.name,r.name,r.grade,r.description FROM routes r
                        JOIN wishlists w ON w.route_id=r.id
                        JOIN locations l ON l.id=r.location_id
                        WHERE w.user_id=%s AND (l.name LIKE %s OR r.name LIKE %s)""",(self.uid,"%{}%".format(search),"%{}%".format(search),))
            elif table == "ascents":
                c.execute("""SELECT l.name,r.name,r.grade,r.description,a.user_rating FROM routes r
                        JOIN ascents a ON a.route_id=r.id
                        JOIN locations l ON l.id=r.location_id
                        WHERE a.user_id=%s AND (l.name LIKE %s OR r.name LIKE %s)""",(self.uid,"%{}%".format(search),"%{}%".format(search),))
            try:
                result = c.fetchall()
            except Exception as e:
                print(e)
                conn.close()
                return []
            conn.close()
            return(result)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError
    
    def delete_wl_data(self, area, climb):
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        try:
            c.execute("""SELECT r.id FROM wishlists w
                    JOIN routes r ON r.id=w.route_id
                    JOIN locations l ON l.id=r.location_id
                    WHERE w.user_id=%s AND r.name=%s AND l.name=%s""",(self.uid,climb,area,))
            cid = c.fetchone()[0]
            c.execute("DELETE FROM wishlists WHERE user_id=%s AND route_id=%s;",(self.uid,cid,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError
        
    def delete_asc_data(self, area, climb):
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        try:
            c.execute("""SELECT r.id FROM ascents a
                    JOIN routes r ON r.id=a.route_id
                    JOIN locations l ON l.id=r.location_id
                    WHERE a.user_id=%s AND r.name=%s AND l.name=%s""",(self.uid,climb,area,))
            cid = c.fetchone()[0]
            c.execute("DELETE FROM ascents WHERE user_id=%s AND route_id=%s;",(self.uid,cid,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError


if __name__=="__main__":
    test = db_mngr("3")
    print(test.search('ascents','G'))