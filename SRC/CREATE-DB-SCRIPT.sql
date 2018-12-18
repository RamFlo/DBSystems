CREATE TABLE Categories (
	category_id smallint unsigned,
	category_name varchar(255) NOT NULL,
	PRIMARY KEY (category_id),
	UNIQUE (category_name)
);

CREATE TABLE Cuisines (
	cuisine_id smallint unsigned,
	cuisine_name varchar(255) NOT NULL,
	PRIMARY KEY (cuisine_id),
	UNIQUE (cuisine_name)
);

CREATE TABLE Restaurants (
	restaurant_id int unsigned,
	restaurant_name varchar(255) NOT NULL,
	lat DECIMAL(10, 8) NOT NULL,
	lng DECIMAL(10, 8) NOT NULL,
	price_category tinyint CHECK (price_category >= 1 AND price_category <=4),
	agg_review float CHECK (agg_review >= 0.0 AND agg_review <= 5.0),
	has_online_delivery bit,
	featured_photo_url nvarchar(2083),
	PRIMARY KEY (restaurant_id)
);

CREATE TABLE RestaurantsCuisines (
	restaurant_id int unsigned,
	cuisine_id smallint unsigned,
	PRIMARY KEY (restaurant_id, cuisine_id),
	FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
	FOREIGN KEY (cuisine_id) REFERENCES Cuisines(cuisine_id)
);

CREATE TABLE Recipes (
	recipe_id int IDENTITY(1,1),
	yummly_recipe_id varchar(512),
	cuisine_id smallint unsigned,
	saltiness float CHECK (saltiness >= 0.0 AND saltiness <= 1.0),
	sweetness float CHECK (sweetness >= 0.0 AND sweetness <= 1.0),
	sourness float CHECK (sourness >= 0.0 AND sourness <= 1.0),
	bitterness float CHECK (bitterness >= 0.0 AND bitterness <= 1.0),
	FOREIGN KEY (cuisine_id) REFERENCES Cuisines(cuisine_id),
	PRIMARY KEY (recipe_id),
	UNIQUE (yummly_recipe_id)
);

CREATE TABLE IngredientsRecipes (
	ingredient varchar(256),
	recipe_id int,
	PRIMARY KEY (ingredient, recipe_id),
	FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

CREATE CLUSTERED INDEX ingredient_index
	ON IngredientsRecipes
	USING hash(ingredient);

CREATE INDEX flavors_index
	ON Recipes (saltiness, sweetness, sourness, bitterness);
	
CREATE INDEX restaurants_location_index
	ON Restaurants (lat, lng);
	
CREATE INDEX restaurants_review_index
	ON Restaurants (agg_review);
	
CREATE INDEX restaurants_price_index
	ON Restaurants (price_category);