drop table if exists Users;
CREATE TABLE Users(
    user_id char(22) PRIMARY KEY,
    name varchar(36) NOT NULL,
    review_count int NOT NULL DEFAULT 0,
    yelping_since date NOT NULL,
    useful int NOT NULL DEFAULT 0,
    funny int NOT NULL DEFAULT 0,
    cool int NOT NULL DEFAULT 0,
    fans int NOT NULL DEFAULT 0,
    average_stars float NOT NULL DEFAULT 0.0,
    compliment_hot int NOT NULL DEFAULT 0,
    compliment_more int NOT NULL DEFAULT 0,
    compliment_profile int NOT NULL DEFAULT 0,
    compliment_cute int NOT NULL DEFAULT 0,
    compliment_list int NOT NULL DEFAULT 0,
    compliment_note int NOT NULL DEFAULT 0,
    compliment_plain int NOT NULL DEFAULT 0,
    compliment_cool int NOT NULL DEFAULT 0,
    compliment_funny int NOT NULL DEFAULT 0,
    compliment_writer int NOT NULL DEFAULT 0,
    compliment_photos int NOT NULL DEFAULT 0
);

drop table if exists Friends;
CREATE TABLE Friends(
    user_id1 char(22) NOT NULL,
    user_id2 char(22) NOT NULL,
    PRIMARY KEY (user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES Users(user_id),
    FOREIGN KEY (user_id2) REFERENCES Users(user_id)
);

drop table if exists EliteYears;
CREATE TABLE EliteYears(
    user_id char(22) NOT NULL,
    elite smallint NOT NULL,
    PRIMARY KEY (user_id, elite),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

drop table if exists Business;
CREATE TABLE Business(
    business_id char(22) PRIMARY KEY,
    name varchar(72) NOT NULL,
    address varchar(144) NOT NULL,
    city varchar(72) NOT NULL,
    state varchar(4) NOT NULL,
    postal_code varchar(10) NOT NULL,
    latitude float NOT NULL,
    longitude float NOT NULL,
    stars float NOT NULL DEFAULT 0.0,
    review_count int NOT NULL DEFAULT 0,
    is_open tinyint NOT NULL DEFAULT 0
);

drop table if exists Reviews;
CREATE TABLE Reviews(
    review_id char(22) PRIMARY KEY,
    user_id char(22) NOT NULL,
    business_id char(22) NOT NULL,
    stars float NOT NULL DEFAULT 0.0,
    useful int NOT NULL DEFAULT 0,
    funny int NOT NULL DEFAULT 0,
    cool int NOT NULL DEFAULT 0,
    content varchar(5004) NOT NULL,
    review_date date NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

drop table if exists Tips;
CREATE TABLE Tips(
    tip_id char(22) PRIMARY KEY,
    user_id char(22) NOT NULL,
    business_id char(22) NOT NULL,
    content varchar(512) NOT NULL,
    tip_date date NOT NULL,
    compliment_count int NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

drop table if exists Attributes;
CREATE TABLE Attributes(
    attribute_id smallint PRIMARY KEY,
    attribute_name varchar(64) NOT NULL
);

drop table if exists AttributeXBusiness;
CREATE TABLE AttributeXBusiness(
    business_id char(22) NOT NULL,
    attribute_id smallint NOT NULL,
    value varchar(255) NOT NULL,
    PRIMARY KEY (business_id, attribute_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id),
    FOREIGN KEY (attribute_id) REFERENCES Attributes(attribute_id)
);

drop table if exists BusinessHours;
CREATE TABLE BusinessHours(
    business_id char(22) NOT NULL,
    day char(3) NOT NULL,
    hours varchar(12) NOT NULL,
    PRIMARY KEY (business_id, day),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

drop table if exists Categories;
CREATE TABLE Categories(
    category_id smallint PRIMARY KEY,
    category_name varchar(64) NOT NULL
);

drop table if exists CategoryXBusiness;
CREATE TABLE CategoryXBusiness(
    business_id char(22) NOT NULL,
    category_id smallint NOT NULL,
    PRIMARY KEY (business_id, category_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

drop table if exists Checkin;
CREATE TABLE Checkin(
    business_id char(22) NOT NULL,
    checkin_date date NOT NULL,
    PRIMARY KEY (business_id, checkin_date),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

drop table if exists Photos;
CREATE TABLE Photos(
    photo_id char(22) PRIMARY KEY,
    business_id char(22) NOT NULL,
    label varchar(32) NOT NULL,
    caption varchar(144) DEFAULT NULL,
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

drop table if exists UserFollowers;
CREATE TABLE UserFollowers(
    -- user1 follows user2
    user_id1 char(22) NOT NULL,
    user_id2 char(22) NOT NULL,
    PRIMARY KEY (user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES Users(user_id),
    FOREIGN KEY (user_id2) REFERENCES Users(user_id)
);

drop table if exists BusinessFollowers;
CREATE TABLE BusinessFollowers(
    -- a user follows a business
    user_id char(22) NOT NULL,
    business_id char(22) NOT NULL,
    PRIMARY KEY (user_id, business_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

drop table if exists ReadReviews;
CREATE TABLE ReadReviews(
    -- a user have read a review
    user_id char(22) NOT NULL,
    review_id char(22) NOT NULL,
    PRIMARY KEY (user_id, review_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (review_id) REFERENCES Reviews(review_id)
);

drop table if exists UserStars;
CREATE TABLE UserStars(
    -- a user have given a star to a review
    user_id char(22) NOT NULL,
    review_id char(22) NOT NULL,
    PRIMARY KEY (user_id, review_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (review_id) REFERENCES Reviews(review_id)
);