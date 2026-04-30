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

    def get_parent_name(self,child_name):
        if child_name=="The Whole World":
            return "The Whole World"

        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()

        c.execute("SELECT parent_id FROM locations WHERE name=%s",(child_name,))
        pid = c.fetchone()[0]
        c.execute("SELECT name FROM locations WHERE id=%s",(pid,))
        parent_name=c.fetchone()[0]
        conn.close()
        return parent_name

    def list_locations(self,parent_name,search=""):
        """
        
        """
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        
        if search=="":
            if parent_name=="":
                c.execute("SELECT name, climbing_type FROM locations WHERE parent_id IS NULL;")
                locations = c.fetchall()
                conn.close()
                return ("The whole world","You live here"),locations,[]
            else:
                c.execute("SELECT name,description FROM locations WHERE name=%s",(parent_name,))
                location_data = c.fetchone()
                c.execute("""SELECT l.name, l.climbing_type FROM locations l
                        JOIN locations p ON l.parent_id=p.id
                        WHERE p.name=%s""",(parent_name,))
                locations = c.fetchall()
                c.execute("""SELECT r.name,r.grade,r.climbing_type FROM routes r
                        JOIN locations l ON l.id=r.location_id
                        WHERE l.name=%s""",(parent_name,))
                climbs = c.fetchall()
                conn.close()
                return location_data,locations,climbs
        else:
            c.execute("SELECT name,climbing_type FROM locations WHERE name LIKE %s",("%{}%".format(search),))
            locations = c.fetchall()
            c.execute("SELECT name,grade,climbing_type FROM routes WHERE name LIKE %s",("%{}%".format(search),))
            climbs = c.fetchall()
            conn.close()
            return ("Search Results","Listed Below are your search results"),locations,climbs

    def climb_info(self,action,climb_name,uinput=None):
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        if action==0:
            c.execute("""SELECT name,grade,climbing_type,description FROM routes WHERE name=%s""",(climb_name,))
            info = c.fetchone()
            conn.close()
            return info
        elif action==1:
            c.execute("SELECT id FROM routes WHERE name=%s",(climb_name,))
            cid=c.fetchone()[0]
            c.execute("""SELECT u.user_name,c.comment FROM comments c
                      JOIN users u ON c.user_id=u.id
                      WHERE c.route_id=%s""",(cid,))
            comments = c.fetchall()
            conn.close()
            return comments
        elif action==2:
            c.execute("SELECT id FROM routes WHERE name=%s",(climb_name,))
            cid=c.fetchone()[0]
            c.execute("INSERT INTO wishlists (user_id,route_id) VALUES (%s,%s)",(self.uid,cid,))
            conn.commit()
            conn.close()
            return None
        elif action==3:
            c.execute("SELECT id FROM routes WHERE name=%s",(climb_name,))
            cid=c.fetchone()[0]
            c.execute("INSERT INTO ascents (user_id,route_id,user_rating) VALUES (%s,%s,%s)",(self.uid,cid,uinput,))
            conn.commit()
            conn.close()
            return None
        elif action==4:
            c.execute("SELECT id FROM routes WHERE name=%s",(climb_name,))
            cid=c.fetchone()[0]
            c.execute("""SELECT u.user_name,a.user_rating FROM ascents a
                      JOIN users u ON a.user_id=u.id
                      WHERE a.route_id=%s""",(cid,))
            ascents = c.fetchall()
            conn.close()
            return ascents
        elif action==5:
            c.execute("SELECT id FROM routes WHERE name=%s",(climb_name,))
            cid=c.fetchone()[0]
            c.execute("INSERT INTO comments (user_id,route_id,comment) VALUES (%s,%s,%s)",(self.uid,cid,uinput,))
            conn.commit()
            conn.close()
            return None




if __name__=="__main__":
    test = db_mngr("3")
    print(test.get_parent_name('Europe'))