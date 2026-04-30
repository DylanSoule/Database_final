-- Use the database
USE climbing_app;

-- 1) List all locations and their parent
SELECT l.name AS location, p.name AS parent
FROM locations l
LEFT JOIN locations p ON l.parent_id = p.id
ORDER BY parent, location;

-- 2) List climbs in a specific location
SELECT r.name, r.grade, r.climbing_type
FROM routes r
JOIN locations l ON r.location_id = l.id
WHERE l.name = 'Chaos';

-- 3) Search climbs or areas by name
SELECT l.name AS area, r.name AS climb, r.grade
FROM routes r
JOIN locations l ON r.location_id = l.id
WHERE l.name LIKE '%Park%' OR r.name LIKE '%Peak%';

-- 4) Show a climb with average rating
SELECT r.name, AVG(a.user_rating) AS avg_rating
FROM routes r
LEFT JOIN ascents a ON a.route_id = r.id
WHERE r.name = 'Blood Money'
GROUP BY r.name;

-- 5) List all comments for a climb
SELECT u.user_name, c.comment
FROM comments c
JOIN users u ON c.user_id = u.id
JOIN routes r ON c.route_id = r.id
WHERE r.name = 'Blood Money';

-- 6) Add a new user
INSERT INTO users (user_name, max_grade, description)
VALUES ('New User', 'V5', 'Beginner climber');

-- 7) Add a new climb to a location
INSERT INTO routes (name, location_id, climbing_type, grade, description, first_ascent, rating)
SELECT 'New Route', l.id, 'sport', '5.10b', 'New sport route', NULL, 4.0
FROM locations l
WHERE l.name = 'North Table';

-- 8) Add a climb to a user wishlist
INSERT INTO wishlists (user_id, route_id)
SELECT u.id, r.id
FROM users u, routes r
WHERE u.user_name = 'Dylan Soule' AND r.name = 'Top notch';

-- 9) Log an ascent with a rating
INSERT INTO ascents (user_id, route_id, user_rating)
SELECT u.id, r.id, 4.5
FROM users u, routes r
WHERE u.user_name = 'Dylan Soule' AND r.name = 'Top notch';

-- 10) Update a route rating
UPDATE routes
SET rating = 4.7
WHERE name = 'Top notch';

-- 11) Delete a comment by user on a climb
DELETE c
FROM comments c
JOIN users u ON c.user_id = u.id
JOIN routes r ON c.route_id = r.id
WHERE u.user_name = 'Dylan Soule' AND r.name = 'Great white';

-- 12) Count climbs per location
SELECT l.name, COUNT(r.id) AS climb_count
FROM locations l
LEFT JOIN routes r ON r.location_id = l.id
GROUP BY l.name
ORDER BY climb_count DESC;