use mydb1;
SHOW CREATE TABLE tweets3;
tweets3, CREATE TABLE `tweets3` (
  `tweetID` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `movies_movieName` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `dateTime` datetime(6) DEFAULT NULL,
  `tweet` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `result` varchar(6) DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `theatrecount` int(11) DEFAULT NULL,
  `starmeter` int(11) DEFAULT NULL,
  `num_sentiment` int(11) DEFAULT NULL,
  `movie_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


use smdm;
# Table, Create Table
 CREATE TABLE `party_sentiment` (
 `id_t1` bigint NOT NULL AUTO_INCREMENT,
  `tweetID` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `party_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `dateTime` datetime(6) DEFAULT NULL,
  `tweet` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `source` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `country_code` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `full_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `place_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `quote_count` int(11) DEFAULT NULL,
  `reply_count` int(11) DEFAULT NULL,
  `retweet_count` int(11) DEFAULT NULL,
  `favorite_count` int(11) DEFAULT NULL,
  `result` varchar(6) DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `num_sentiment` int(11) DEFAULT NULL,
  primary key (id_t1)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#delete all data from table
DELETE FROM party_sentiment;

#seed auto increment
ALTER TABLE party_sentiment AUTO_INCREMENT = 1;

