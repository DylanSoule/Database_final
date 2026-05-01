import mysql.connector


def create_connection():
        """Create and return a MySQL connection, or None on failure."""
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
        Validate that a username exists.
        
        Args:
            uname: Username to look up.
        Returns:
            User id if found, None if not found, or LookupError on failure.
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
    """
    Create a user record.
    
    Args:
        uname: Username.
        max_grade: Max grade string.
        description: Optional user description.
    """
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
    """Database manager for a specific user id."""
    def __init__(self,uid):
        """Initialize manager with a user id."""
        self.uid = uid
        
    def pull_wishlist(self):
        """
        Fetch wishlist climbs for this user.
        
        Returns:
            List of tuples: [(name, grade, description), ...]
        """
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        try:
            # Join wishlist to routes
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
        Fetch ascents for this user.
        
        Returns:
            List of tuples: [(name, grade, description, user_rating), ...]
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
        """
        Search routes and locations within a user's wishlist or ascents.
        
        Args:
            table: "wishlists" or "ascents".
            search: Search string.
        """
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
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
            # Fetch results for the last executed SELECT
            result = c.fetchall()
            conn.close()
            return(result)
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError
    
    def delete_wl_data(self, area, climb):
        """Delete a wishlist entry for a given area and climb."""
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()
        try:
            area = area.strip()
            climb = climb.strip()
            c.execute("""DELETE w FROM wishlists w
                    JOIN routes r ON r.id=w.route_id
                    JOIN locations l ON l.id=r.location_id
                    WHERE w.user_id=%s AND r.name=%s AND l.name=%s""",
                    (self.uid, climb, area))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")
            conn.close()
            return LookupError
        
    def delete_asc_data(self, area, climb):
        """
        Delete an ascent entry for a given area and climb.
        
        Args:
            area: Location name.
            climb: Route name.
        """
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
        """
        Resolve the parent location name for a given child location.
        
        Args:
            child_name: Location name.
        Returns:
            Parent location name or "The Whole World" if at the root.
        """
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
        List sub-locations and climbs under a location, or search results.
        
        Args:
            parent_name: Parent location name.
            search: Optional search string.
        Returns:
            (location_data, locations, climbs)
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
                # Fetch location header
                c.execute("SELECT name,description FROM locations WHERE name=%s",(parent_name,))
                location_data = c.fetchone()
                # Fetch sub-locations
                c.execute("""SELECT l.name, l.climbing_type FROM locations l
                        JOIN locations p ON l.parent_id=p.id
                        WHERE p.name=%s""",(parent_name,))
                locations = c.fetchall()
                # Fetch climbs in the location
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
        """
        Get or mutate climb-related data based on an action code.
        
        Actions:
            0: Fetch climb details
            1: Fetch comments
            2: Add to wishlist
            3: Add ascent
            4: Fetch ascents
            5: Add comment
        """
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
        
    def create_location(self,name,description,c_type,parent_name):
        """
        Insert a new location under a parent location.
        
        Args:
            name: Location name.
            description: Optional description.
            c_type: SET string for climbing types.
            parent_name: Parent location name.
        """
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()

        c.execute("SELECT id FROM locations WHERE name=%s",(parent_name,))
        pid=c.fetchone()[0]

        c.execute("""INSERT INTO locations (parent_id,name,description,climbing_type) VALUES (%s,%s,%s,%s)""",(pid,name,description,c_type))
        conn.commit()
        conn.close()
        return None
    
    def create_climb(self,name,description,c_type,parent_name,grade,fa,rating):
        """
        Insert a new climb under a location.
        
        Args:
            name: Climb name.
            description: Optional description.
            c_type: Climb type.
            parent_name: Location name.
            grade: Grade string.
            fa: First ascent string.
            rating: Optional float rating.
        """
        conn = create_connection()
        if not conn:
            return LookupError
        c = conn.cursor()

        c.execute("SELECT id FROM locations WHERE name=%s",(parent_name,))
        pid=c.fetchone()[0]

        c.execute("""INSERT INTO routes (name,location_id,climbing_type,grade,description,first_ascent,rating) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(name,pid,c_type,grade,description,fa,rating))
        conn.commit()
        conn.close()
        return None




if __name__=="__main__":
    test = db_mngr("3")
    print(test.get_parent_name('Europe'))