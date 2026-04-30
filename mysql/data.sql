USE DATABASE climbing_app;

INSERT INTO locations (name,description,climbing_type) VALUES
("The Whole World","You live here","bouldering,sport,top rope,ice,alpine,trad");

INSERT INTO locations (parent_id,name,description,climbing_type) VALUES
(1,'Europe','Climbing in the continent of Europe',"bouldering,sport,top rope,ice,alpine,trad"),
(1,'USA','Climbing in the country of USA',"bouldering,sport,top rope,ice,alpine,trad"),
(3,'Colorado','Climbing in state of Colorado, one of the most developed states in the country',"bouldering,sport,top rope,ice,alpine,trad"),
(3,'Utah','Climbing in state of Utah, beautiful desert areas allow for pristine climbing',"bouldering,sport,top rope,trad"),
(2,'France','Climbing in the country of France, not very well built out at the moment, only have some climbs', "bouldering"),
(4,'Rocky Mountain National Park','Rocky mountain national park is some of the best quality rock in the nation, whether you want to boulder, trad climb, or big wall. *Make sure you have a reservation to get in during the summer months', "bouldering,trad,alpine"),
(7,'Chaos','Chaos has lots of amazing bouldering around lake Haiyaha', "bouldering"),
(7,'Longs Peak','The only 14er in Rocky Mountain National Park, the sheer face has multiple adventure routes', "trad,alpine"),
(5,"Joe's valley",'Amazing sandstone bouldering, and beautiful great quality rock. *Make sure to not climb rock when wet, as it will break', "bouldering"),
(6,'Fontainebleau','Great french climbing',"bouldering"),
(9,'The diamond','Huge face on the front of longs peak','trad,alpine'),
(4,'North Table','Climbing at North table Mountain by Golden','sport');

INSERT INTO users (user_name,max_grade,description) VALUES
('Daniel Woods', 'V17', 'rage & tranquility, Pro climber for @thenorthface @evolv_worldwide @organicclimbing @frictionlabs @physivantage'),
('Lynn Hill', '5.14', 'FFA of the nose of el capitan'),
('Dylan Soule', 'V12', 'Idk climbing stuff'),
('Owen Townsend', 'V3', 'Amalgamation of Warren Tech classmates'),
('Max Shay', 'V13', 'Local strong dude, coaches'),
('Noah Wheeler','V17', 'Colorado climber'),
('Saige Shulda', 'V9', 'Pretty cool person'),
('Alex Puccio', NULL, 'World cup climber and great outdoor climber'),
('Jaqueline John', 'V8', "Local gym gumby that's really annoying"),
('Rumbert Stiltson', '5.12b', 'Outdoor trad dad');

INSERT INTO routes (name, location_id, climbing_type, grade, description, first_ascent, rating) VALUES
("Blood Money",8,'bouldering', 'V12', "Large squeezy shouldery heel hooky",'Daniel Woods',3.9),
("Top notch",8,'bouldering','V13',"Big moves on crimps",'Daniel Woods',3.0),
("Great white",10,'bouldering','V6',"Really cool arete boulder, looks like a great white fin",NULL,4.2),
("Ariana",12,'alpine','5.12a',"6 pitch ascent",NULL,4.0),
("La Marie-Rose",11,'bouldering','6a','Probably the most famous font boulder. Crux involves a long reach to a small hold before topping out.','Rene Ferlet',4.5),
("Rainbow Rocket",11,'bouldering','8a','Big jump step up bloc',NULL,3.5),
("Culp-Bossier",7,'trad','5.8','8 pitch climb up hallet peak from emerald lake side',NULL,4.0),
("Freshly Squeezed",8,'bouldering','V12','Start low on areta and small left crimp and climb out on incuts.','Dave Graham',4.3),
("Makaila",9,"bouldering",'V7',"Hard move to a crimp followed by easier climbing of the clear rails.",NULL,3.1),
("Tubesnake boogie",10,'bouldering','V9',"One of the most fun in the area, maneuver around the 'Tubesnake' formation followed by a long topout",NULL, 4.7),
("Bullet The Brown Cloud",13,'sport','5.11c','Start with a funky move and work the face',NULL,3.0);

INSERT INTO ascents (user_id,route_id,user_rating) VALUES
(1,1,3.5),
(1,2,4.0),
(1,8,NULL),
(2,4,3.5),
(3,9,3.0),
(3,3,4.0),
(5,3,3.5),
(6,1,3.5),
(7,11,NULL),
(10,11,4.3),
(9,5,4.8),
(8,1,3.2);

INSERT INTO comments (user_id,route_id,comment) VALUES
(1,1,'Cool'),
(2,4,'Amazingly pretty and what a good day to do this mega route'),
(3,3,'Really pretty rock and fun moves'),
(6,8,"Didn't do it in the little time I had, fun boulder though"),
(7,9,"This one is on the list, its gonna happen"),
(5,1,"Did the stand start, have to come back for the sit sometime"),
(1,2,"One of the best"),
(9,5,"Wi Wi Baguete"),
(4,10,"Looked really amazing, top out sounds freaky unfortunately"),
(10,11,"Took the kids to this one and they loved it");

INSERT INTO wishlists(user_id,route_id) VALUES
(3,1),
(3,2),
(5,1),
(5,2),
(5,8),
(7,9),
(4,4),
(10,7),
(10,4),
(2,2),
(9,3);