CREATE TABLE `locations` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `parent_id` INT,
  `name` VARCHAR(200) NOT NULL,
  `description` TEXT,
  `climbing_type` SET('bouldering', 'sport', 'top rope', 'ice', 'alpine', 'trad') NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`parent_id`)
      REFERENCES `location`(`id`)
);

CREATE TABLE `routes` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `location_id` INT NOT NULL,
  `type` ENUM('bouldering', 'sport', 'top rope', 'ice', 'alpine', 'trad') NOT NULL,
  `grade` VARCHAR(5) NOT NULL,
  `description` TEXT,
  `first_ascent_uid` TEXT,
  `rating` FLOAT,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`location_id`)
      REFERENCES `location`(`id`)
);

CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `user_name` VARCHAR(50) NOT NULL,
  `max_grade` VARCHAR(5),
  `description` TEXT,
  PRIMARY KEY (`id`)   
);

CREATE TABLE `ascents` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `route_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `user_rating` FLOAT,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`route_id`)
       REFERENCES `route` (`id`)
       ON DELETE CASCADE,
  FOREIGN KEY (`user_id`)
        REFERENCES `user` (`id`)
        ON DELETE CASCADE
);

CREATE TABLE `comments` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `route_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `comment` TEXT,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`route_id`)
       REFERENCES `route` (`id`)
       ON DELETE CASCADE,
  FOREIGN KEY (`user_id`)
        REFERENCES `user` (`id`)
        ON DELETE CASCADE
);

CREATE TABLE `wishlists` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `route_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`route_id`)
       REFERENCES `route` (`id`)
       ON DELETE CASCADE,
  FOREIGN KEY (`user_id`)
        REFERENCES `user` (`id`)
        ON DELETE CASCADE
);