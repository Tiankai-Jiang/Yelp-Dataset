select * from Friends limit 5;
select * from Users limit 5;
select * from Business limit 5;

select * from BusinessFollowers;
select * from UserFollowers;

select * from Reviews where review_id = "pPOWeAgwsRaJs_dArsBW5x";

delete from Reviews where review_id = "pPOWeAgwsRaJs_dArsBW5x";

delete from UserStars where review_id = "pPOWeAgwsRaJs_dArsBW5x";

SELECT count(*) FROM UserStars WHERE user_id='123' AND review_id='123';

SELECT * FROM (SELECT * FROM UserFollowers WHERE user_id1 = "___QCazm0YrHLd3uNUPYMA")f
    INNER JOIN Reviews ON Reviews.user_id = f.user_id2
    LEFT JOIN ReadReviews ON Reviews.review_id = ReadReviews.review_id
WHERE ReadReviews.review_id IS NULL;

SELECT Reviews.review_id as review_id, Reviews.user_id as reviewer, business_id, content FROM UserFollowers
    INNER JOIN Reviews ON Reviews.user_id = UserFollowers.user_id2
    LEFT JOIN ReadReviews ON Reviews.review_id = ReadReviews.review_id
WHERE ReadReviews.review_id IS NULL AND UserFollowers.user_id1 = "___QCazm0YrHLd3uNUPYMA";

select distinct user_id from Reviews limit 5;
# ___QCazm0YrHLd3uNUPYMA  ___DPmKJsBF2X6ZKgAeGqg
select * from Reviews where user_id = "___DPmKJsBF2X6ZKgAeGqg";
select * from UserStars;
insert into UserFollowers(user_id1, user_id2) VALUES ("___QCazm0YrHLd3uNUPYMA", "___DPmKJsBF2X6ZKgAeGqg");

select * from ReadReviews;
delete from ReadReviews;

SELECT Reviews.review_id as review_id, Reviews.user_id as reviewer, Reviews.business_id as business_id, content FROM BusinessFollowers
    INNER JOIN Reviews ON Reviews.business_id = BusinessFollowers.business_id
    LEFT JOIN ReadReviews ON Reviews.review_id = ReadReviews.review_id
WHERE ReadReviews.review_id IS NULL AND BusinessFollowers.user_id = "___QCazm0YrHLd3uNUPYMA";

delete from Reviews where review_id = "gDxz3tC7Y8oaY2taPyPqCp";

# bid __1uG7MLxWGFIv2fCGPiQQ
# uid ___MTsBloH4jvybJ5DrTYw