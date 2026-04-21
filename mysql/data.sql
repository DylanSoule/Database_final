INSERT INTO locations (name,description,climbing_type) VALUES
('Europe','Climbing in the continent of Europe',"bouldering,sport,top rope,ice,alpine,trad"),
('USA','Climbing in the country of USA',"bouldering,sport,top rope,ice,alpine,trad");

INSERT INTO locations (parent_id,name,description,climbing_type) VALUES
(2,'Colorado','Climbing in state of Colorado, one of the most developed states in the country',"bouldering,sport,top rope,ice,alpine,trad"),
(2,'Utah','Climbing in state of Utah, beautiful desert areas allow for pristine climbing',"bouldering,sport,top rope,trad"),
(1,'France','Climbing in the country of France, not very well built out at the moment, only have some climbs', "bouldering"),
(3,'Rocky Mountain National Park','Rocky mountain national park is some of the best quality rock in the nation, whether you want to boulder, trad climb, or big wall. *Make sure you have a reservation to get in during the summer months', "bouldering,trad,alpine"),
(6,'Chaos','Chaos has lots of amazing bouldering around lake Haiyaha', "bouldering"),
(6,'Longs Peak','The only 14er in Rocky Mountain National Park, the sheer face has multiple adventure routes', "trad,alpine"),
(4,"Joe's valley",'Amazing sandstone bouldering, and beautiful great quality rock. *Make sure to not climb rock when wet, as it will break', "bouldering"),
(5, 'Fontainebleau','Great french climbing',"bouldering");
